from django.shortcuts import render, redirect
from datetime import date
from .forms import UploadForm
from .handle_csv_upload import handle_upload_csv
from .pnl_calculations import calendar_daily_pnl, overview_pnl, calendar_weekly_pnl
from .generate_calendar import generate_calendar
from django.contrib import messages

# Create your views here.

def pnl_calendar(request):
    if request.POST:
        form = UploadForm(request.POST, request.FILES)
        if form.is_valid():
            csv_files = form.cleaned_data["csv_file"]

            for csv_file in csv_files: 
                try:
                    handle_upload_csv(csv_file)
                except ValueError as e:
                    messages.error(request, f"Error in {csv_file.name}: {str(e)}")
                except Exception as e:
                    messages.error(request, f"Unexpected error in {csv_file.name}: {str(e)}")
                
            return redirect("pnl_calendar")
        else:
            for field, errors in form.errors.items():
                 for error in errors:
                     messages.error(request, error)
    else:
        form = UploadForm()

    #Get date 
    today = date.today()

    try:
        year_param = request.GET.get("year", "").strip()
        year = int(year_param) if year_param else today.year
    except (ValueError, TypeError):
        year = today.year
    
    try:
        month_param = request.GET.get("month", "").strip()
        month = int(month_param) if month_param else today.month
    except (ValueError, TypeError):
        month = today.month

    if not (1 <= month <= 12):
        month = today.month
    
    if not (1900 <= year <= 2100): 
        year = today.year

    current_date = date(year, month, 1)

    #Calculate previous dates
    #Previous year if month is Jauary
    if month == 1:
        previous_month = {"month": 12, "year": year - 1}
    else:
        previous_month = {"month": month - 1, "year": year}
    
    #Next year if month is December
    if month == 12:
        next_month = {"month": 1, "year": year + 1}
    else:
        next_month = {"month": month + 1, "year": year}
    
    #Generate calendar
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
        "current_month": current_date.strftime('%B %Y'),
        "previous_month" : previous_month,
        "next_month": next_month,
    }

    return render(request,"pnl_calendar.html", context)  
