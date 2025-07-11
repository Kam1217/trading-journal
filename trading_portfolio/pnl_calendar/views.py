from django.shortcuts import render, redirect
from datetime import date
from .forms import UploadForm
from .handle_csv_upload import handle_upload_csv
from .pnl_calculations import calendar_daily_pnl, overview_pnl, calendar_weekly_pnl
from .generate_calendar import generate_calendar

# Create your views here.

def pnl_calendar(request):
    if request.POST:
        form = UploadForm(request.POST, request.FILES)
        if form.is_valid():
            handle_upload_csv(request.FILES["csv_file"])
            return redirect("pnl_calendar")
    else:
        form = UploadForm()

    today = date.today()
    year = today.year
    month = today.month
    
    calendar_weeks = generate_calendar(
        calendar_daily_pnl(), 
        calendar_weekly_pnl(), 
        year, 
        month
    )
    
    context = {
        "form" : form,
        "overview_pnl": overview_pnl(),
        "calendar_daily_pnl": calendar_daily_pnl(),
        "calendar_weekly_pnl" : calendar_weekly_pnl(),
        "calendar_weeks": calendar_weeks,
        "current_month": today.strftime('%B %Y'),
    }

    return render(request,"pnl_calendar.html", context)  
