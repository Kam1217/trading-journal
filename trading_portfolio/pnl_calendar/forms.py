from django import forms
from django.forms import ValidationError
import os

#Create a form which allows the upload of csv files with all trade data

class UploadForm(forms.Form):
    csv_file = forms.FileField()

    #Function that checks if it is a csv file - if not throw an error
    def clean_csv_file(self):
        file = self.cleaned_data.get("csv_file")  
        if not file:
            return file
        file_extension = os.path.splitext(file.name)[1].lower()
        if file_extension != '.csv':
            raise ValidationError("File must be a CSV file")
        return file
    
