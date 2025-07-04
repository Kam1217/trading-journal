from django.shortcuts import render, redirect
from .forms import UploadForm
from .handle_csv_upload import handle_upload_csv
from .pnl_calculations import calendar_daily_pnl, overview_pnl, calendar_weekly_pnl

# Create your views here.

def pnl_calendar(request):
    context = {
        "overview_pnl": overview_pnl(),
        "calendar_daily_pnl": calendar_daily_pnl(),
        "calendar_weekly_pnl" : calendar_weekly_pnl(),
        }
    if request.POST:
        form = UploadForm(request.POST, request.FILES)
        if form.is_valid(): 
            handle_upload_csv(request.FILES["csv_file"])
            return redirect("pnl_calendar")
    else:
        form = UploadForm()
    context["form"] = form
    return render(request,"pnl_calendar.html", context)  

