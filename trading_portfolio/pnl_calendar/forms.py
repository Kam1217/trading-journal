from django import forms
from django.forms import ValidationError
import os

#Create a form which allows the upload of csv files with all trade data

class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True

class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput(attrs={
            'accept': '.csv',
            'class': 'file-input',
            'id': 'csv-file-input'
        }))
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        if isinstance(data, (list, tuple)):
            result = [self.__clean_csv_file(d, initial) for d in data]
        else:
            result = [self.__clean_csv_file(data, initial)]
        return result
    
    #Function that checks if it is a csv file - if not throw an error
    def __clean_csv_file(self, data, initial):
        single_file_clean = super().clean
        file = single_file_clean(data, initial)  
        if not file:
            return file
        file_extension = os.path.splitext(file.name)[1].lower()
        if file_extension != '.csv':
            raise ValidationError("File must be a CSV file")
        return file

class UploadForm(forms.Form):
    csv_file = MultipleFileField(label="")


    
