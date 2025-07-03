from django import forms
from django.forms import ValidationError
import os

#Create a form which allows the upload of csv files with all trade data

class UploadForm(forms.Form):
    csv_file = forms.FileField()

    #Function that checks if it is a csv file - if not throw an error
    def clean_csv_file(self):
        file = self.cleaned_data.get("csv_file")  
        print(f"File value: {repr(file)}")  # This will show exactly what file is
        print(f"File type: {type(file)}")
        print(f"File is None: {file is None}")
        print(f"File is falsy: {not file}")
        
        if not file:
            print("No file - returning early")
            return file
        
        print("File exists - validating...")
        file_extension = os.path.splitext(file.name)[1].lower()
        if file_extension != '.csv':
            raise ValidationError("File must be a CSV file")
        return file
    
