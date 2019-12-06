import logging
import json
import socket

from paste.deploy.converters import asbool

import ckan.lib.dictization
import ckan.logic as logic
import ckan.logic.action
import ckan.logic.schema
import ckan.lib.dictization.model_dictize as model_dictize
import ckan.lib.navl.dictization_functions
import ckan.plugins as plugins
import ckan.lib.search as search
import ckan.lib.plugins as lib_plugins
import ckan.plugins.toolkit as toolkit
import ckan.lib.navl.dictization_functions as df
from ckanext.colorado.model.user import UserExtra
from ckanext.colorado.model.user_schema import user_extra_schema
from ckanext.colorado.model.user_schema import user_extra_delete_schema

# Define some shortcuts
# Ensure they are module-private so that they don't get loaded as available
# actions in the action API.
_validate = ckan.lib.navl.dictization_functions.validate
_table_dictize = ckan.lib.dictization.table_dictize
_check_access = logic.check_access
NotFound = logic.NotFound
ValidationError = logic.ValidationError
_get_or_bust = logic.get_or_bust


log = logging.getLogger(__name__)


def user_extra_create(context, data_dict):
    '''Create user extra parameter.

        :param key: Key of the parameter.
        :type key: string

        :param value: Value of the parameter.
        :type value: string

        :param active: State of the parameter. Default is active.
        :type active: string

        '''

    data, errors = df.validate(data_dict, user_extra_schema(), context)

    if errors:
        raise toolkit.ValidationError(errors)

    user_obj = context.get('user_obj')

    user_id = user_obj.id
    key = data.get('key')
    user_type = data.get('user_type')

    user_extra = UserExtra.get(user_id=user_id, key=key)
    if user_extra:
        user_extra.key = key
        user_extra.user_type = user_type
        user_extra.save()
    else:
        user_extra = UserExtra(
            user_id=user_id,
            key=key,
            user_type=user_type
        )
        user_extra.save()

    return _table_dictize(user_extra, context)


def user_extra_update(context, data_dict):
    '''Update user extra parameter.

        :param key: Key of the parameter you want to update.
        :type key: string

        :param value: The new value of the parameter.
        :type value: string

        '''

    data, errors = df.validate(data_dict, user_extra_schema(), context)

    if errors:
        raise toolkit.ValidationError(errors)

    model = context.get('model')
    user = context.get('user')
    user_obj = model.User.get(user)
    user_id = user_obj.id
    key = data.get('key')
    user_type = data.get('user_type')
    expertise = data.get('expertise')
    job_preference = data.get('job_preference')
    experience = data.get('experience')
    education = data.get('education')
    insurance_type = data.get('insurance_type')

    user_extra = UserExtra.get(user_id, key)
    
    if user_extra is None:
        raise logic.NotFound

    user_extra.key = key
    user_extra.user_type = user_type
    user_extra.expertise = expertise
    user_extra.job_preference = job_preference
    user_extra.experience = experience
    user_extra.education = education
    user_extra.insurance_type = insurance_type
    user_extra.save()

    return _table_dictize(user_extra, context)


def user_extra_read(context, data_dict):
    '''Read user extra parameter.

        :param key: Key of the parameter.
        :type key: string

        '''
    data, errors = df.validate(data_dict, user_extra_delete_schema(), context)
    if errors:
        raise toolkit.ValidationError(errors)
    
    user_id = data_dict.get('user_id')
    key = data.get('key')

    user_extra = UserExtra.get(user_id=user_id, key=key)

    if user_extra is not None:
        return _table_dictize(user_extra, context)
    else:
        return None


def user_extra_delete(context, data_dict):
    '''Delete user extra parameter.

        :param key: Key of the parameter you want to delete.
        :type key: string

        '''

    data, errors = df.validate(data_dict, user_extra_delete_schema(), context)

    if errors:
        raise toolkit.ValidationError(errors)

    model = context.get('model')
    user = context.get('user')
    user_obj = model.User.get(user)
    user_id = user_obj.id
    key = data.get('key')

    UserExtra.delete(user_id, key)

    return {
        'message': 'Extra with key: %s, deleted' % key
    }
