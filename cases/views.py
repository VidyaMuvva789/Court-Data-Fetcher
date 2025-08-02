
from django.shortcuts import render
from .forms import CaseSearchForm
from .scraper import fetch_case_details
import json
from .models import CaseQuery

def search_case(request):
    data = None
    error = None
    if request.method == "POST":
        form = CaseSearchForm(request.POST)
        if form.is_valid():
            ct = form.cleaned_data['case_type']
            cn = form.cleaned_data['case_number']
            fy = form.cleaned_data['filing_year']
            try:
                data = fetch_case_details(ct, cn, fy)
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
