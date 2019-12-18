"""Colorado custom helpers.
"""
import ckan.plugins.toolkit as toolkit
from datetime import datetime
from human_dates import time_ago_in_words


def get_user_types():
    """Defines options available for user types.
    """
    return [
        {'name': "job_seeker", 'value': "Job Seeker"},
        {'name': "agency", 'value': "Agency"}
    ]


def get_expertise():
    """Defines options available for field of expertise.
    """
    return [
        {'name': "accountant", 'value': "Accountant"},
        {'name': "actor", 'value': "Actor"},
        {'name': "analyst", 'value': "Analyst"},
        {'name': "baker", 'value': "Baker"},
        {'name': "bodyguard", 'value': "Bodyguard"},
        {'name': "cameraman", 'value': "Cameraman"},
        {'name': "chef", 'value': "Chef"},
        {'name': "driver", 'value': "Driver"},
        {'name': "fireman", 'value': "Fireman"},
        {'name': "gardener", 'value': "Gardener"},
        {'name': "historian", 'value': "Historian"},
        {'name': "investigator", 'value': "Investigator"},
        {'name': "lawyer", 'value': "Lawyer"},
        {'name': "magician", 'value': "Magician"},
        {'name': "mechanic", 'value': "Mechanic"},
        {'name': "neurologist", 'value': "Neurologist"},
        {'name': "painter", 'value': "Painter"},
        {'name': "pilot", 'value': "Pilot"},
        {'name': "software_engineer", 'value': "Software Engineer"}
    ]


def get_insurance_types():
    """Defines options available for insurance types.
    """
    return [
        {'name': "life_insurance", 'value': "Life Insurance"},
        {'name': "health_insurance", 'value': "Health Insurance"},
        {'name': "ltd_insurance", 'value': "Long-term Disability Insurance"},
        {'name': "auto_insurance", 'value': "Auto Insurance"},
        {'name': "none", 'value': "None"}
    ]


def get_job_preferences():
    """Defines options available for job preferences.
    """
    return [
        {'name': "full_time", 'value': "Full Time"},
        {'name': "part_time", 'value': "Part Time"},
        {'name': "contract", 'value': "Contract"},
        {'name': "internship", 'value': "Internship"}
    ]


def get_job_types():
    """Defines options available for job types
    """
    return [
        {'name': 'commission', 'value': 'Commission'},
        {'name': 'remote', 'value': 'Remote'},
        {'name': 'full-time', 'value': 'Full-time'},
        {'name': 'part-time', 'value': 'Part-time'},
        {'name': 'temporary', 'value': 'Temporary'},
        {'name': 'contract', 'value': 'Contract'},
        {'name': 'internship', 'value': 'Internship'}
    ]


def get_job_locations():
    """Define options available for job locations
    """
    return [
        {'name': 'indianapolis', 'value': 'Indianapolis, IN'},
        {'name': 'memphis', 'value': 'Memphis, TN'},
        {'name': 'houston', 'value': 'Houston, TX'},
        {'name': 'st-louis', 'value': 'St. Louis, MO'},
        {'name': 'new-york', 'value': 'New York, NY'},
        {'name': 'austin', 'value': 'Austin, TX'},
        {'name': 'baltimore', 'value': 'Baltimore, MD'},
        {'name': 'cleveland', 'value': 'Cleveland, OH'},
        {'name': 'nashville', 'value': 'Nashville, TN'},
        {'name': 'martinsburg', 'value': 'Martinsburg, WV'},
        {'name': 'durham', 'value': 'Durham, NC'},
        {'name': 'washington', 'value': 'Washington, DC'},
        {'name': 'orlando', 'value': 'Orlando, FL'},
        {'name': 'columbus', 'value': 'Columbus, OH'},
        {'name': 'chicago', 'value': 'Chicago, IL'}
    ]


def get_experiance_level():
    """Define options available for require job experiance
    """
    return [
        {'name': 'all', 'value': 'All'},
        {'name': 'entry-level', 'value': 'Entry Level'},
        {'name': 'mid-level', 'value': 'Mid Level'},
        {'name': 'senior-level', 'value': 'Senior Level'}
    ]


def get_salary_estimate():
    """Define options availabe for salaries
    """
    return [
        {'name': '35000', 'value': '$35,000+'},
        {'name': '40000', 'value': '$40,000+'},
        {'name': '45000', 'value': '$45,000+'},
        {'name': '50000', 'value': '$50,000+'},
        {'name': '55000', 'value': '$55,000+'},
        {'name': '60000', 'value': '$60,000+'},
        {'name': '65000', 'value': '$65,000+'}
    ]


def pretty_date(str):
    """ Return time passed fro the given time
    """
    t = datetime.strptime(str, '%Y-%m-%dT%H:%M:%S.%f')

    return time_ago_in_words(t)


def get_recently_updated_datasets(limit=6):
    '''
     Returns recent created or updated datasets.
    :param limit: Limit of the datasets to be returned. Default is 5.
    :type limit: integer
    :returns: a list of recently created or updated datasets
    :rtype: list
    '''
    try:
        pkg_search_results = toolkit.get_action('package_search')(data_dict={
            'sort': 'metadata_modified desc',
            'rows': limit,
        })['results']

    except toolkit.ValidationError, search.SearchError:
        return []
    else:
        pkgs = []
        for pkg in pkg_search_results:
            package = toolkit.get_action('package_show')(
                data_dict={'id': pkg['id']})
            modified = datetime.strptime(
                package['metadata_modified'].split('T')[0], '%Y-%m-%d')
            package['days_ago_modified'] = ((datetime.now() - modified).days)
            pkgs.append(package)
        return pkgs


def user_type(user):
    user_type = None
    if user:
        user_type = toolkit.get_action('user_extra_read')(
            {}, {'key': 'unique', 'user_id': user['id']})
        if user_type:
            return user_type.get('user_type', None)

def expertise(user):
    expertise = None
    if user:
        expertise = toolkit.get_action('user_extra_read')(
            {}, {'key': 'unique', 'user_id': user['id']})
        if expertise:
            return expertise.get('expertise', None)

def job_preference(user):
    job_preference = None
    if user:
        job_preference = toolkit.get_action('user_extra_read')(
            {}, {'key': 'unique', 'user_id': user['id']})
        if job_preference:
            return job_preference.get('job_preference', None)

def experience(user):
    experience = None
    if user:
        experience = toolkit.get_action('user_extra_read')(
            {}, {'key': 'unique', 'user_id': user['id']})
        if experience:
            return experience.get('experience', None)

def education(user):
    education = None
    if user:
        education = toolkit.get_action('user_extra_read')(
            {}, {'key': 'unique', 'user_id': user['id']})
        if education:
            return education.get('education', None)

def insurance_type(user):
    insurance_type = None
    if user:
        insurance_type = toolkit.get_action('user_extra_read')(
            {}, {'key': 'unique', 'user_id': user['id']})
        if insurance_type:
            return insurance_type.get('insurance_type', None)
