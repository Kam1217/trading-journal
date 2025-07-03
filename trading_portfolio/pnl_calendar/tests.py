from django.test import TestCase
import os
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from .handle_csv_upload import handle_upload_csv
from .forms import UploadForm

# Create your tests here.

class CsvUploadTestCase(TestCase):
    #Test file uploads and saves to the correct folder
    def test_csv_uploads_to_correct_folder(self):
        file_content = b"header1,header2\nvalue1,value2"
        uploaded_file = SimpleUploadedFile('test.csv', file_content, content_type='text/csv')
        expected_file_path = os.path.join("pnl_calendar", "trades_csv", "test.csv")
        handle_upload_csv(uploaded_file)
        self.assertTrue(os.path.exists(expected_file_path))

        if os.path.exists(expected_file_path):
            os.remove(expected_file_path)

    #Test for POST request
    def test_csv_file_post_request(self):
        file_content = b"header1,header2\nvalue1,value2"
        uploaded_file = SimpleUploadedFile('test.csv', file_content, content_type='text/csv')
        response = self.client.post(
            reverse("pnl_calendar"),
            data = {},
            FILES = {"csv_file": uploaded_file},
        )
        self.assertEqual(response.status_code, 200)

    #Test non csv files throw an error
    def test_non_csv_upload_fails(self):
        txt_content = b"This is not a CSV file"
        txt_file = SimpleUploadedFile("test.txt", txt_content, content_type="text/plain")
        form = UploadForm(files={"csv_file": txt_file})
        self.assertFalse(form.is_valid())
        self.assertIn('File must be a CSV file', str(form.errors['csv_file']))
   
    #Test csv file does not throw an error
    def test_csv_upload_succeds(self):
        csv_content = b"name,age,city\nJohn,25,NYC\nJane,30,LA"
        csv_file = SimpleUploadedFile("test.csv", csv_content, content_type="text/csv")
        form = UploadForm(files={"csv_file": csv_file})
        self.assertTrue(form.is_valid())
   
    #Test no file uploaded 