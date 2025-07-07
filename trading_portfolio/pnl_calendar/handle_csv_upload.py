import csv
from datetime import datetime
import uuid
import os
from .models import Trade

def save_uploaded_csv(f):
    #Make a unique name for each file about to me uploaded
    unique_csv_id = uuid.uuid4().hex 
    name, ext = os.path.splitext(f.name)
    unique_csv_name = f"{unique_csv_id}_{name}{ext}"
    file_path = f"pnl_calendar/trades_csv/{unique_csv_name}"

    #Open and save the uploaded csv file to trades_csv folder   
    with open(file_path, "wb+") as destination:
        for chunk in f.chunks():
            destination.write(chunk)
    
    return file_path

#Function which checks all rows have valid data
def validate_csv_data(row, row_num, required_fields):
    #Missing/ No value
    for field in required_fields:
        value = row.get(field, "").strip()
        if not value:
            raise ValueError(f"Missing or empty value for '{field}' in row {row_num}")
        
    


def process_csv_to_trades(csv_file_path):
    #Get required csv data for the Trade model
    desired_keys = {"Date/Time": "trade_date", "Gross P/L": "gross_pnl", "Fee": "fee", "Net P/L": "net_pnl", "Trade ID": "trade_id"}

    #Count newly addes trades and updated trades
    new_trade_obj_count = 0
    updated_trade_obj_count = 0

    with open(csv_file_path, mode= "r") as file:
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
                defaults={
                    "trade_date": filtered_row["trade_date"],
                    "gross_pnl": filtered_row["gross_pnl"],
                    "fee": filtered_row["fee"],
                    "net_pnl": filtered_row["net_pnl"],
                }
            )

        if created:
            print(f"Successfully added new trade with ID: {trade_obj.trade_id}")
            new_trade_obj_count += 1
        else:
            print(f"Trade with ID: {trade_obj.trade_id} already exists and has been updated")
            updated_trade_obj_count += 1

        return new_trade_obj_count, updated_trade_obj_count


def handle_upload_csv(f):
    csv_file_path = save_uploaded_csv(f)

    try:
        new_count, updated_count = process_csv_to_trades(csv_file_path)
        print(f"Processing complete: {new_count} new trades, {updated_count} updated trades")
    
    #Remove csv once it is done processing
    finally:
        if os.path.exists(csv_file_path):
            os.remove(csv_file_path)



