from django.test import TestCase
import os
from django.core.files.uploadedfile import SimpleUploadedFile
from .handle_csv_upload import handle_upload_csv

# Create your tests here.

class CsvUploadTestCase(TestCase):
    #Test file uploads and saves to the correct folder
    def test_csv_file_upload(self):
        file_content = b"header1,header2\nvalue1,value2"
        uploaded_file = SimpleUploadedFile('test.csv', file_content, content_type='text/csv')
        expected_file_path = os.path.join("pnl_calendar", "trades_csv", "test.csv")
        handle_upload_csv(uploaded_file)
        self.assertTrue(os.path.exists(expected_file_path))

        if os.path.exists(expected_file_path):
            os.remove(expected_file_path)