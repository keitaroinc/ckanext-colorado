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

# encoding: utf-8
import logging
import inspect
import os.path

from flask import Blueprint, Response
from flask.views import MethodView
import ckan.lib.base as base
import ckan.lib.helpers as h
import ckan.lib.navl.dictization_functions as ls
import ckan.logic as logic
import ckan.model as model
from ckan.common import _, g, request, response
import paste.fileapp
import ckanapi_exporter.exporter as exporter


log = logging.getLogger(__name__)


export = Blueprint(
    u'export',
    __name__,
    url_prefix=u'/export'
)


def _get_context():
    return dict(model=model, user=g.user,
                auth_user_obj=g.userobj,
                session=model.Session)


def _absolute_path(relative_path):
    """Return an absolute path given a path relative to this Python file."""
    return os.path.join(os.path.dirname(os.path.abspath(
        inspect.getfile(inspect.currentframe()))), relative_path)


def download_metadata(name):
    params={'fq': 'name:{}'.format(name)}

    csv_string = exporter.export(
        'http://localhost:5000',
        _absolute_path('columns.json'),
        params=str(params))

    return Response(
        csv_string,
        mimetype="text/csv",
        headers={"Content-disposition":
                 "attachment; filename={}-matadata.csv".format(name)})


def download_metadata_all():
    csv_string = exporter.export(
        'http://localhost:5000',
        _absolute_path('columns.json'))

    return Response(
        csv_string,
        mimetype="text/csv",
        headers={"Content-disposition":
                 "attachment; filename=jobs-matadata.csv"})



export.add_url_rule(u'/all', methods=[u'get'], view_func=download_metadata_all)
export.add_url_rule(u'/<name>', methods=[u'get'], view_func=download_metadata)

