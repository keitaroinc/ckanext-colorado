"""Colorado custom helpers.
"""

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
