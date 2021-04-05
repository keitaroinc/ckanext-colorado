"""
Copyright (c) 2019 Keitaro AB

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as
published by the Free Software Foundation, either version 3 of the
License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

import logging

from flask import Blueprint
from paste.deploy.converters import asbool

import ckan.logic as logic
import ckan.lib.base as base
import ckan.model as model
import ckan.lib.captcha as captcha
import ckan.lib.helpers as h
import ckan.logic.schema as schema
import ckan.plugins.toolkit as toolkit
import ckan.lib.authenticator as authenticator
import ckan.lib.navl.dictization_functions as dictization_functions
from ckan.views.user import RegisterView, EditView
from ckan import authz
from ckan.common import _, config, g, request


log = logging.getLogger(__name__)

edit_user_form = u'user/edit_user_form.html'

user = Blueprint(u'colorado_user', __name__, url_prefix=u'/user')


def set_repoze_user(user_id, resp):
    u'''Set the repoze.who cookie to match a given user_id'''
    if u'repoze.who.plugins' in request.environ:
        rememberer = request.environ[u'repoze.who.plugins'][u'friendlyform']
        identity = {u'repoze.who.userid': user_id}
        resp.headers.extend(rememberer.remember(request.environ, identity))


def _edit_form_to_db_schema():
    return schema.user_edit_form_schema()


def _extra_template_variables(context, data_dict):
    is_sysadmin = authz.is_sysadmin(g.user)
    try:
        user_dict = logic.get_action(u'user_show')(context, data_dict)
    except logic.NotFound:
        h.flash_error(_(u'Not authorized to see this page'))
        return
    except logic.NotAuthorized:
        base.abort(403, _(u'Not authorized to see this page'))

    is_myself = user_dict[u'name'] == g.user
    about_formatted = h.render_markdown(user_dict[u'about'])
    extra = {
        u'is_sysadmin': is_sysadmin,
        u'user_dict': user_dict,
        u'is_myself': is_myself,
        u'about_formatted': about_formatted
    }
    return extra


class RegisterColoradoUserView(RegisterView):

    def post(self):
        context = self._prepare()
        try:
            data_dict = logic.clean_dict(
                dictization_functions.unflatten(
                    logic.tuplize_dict(logic.parse_params(request.form))))
        except dictization_functions.DataError:
            base.abort(400, _(u'Integrity Error'))

        context[u'message'] = data_dict.get(u'log_message', u'')
        try:
            captcha.check_recaptcha(request)
        except captcha.CaptchaError:
            error_msg = _(u'Bad Captcha. Please try again.')
            h.flash_error(error_msg)
            return self.get(data_dict)

        try:
            logic.get_action(u'user_create')(context, data_dict)
            toolkit.get_action(u'user_extra_create')(context, data_dict)
        except logic.NotAuthorized:
            base.abort(403, _(u'Unauthorized to create user %s') % u'')
        except logic.NotFound:
            base.abort(404, _(u'User not found'))
        except logic.ValidationError as e:
            errors = e.error_dict
            error_summary = e.error_summary
            return self.get(data_dict, errors, error_summary)

        if g.user:
            h.flash_success(
                _(u'User "%s" is now registered but you are still '
                  u'logged in as "%s" from before') % (data_dict[u'name'],
                                                       g.user))
            if authz.is_sysadmin(g.user):
                return h.redirect_to(u'user.activity', id=data_dict[u'name'])
            else:
                return base.render(u'user/logout_first.html')

        resp = h.redirect_to(u'user.me')
        set_repoze_user(data_dict[u'name'], resp)
        return resp


class EditColoradoUserView(EditView):
    
    def post(self, id=None):
        context, id = self._prepare(id)
        if not context[u'save']:
            return self.get(id)
        log.debug(context)
        if id in (g.userobj.id, g.userobj.name):
            current_user = True
        else:
            current_user = False
        old_username = g.userobj.name

        try:
            data_dict = logic.clean_dict(
                dictization_functions.unflatten(
                    logic.tuplize_dict(logic.parse_params(request.form))))
        except dictization_functions.DataError:
            base.abort(400, _(u'Integrity Error'))
        data_dict.setdefault(u'activity_streams_email_notifications', False)

        context[u'message'] = data_dict.get(u'log_message', u'')
        data_dict[u'id'] = id
        email_changed = data_dict[u'email'] != g.userobj.email

        if (data_dict[u'password1']
                and data_dict[u'password2']) or email_changed:
            identity = {
                u'login': g.user,
                u'password': data_dict[u'old_password']
            }
            auth = authenticator.UsernamePasswordAuthenticator()

            if auth.authenticate(request.environ, identity) != g.user:
                errors = {
                    u'oldpassword': [_(u'Password entered was incorrect')]
                }
                error_summary = {_(u'Old Password'): _(u'incorrect password')}
                return self.get(id, data_dict, errors, error_summary)

        try:
            user = logic.get_action(u'user_update')(context, data_dict)
            user_extra = toolkit.get_action(u'user_extra_update')(context, data_dict)
        except logic.NotAuthorized:
            base.abort(403, _(u'Unauthorized to edit user %s') % id)
        except logic.NotFound:
            base.abort(404, _(u'User not found'))
        except logic.ValidationError as e:
            errors = e.error_dict
            error_summary = e.error_summary
            return self.get(id, data_dict, errors, error_summary)

        h.flash_success(_(u'Profile updated'))
        resp = h.redirect_to(u'user.read', id=user[u'name'])
        if current_user and data_dict[u'name'] != old_username:
            set_repoze_user(data_dict[u'name'], resp)
        return resp

    def get(self, id=None, data=None, data_extra=None, errors=None, error_summary=None):
        context, id = self._prepare(id)

        model = context.get('model')
        user = context.get('user')
        user_obj = model.User.get(id)
        user_id = user_obj.id
        data_dict = {u'id': id,
                     u'user_id': user_id,
                     u'key': 'unique'
                     }

        try:
            old_data = logic.get_action(u'user_show')(context, data_dict)
            old_extra_data = toolkit.get_action(u'user_extra_read')(context, data_dict)

            g.display_name = old_data.get(u'display_name')
            g.user_name = old_data.get(u'name')

            data_old = data or old_data
            data_extra = data_extra or old_extra_data
            
            if data_extra is None:
                data = data_old
            else:
                data = dict(data_extra, **data_old)
    
        except logic.NotAuthorized:
            base.abort(403, _(u'Unauthorized to edit user %s') % u'')
        except logic.NotFound:
            base.abort(404, _(u'User not found'))
        user_obj = context.get(u'user_obj')

        if not (authz.is_sysadmin(g.user) or g.user == user_obj.name):
            msg = _(u'User %s not authorized to edit %s') % (g.user, id)
            base.abort(403, msg)

        errors = errors or {}
        vars = {
            u'data': data,
            u'errors': errors,
            u'error_summary': error_summary
        }
        
        extra_vars = _extra_template_variables({
            u'model': model,
            u'session': model.Session,
            u'user': g.user
        }, data_dict)

        extra_vars[u'is_myself'] = True
        extra_vars[u'show_email_notifications'] = asbool(
            config.get(u'ckan.activity_streams_email_notifications'))
        vars.update(extra_vars)
        extra_vars[u'form'] = base.render(edit_user_form, extra_vars=vars)

        return base.render(u'user/edit.html', extra_vars)


user.add_url_rule(
    u'/register', view_func=RegisterColoradoUserView.as_view(str(u'register')))

_edit_view = EditColoradoUserView.as_view(str(u'edit'))
user.add_url_rule(u'/edit', view_func=_edit_view)
user.add_url_rule(u'/edit/<id>', view_func=_edit_view)
