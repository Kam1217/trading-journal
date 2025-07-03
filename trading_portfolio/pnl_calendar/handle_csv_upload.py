#Upload and save csv file to a folder

def handle_upload_csv(f):
    with open("pnl_calendar/trades_csv/"+f.name,"wb+") as destination:
        for chunk in f.chunks():
            destination.write(chunk)
