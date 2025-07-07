from django.db.models import Sum, Count
from django.db.models.functions import TruncDate, TruncWeek
from .models import Trade

#Function to calculate overview data
def overview_pnl():
    total_pnl = Trade.objects.aggregate(
        total_gross_pnl = Sum("gross_pnl"),
        total_fee = Sum("fee"),
        total_net_pnl = Sum("net_pnl"),
        number_of_trades = Count("trade_id"),
    )
    return (total_pnl)

#Fucntion to calculate individual day data for the calendar
def calendar_daily_pnl():
    daily_pnl = Trade.objects.annotate(
        day = TruncDate("trade_date")
    ).values("day").annotate(
        total_fee = Sum("fee"),
        total_net_pnl = Sum("net_pnl"),
        number_of_trades = Count("trade_id"),
    )
    return list(daily_pnl)

#Function to calculate end of week pnl
def calendar_weekly_pnl():
    weekly_pnl = Trade.objects.annotate(
        week = TruncWeek("trade_date")
    ).values("week").annotate(
        total_fee = Sum("fee"),
        total_net_pnl = Sum("net_pnl"),
        number_of_trades = Count("trade_id"),
    )
    return list(weekly_pnl)