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

from ckan.lib.navl.validators import (ignore_missing,
                                      not_empty,
                                      not_missing,
                                      ignore_empty
                                      )
                                      

def user_extra_schema():
    return {
        'user_id': [ignore_missing, unicode],
        'key': [not_empty, unicode],
        'user_type': [not_empty, unicode],
        'expertise': [ignore_missing, unicode],
        'job_preference': [ignore_missing, unicode],
        'experience': [ignore_missing, unicode],
        'education': [ignore_missing, unicode],
        'insurance_type': [ignore_missing, unicode]
    }


def user_extra_delete_schema():
    return {
        'key': [not_empty, unicode]
    }
