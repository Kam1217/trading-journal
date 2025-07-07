import csv
from datetime import datetime
import uuid
import os
from .models import Trade

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
    
    #Get required csv data for the Trade model
    desired_keys = {"Date/Time": "trade_date", "Gross P/L": "gross_pnl", "Fee": "fee", "Net P/L": "net_pnl", "Trade ID": "trade_id"}

    with open(f"pnl_calendar/trades_csv/{unique_csv_name}", mode= "r") as file:
        csv_file = csv.DictReader(file)

        #Raise error if required keys are missing in the CSV file 
        required_fields = desired_keys.keys()
        for field in required_fields:
            if field not in csv_file.fieldnames:
                raise ValueError(f"Missing required header in CSV row: {field}")

        #Filter each row to desired headers
        for row in csv_file:
            filtered_row = {desired_keys[key]: row[key] for key in desired_keys.keys() if key in row} 

            #Convert date to correct model format for Trade model

            date_obj = datetime.strptime(filtered_row["trade_date"], "%d/%m/%Y %H:%M:%S %z")
            filtered_row["trade_date"] = date_obj.strftime("%Y-%m-%d %H:%M:%S%z")

            #Handle duplicates
            trade_obj, created = Trade.objects.update_or_create(
                trade_id = filtered_row["trade_id"],
                defaults= {
                    "trade_date": filtered_row["trade_date"],
                    "gross_pnl": filtered_row["gross_pnl"],
                    "fee": filtered_row["fee"],
                    "net_pnl": filtered_row["net_pnl"],
                }
            )

            #Count newly addes trades and updated trades
            new_trade_obj_count = 0
            updated_trade_obj_count = 0

            if created:
                print(f"Successfully added new trade with ID: {trade_obj.trade_id}")
                new_trade_obj_count += 1

            else:
                print(f"Trade with ID: {trade_obj.trade_id} already exists and has been updated")
                updated_trade_obj_count += 1

    #Remove csv once it is done processing
    csv_file_path = f"pnl_calendar/trades_csv/{unique_csv_name}"
    os.remove(csv_file_path)


