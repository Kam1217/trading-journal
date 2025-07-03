from django.urls import path
from .import views

urlpatterns = [
    path("", views.pnl_calendar, name="pnl_calendar")
]