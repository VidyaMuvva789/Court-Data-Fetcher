from django.shortcuts import render
from .forms import CaseSearchForm
from .scraper import fetch_case_details
import json
from .models import CaseQuery
import requests
from bs4 import BeautifulSoup
from django.http import HttpResponseBadRequest


def search_case(request):
    # fetches case details using scraper.py and saves search logs in DB 
    data = None
    error = None
    if request.method == "POST":
        form = CaseSearchForm(request.POST)
        if form.is_valid():
            ct = form.cleaned_data['case_type']
            cn = form.cleaned_data['case_number']
            fy = form.cleaned_data['filing_year']
            try:
                # fetch data from delhi high court website
                data = fetch_case_details(ct, cn, fy)
                if data and 'data' in data:
                    for case in data['data']:
                        soup = BeautifulSoup(case.get('ctype', ''), 'html.parser')
                        for a_tag in soup.find_all('a'):
                            if 'Orders' in a_tag.get_text():
                                a_tag.decompose()
                        case['ctype'] = str(soup)

                # store search logs in DB
                CaseQuery.objects.create(
                    case_type=ct,
                    case_number=cn,
                    filing_year=fy,
                    raw_json=json.dumps(data)
                )
            except Exception as e:
                error = str(e)
    else:
        form = CaseSearchForm()
    return render(request, "search.html", {"form": form, "data": data, "error": error})
  

def order_details(request):
    # fetches and displays PDF order links for cases
    ajax_url = request.GET.get("url")
    if not ajax_url:
        return HttpResponseBadRequest("Missing case details")

    headers = {
        "User-Agent": "Mozilla/5.0",
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "X-Requested-With": "XMLHttpRequest"
    }

    # gets order list from delhi high court website
    resp = requests.get(ajax_url, headers=headers, timeout=15)
    data = resp.json()

    orders = []
    for item in data.get("data", []):
        soup = BeautifulSoup(item["case_no_order_link"], "html.parser")
        link_tag = soup.find("a")
        pdf_link = None
        if link_tag and link_tag.get("href"):
            pdf_link = link_tag["href"]
            if pdf_link.startswith("/"):
                pdf_link = "https://delhihighcourt.nic.in" + pdf_link

        orders.append({
            "pdf": pdf_link,
            "date": item["order_date"]["display"],
        })

    return render(request, "order_details.html", {"orders": orders})
