import requests
import re
from bs4 import BeautifulSoup

def fetch_case_details(case_type, case_number, case_year):
    session = requests.Session()

    search_page_url = "https://delhihighcourt.nic.in/app/get-case-type-status"  
    search_page = session.get(search_page_url, headers={"User-Agent": "Mozilla/5.0"})
    search_page.raise_for_status()

    soup = BeautifulSoup(search_page.text, "html.parser")

    captcha_span = soup.find("span", id="captcha-code")
    captcha_value = captcha_span.text.strip() if captcha_span else None

    hidden_input = soup.find("input", {"name": "randomid"})
    hidden_value = hidden_input["value"].strip() if hidden_input else None

    if not captcha_value or not hidden_value:
        raise ValueError("Could not retrieve captcha from Delhi HC website.")

    url = "https://delhihighcourt.nic.in/app/get-case-type-status"

    params = {
        "draw": 1,
        "columns[0][data]": "DT_RowIndex",
        "columns[0][name]": "DT_RowIndex",
        "columns[0][searchable]": "true",
        "columns[0][orderable]": "false",
        "columns[0][search][value]": "",
        "columns[0][search][regex]": "false",

        "columns[1][data]": "ctype",
        "columns[1][name]": "ctype",
        "columns[1][searchable]": "true",
        "columns[1][orderable]": "true",
        "columns[1][search][value]": "",
        "columns[1][search][regex]": "false",

        "columns[2][data]": "pet",
        "columns[2][name]": "pet",
        "columns[2][searchable]": "true",
        "columns[2][orderable]": "true",
        "columns[2][search][value]": "",
        "columns[2][search][regex]": "false",

        "columns[3][data]": "orderdate",
        "columns[3][name]": "orderdate",
        "columns[3][searchable]": "true",
        "columns[3][orderable]": "true",
        "columns[3][search][value]": "",
        "columns[3][search][regex]": "false",

        "order[0][column]": 0,
        "order[0][dir]": "asc",
        "order[0][name]": "DT_RowIndex",
        "start": 0,
        "length": 50,
        "search[value]": "",
        "search[regex]": "false",

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

    response = session.get(url, params=params, headers=headers)
    response.raise_for_status()
    data = response.json()

    if not data.get('data'):
        raise ValueError("No cases found for the given details.")

    for case in data['data']:
        raw_ctype = case.get('ctype', '')
        match = re.search(r'^(.*?)(<a href=.*Orders</a>)$', raw_ctype, re.DOTALL)
        if match:
            ctype_cleaned = match.group(1).strip()
            order_link_html = match.group(2)
            href_match = re.search(r'href=[\'"]?([^\'" >]+)', order_link_html)
            orderlink = href_match.group(1) if href_match else ''
        else:
            ctype_cleaned = raw_ctype.strip()
            orderlink = ''
        case['ctype'] = ctype_cleaned
        case['orderlink'] = orderlink

    return data
