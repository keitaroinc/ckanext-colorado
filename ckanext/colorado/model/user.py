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

import uuid
import logging

import sqlalchemy as sa
from sqlalchemy import func

import ckan.logic as logic
import ckan.model as model

user_extra = None
log = logging.getLogger(__name__)
NotFound = logic.NotFound

__all__ = ['UserExtra', 'user_extra', ]


def uuid4():
    return str(uuid.uuid4())


def setup():
    if user_extra is None:
        define_user_extra_table()
        log.debug('User extra table defined in memory')

        if not user_extra.exists():
            user_extra.create()
        else:
            log.debug('User extra table already exists')


class UserExtra(model.DomainObject):

    @classmethod
    def get(cls, user_id, key, default=None):
        '''Finds a single entity in the register.'''
        kw = {'user_id': user_id, 'key': key}
        query = model.Session.query(cls).autoflush(False)
        result = query.filter_by(**kw).first()
        if result:
            return result
        else:
            return default

    @classmethod
    def extra_exists(cls, key):
        """Returns true if there is an extra field with the same key."""
        query = model.Session.query(cls).autoflush(False)
        return query.filter(func.lower(cls.key) == func.lower(key)).first() is not None

    @classmethod
    def delete(cls, user_id, key):
        """Deletes single instance."""
        kwds = {'user_id': user_id, 'key': key}
        obj = model.Session.query(cls).filter_by(**kwds).first()
        if not obj:
            raise NotFound
        model.Session.delete(obj)
        model.Session.commit()


def define_user_extra_table():
    global user_extra
    user_extra = sa.Table('user_extra', model.meta.metadata,
                          sa.Column('id', sa.types.UnicodeText,
                                    primary_key=True, default=uuid4),
                          sa.Column('user_id', sa.types.UnicodeText,
                                    sa.ForeignKey('user.id')),
                          sa.Column('key', sa.types.UnicodeText), 
                          sa.Column('user_type', sa.types.UnicodeText),
                          sa.Column('expertise', sa.types.UnicodeText),
                          sa.Column('job_preference', sa.types.UnicodeText),
                          sa.Column('experience', sa.types.UnicodeText),
                          sa.Column('education', sa.types.UnicodeText),
                          sa.Column('insurance_type', sa.types.UnicodeText),
                          )
    model.meta.mapper(UserExtra, user_extra)
