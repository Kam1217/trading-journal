import uuid
import os
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