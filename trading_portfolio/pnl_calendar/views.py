from django.shortcuts import render, redirect
from django.contrib import messages
from datetime import datetime, date
import calendar
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
            try:
                csv_files = form.cleaned_data["csv_file"]
                processed_count = 0

                for csv_file in csv_files: 
                    handle_upload_csv(csv_file)
                    processed_count += 1

                messages.success(request,f"Successfully processed {processed_count} CSV file(s)!")
            
            except Exception as e:
                messages.error(request, F"Error processing CSV: {str(e)}")
            except Exception as e:
                messages.error(request, f"An error occurred: {str(e)}")
            return redirect("pnl_calendar")
        else:
            for field,errors in form.errors.items():
                for error in errors:
                    messages.error(request,error)
    else:
        form = UploadForm()
    context["form"] = form
    return render(request,"pnl_calendar.html", context)  

