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
