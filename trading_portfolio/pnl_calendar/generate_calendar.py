from datetime import datetime, date
import calendar

def generate_calendar(daily_data, weekly_data, year, month):
    
    cal = calendar.monthcalendar(year, month)
    
    daily_dict = {}
    for day_data in daily_data:
        day_date = day_data['day'] 
        if day_date.year == year and day_date.month == month:
            daily_dict[day_date.day] = {
                "net_pnl": float(day_data["total_net_pnl"]) if day_data["total_net_pnl"] else 0,
                "fees": float(day_data["total_fee"]) if day_data["total_fee"] else 0,
                "trade_count": day_data["number_of_trades"],
            }

    def get_pnl_type(net_pnl):
        if net_pnl > 0:
            return "positive"
        elif net_pnl < 0:
            return "negative"
        else:
            return "neutral"
   
    weekly_dict = {}
    for week_data in weekly_data:
        week_start = week_data["week"]  
        if week_start.year == year and week_start.month == month:
            weekly_dict[week_start] = {
                "net_pnl": float(week_data["total_net_pnl"]) if week_data["total_net_pnl"] else 0,
                "fees": float(week_data["total_fee"]) if week_data["total_fee"] else 0,
                "trade_count": week_data["number_of_trades"],
            }
    
    calendar_weeks = []
    for week_index, week in enumerate(cal):
        week_data = []
        week_totals = {"net_pnl": 0, "fees": 0, "trades": 0}
        
        for day in week:
            if day == 0:  
                day_data = {
                    "day": "",
                    "date": None,
                    "net_pnl": 0,
                    "fees": 0,
                    "trade_count": 0,
                    "has_trades": False,
                    "is_empty": True
                }
            else:
                current_date = date(year, month, day)
                trade_data = daily_dict.get(day, {"net_pnl": 0, "fees": 0, "trade_count": 0})
                
                day_data = {
                    "day": day,
                    "date": current_date,
                    "net_pnl": trade_data["net_pnl"],
                    "fees": trade_data["fees"],
                    "trade_count": trade_data["trade_count"],
                    'has_trades': trade_data["trade_count"] > 0,
                    "is_empty": False,
                    "pnl_type": get_pnl_type(trade_data['net_pnl'])
                }
                
                week_totals["net_pnl"] += trade_data["net_pnl"]
                week_totals["fees"] += trade_data["fees"]
                week_totals["trades"] += trade_data["trade_count"]
            
            week_data.append(day_data)
        
        week_data.append({
            "is_week_summary": True,
            "week_number" : week_index + 1,
            "net_pnl": week_totals["net_pnl"],
            "fees": week_totals["fees"],
            "trade_count": week_totals["trades"],
        })
        
        calendar_weeks.append(week_data)
    
    return calendar_weeks