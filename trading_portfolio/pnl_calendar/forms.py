from django import forms

#Create a form which allows the upload of csv files with all trade data

class UploadForm(forms.Form):
    csv_file = forms.FileField()

    #Function that checks if it is a csv file - if not throw an error