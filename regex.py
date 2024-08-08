import re

def check_na(license_no):
    match = re.search(r'^NA.*$', license_no)

    return match