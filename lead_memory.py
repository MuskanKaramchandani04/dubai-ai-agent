# Simple in-memory storage for leads

LEADS = {}

def get_lead(user_id):
    if user_id not in LEADS:
        LEADS[user_id] = {
            "budget": None,
            "purpose": None,
            "interest": None
        }
    return LEADS[user_id]


def update_lead(user_id, key, value):
    if user_id not in LEADS:
        LEADS[user_id] = {
            "budget": None,
            "purpose": None,
            "interest": None
        }

    LEADS[user_id][key] = value