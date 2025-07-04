from django.db.models import Sum, Count
from django.db.models.functions import TruncDate
from .models import Trades

#Function to calculate overview data
def overview_pnl():
    total_pnl = Trades.objects.aggregate(
        total_gross_pnl = Sum("gross_pnl"),
        total_fee = Sum("fee"),
        total_net_pnl = Sum("net_pnl"),
        number_of_trades = Count("trade_id"),
    )
    return (total_pnl)

#Fucntion to calculate individual day data for the calendar
def calendar_pnl():
    daily_pnl = Trades.objects.annotate(
        date = TruncDate("trade_date")
    ).values("date").annotate(
        total_fee = Sum("fee"),
        total_net_pnl = Sum("net_pnl"),
        number_of_trades = Count("trade_id"),
    )
    return list(daily_pnl)

#Function to calculate end of week pnl
