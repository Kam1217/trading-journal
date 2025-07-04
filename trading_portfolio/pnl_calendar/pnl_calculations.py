from django.db.models import Sum
from django.db.models.functions import TruncDate
from .models import Trades

#Function to calculate overview data


#Fucntion to calculate individual day data for the calendar
def calendar_pnl():
    daily_pnl = Trades.objects.annotate(
        date = TruncDate("trade_date")
    ).values("date").annotate(
        total_gross_pnl = Sum("gross_pnl"),
        total_fee = Sum("fee"),
        total_net_pnl = Sum("net_pnl")
    )
    return list(daily_pnl)