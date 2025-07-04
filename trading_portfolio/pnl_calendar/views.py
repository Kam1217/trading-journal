from django.shortcuts import render
from .forms import UploadForm
from .handle_csv_upload import handle_upload_csv
from .pnl_calculations import calendar_pnl

# Create your views here.

def pnl_calendar(request):
    context = {"calendar_pnl": calendar_pnl()}
    if request.POST:
        form = UploadForm(request.POST, request.FILES)
        if form.is_valid(): 
            handle_upload_csv(request.FILES["csv_file"])
    else:
        form = UploadForm()
    context["form"] = form
    return render(request,"pnl_calendar.html", context)

