import csv
from datetime import datetime
import uuid
import os
from .models import Trades

#Upload and save csv file to a folder
def handle_upload_csv(f):
    #Make a unique name for each file about to me uploaded
    unique_csv_id = uuid.uuid4().hex 
    name, ext = os.path.splitext(f.name)
    unique_csv_name = f"{unique_csv_id}_{name}{ext}"
    
    #Open and save the uploaded csv file to trades_csv folder   
    with open(f"pnl_calendar/trades_csv/{unique_csv_name}", "wb+") as destination:
        for chunk in f.chunks():
            destination.write(chunk)
    
    #Get required csv data for the Trades model
    desired_keys = {"Date/Time": "trade_date", "Gross P/L": "gross_pnl", "Fee": "fee", "Net P/L": "net_pnl", "Trade ID": "trade_id"}

    with open(f"pnl_calendar/trades_csv/{unique_csv_name}", mode= "r") as file:
        csv_file = csv.DictReader(file)

        #Filter each row to desired headers
        for row in csv_file:
            filtered_row = {desired_keys[key]: row[key] for key in desired_keys.keys() if key in row} 
            required_fields = desired_keys.values()

            #Raise error if required keys are missing in the CSV file
            for field in required_fields:
                if field not in filtered_row:
                    raise ValueError(f"Missing required header in CSV row: {field}. Rows: {row}")

            #Convert date to correct model format for Trades model
            date_obj = datetime.strptime(filtered_row["trade_date"], "%d/%m/%Y %H:%M:%S %z")
            filtered_row["trade_date"] = date_obj.strftime("%Y-%m-%d %H:%M:%S%z")
            
            #Save to data to Trades model
            trades = Trades(**filtered_row)
            trades.save()

