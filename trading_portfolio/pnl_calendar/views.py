from django.shortcuts import render
from .forms import UploadForm

# Create your views here.

def pnl_calendar(request):
    context = {}
    context['form']= UploadForm()
    return render(request, "pnl_calendar.html", context)

