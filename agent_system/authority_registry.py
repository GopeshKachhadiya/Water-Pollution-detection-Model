AUTHORITY_DB = {
    "sea": [
        {
            "name": "Pollution Control Board",
            "email": "environment@indiancoastguard.gov.in"
        }
    ],
    "river": [
        {
            "name": "National Mission for Clean Ganga",
            "email": "support@nmcg.nic.in"
        }
    ],
    "lake": [
        {
            "name": "State Pollution Control Board",
            "email": "spcb@state.gov.in"
        }
    ],
    "ngo": [
        {
            "name": "Ocean Cleanup India",
            "email": "contact@oceancleanup.org"
        }
    ]
}

def get_authorities(water_body="sea"):
    return AUTHORITY_DB.get(water_body, AUTHORITY_DB["ngo"])
