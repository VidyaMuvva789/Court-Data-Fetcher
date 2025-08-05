import requests
from bs4 import BeautifulSoup
import re

BASE_URL = "https://delhihighcourt.nic.in"

def fetch_case_details(case_type, case_number, case_year):
    """
    Fetch case details from Delhi High Court website which takes
    case type, case number anf filing year as input and returns JSON response with case details
    """
    session = requests.Session()

    # Load search page to get CAPTCHA and randomid
    search_page_url = f"{BASE_URL}/app/get-case-type-status"
    resp = session.get(search_page_url, headers={"User-Agent": "Mozilla/5.0"})
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")

    # Extract captcha value
    captcha_span = soup.find("span", id="captcha-code")
    captcha_value = captcha_span.text.strip() if captcha_span else None

    # Extract hidden input randomid
    hidden_input = soup.find("input", {"name": "randomid"})
    hidden_value = hidden_input["value"].strip() if hidden_input else None

    if not captcha_value or not hidden_value:
        raise ValueError("Could not retrieve captcha from Delhi HC website.")

    # Preparing request parameters
    params = {
        "draw": 1,
        "start": 0,
        "length": 50,
        "case_type": case_type,
        "case_number": case_number,
        "case_year": case_year,
        "captcha": captcha_value,
        "randomid": hidden_value
    }

    headers = {
        "User-Agent": "Mozilla/5.0",
        "Accept": "application/json",
        "X-Requested-With": "XMLHttpRequest",
    }

    # Sends request with search parameters
    r = session.get(search_page_url, params=params, headers=headers)
    r.raise_for_status()
    data = r.json()

    #Extract order link from ctype HTML
    for case in data.get('data', []):
        raw_ctype = case.get('ctype', '')
        match = re.search(r'href=[\'"]?([^\'" >]+)', raw_ctype)
        orderlink = match.group(1) if match else ''
        case['orderlink'] = orderlink
        
    return data
