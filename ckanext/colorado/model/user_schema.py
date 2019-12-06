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
