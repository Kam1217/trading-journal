from django.test import TestCase
import os
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from .handle_csv_upload import handle_upload_csv
from .forms import UploadForm
from .models import Trade
from datetime import date
from .pnl_calculations import overview_pnl, calendar_daily_pnl, calendar_weekly_pnl

# Create your tests here.

class CsvUploadTestCase(TestCase):

    #Test for POST request
    def test_csv_file_post_request(self):
        file_content = (
            "Date/Time,Gross P/L,Fee,Net P/L,Trade ID,Other Column\n"
            "01/01/2023 10:00:00 +0000,100,5.00,95.00,TRADE123,Extra\n"
            "02/01/2023 11:00:00 +0000,-50,2.00,-52.00,TRADE456,Another"
        ).encode("utf-8")
        uploaded_file = SimpleUploadedFile("test.csv", file_content, content_type="text/csv")
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
        self.assertIn("File must be a CSV file", str(form.errors["csv_file"]))
   
    #Test csv file does not throw an error
    def test_csv_upload_succeds(self):
        file_content = (
            "Date/Time,Gross P/L,Fee,Net P/L,Trade ID,Other Column\n"
            "01/01/2023 10:00:00 +0000,100.00,5.00,95.00,TRADE123,Extra\n"
            "02/01/2023 11:00:00 +0000,-50,2.00,-52.00,TRADE456,Another"
        ).encode('utf-8')
        csv_file = SimpleUploadedFile("test.csv", file_content, content_type="text/csv")
        form = UploadForm(files={"csv_file": csv_file})
        self.assertTrue(form.is_valid())
   
    #Test no file uploaded 
    def test_no_file_upload_fails(self):
        form = UploadForm(files={})
        self.assertFalse(form.is_valid())
        self.assertIn("This field is required", str(form.errors["csv_file"]))

    #Test file size 
    def test_large_file_upload_fail(self):
        large_content = "Date/Time,Gross P/L,Fee,Net P/L,Trade ID\n" + ("01/01/2023 10:00:00 +0000,100,5.00,95.00,TRADE123\n" * 100000)
        large_file = SimpleUploadedFile("large.csv", large_content.encode("utf-8"), content_type="text/csv")

        with self.assertRaises(ValueError) as context:
            handle_upload_csv(large_file)
        
        self.assertIn("File too large", str(context.exception))

    def test_file_within_size_succeds(self):
        file_content = (
            "Date/Time,Gross P/L,Fee,Net P/L,Trade ID\n"
            "01/01/2023 10:00:00 +0000,100.00,5.00,95.00,TRADE123\n"
        ).encode("utf-8")
        csv_file = SimpleUploadedFile("test.csv", file_content, content_type="text/csv")

        try:
            handle_upload_csv(csv_file)
        except ValueError as e:
            if "File too large" in str(e):
                self.fail("Valid sized file failed to upload")
    
    #Test wrong csv format - Missing header
    def test_missing_header(self):
        file_content = (
            "Date/Time,Gross P/L,Fee,Trade ID\n"
            "01/01/2023 10:00:00 +0000,100.00,5.00,95.00,TRADE123\n"
        ).encode("utf-8")
        csv_file = SimpleUploadedFile("test.csv", file_content, content_type="text/csv")

        with self.assertRaises(ValueError) as context:
            handle_upload_csv(csv_file)

        self.assertIn("Missing required header in CSV row", str(context.exception))
    
    #Test wrong csv format - invalid numeric value
    def test_invalid_numeric_value(self):
        file_content = (
            "Date/Time,Gross P/L,Fee,Net P/L,Trade ID\n"
            "01/01/2023 10:00:00 +0000,not_a_number,5.00,95.00,TRADE123\n"
        ).encode("utf-8")
        csv_file = SimpleUploadedFile("test.csv", file_content, content_type="text/csv")

        with self.assertRaises(ValueError) as context:
            handle_upload_csv(csv_file)

        self.assertIn("Invalid numeric value in row",str(context.exception))

class PNLCalculationsTestCase(TestCase):
    def setUp(self):
        Trade.objects.create( 
            trade_date = date(2025, 4, 1),
            gross_pnl = 100,
            fee = 1.2,
            net_pnl = 98.8,
            trade_id = "SOMEID1",
        )
        Trade.objects.create(
            trade_date = date(2025,4,2),
            gross_pnl = -100,
            fee = 3.0,
            net_pnl = -103,
            trade_id = "SOMEID2",
        )
        Trade.objects.create(
            trade_date = date(2025,4,3),
            gross_pnl = 200,
            fee = 3.0,
            net_pnl = 197,
            trade_id = "SOMEID3",
        )

        Trade.objects.create(
            trade_date = date(2025,12,17),
            gross_pnl = 500,
            fee = 3.0,
            net_pnl = 497,
            trade_id = "SOMEID4",
        )

    def test_overview_pnl(self):
        result = overview_pnl()
        expected_gross_pnl = 100 + -100 + 200 + 500 #700
        expected_fee = 1.2 + 3 + 3 + 3 #10.2
        expectd_net_pnl = 98.8 + -103 + 197 + 497 #689.8
        expectd_num_trades = 4

        self.assertEqual(result["total_gross_pnl"], expected_gross_pnl)
        self.assertEqual(result["total_fee"], expected_fee)
        self.assertEqual(result["total_net_pnl"], expectd_net_pnl)
        self.assertEqual(result["number_of_trades"], expectd_num_trades)

    def test_daily_pnl(self):
        result = calendar_daily_pnl()
        
        april_first_data = next((item for item in result if item["day"] == date(2025, 4, 1)), None)
        self.assertIsNotNone(april_first_data)
        self.assertEqual(april_first_data["total_fee"], 1.2)
        self.assertEqual(april_first_data["total_net_pnl"], 98.8)
        self.assertEqual(april_first_data["number_of_trades"], 1)

        april_second_data = next((item for item in result if item["day"] == date(2025,4,2)), None)
        self.assertIsNotNone(april_second_data)
        self.assertEqual(april_second_data["total_fee"], 3.0)
        self.assertEqual(april_second_data["total_net_pnl"], -103)
        self.assertEqual(april_second_data["number_of_trades"], 1)

        april_third_data = next((item for item in result if item["day"] == date(2025,4,3)), None)
        self.assertIsNotNone(april_third_data)
        self.assertEqual(april_third_data["total_fee"], 3.0)
        self.assertEqual(april_third_data["total_net_pnl"], 197)
        self.assertEqual(april_third_data["number_of_trades"], 1)

        december_seventeenth_data = next((item for item in result if item["day"] == date(2025,12,17)), None)
        self.assertIsNotNone(december_seventeenth_data)
        self.assertEqual(december_seventeenth_data["total_fee"], 3.0)
        self.assertEqual(december_seventeenth_data["total_net_pnl"], 497)
        self.assertEqual(december_seventeenth_data["number_of_trades"], 1)

    def test_weekly_pnl(self):
        result = calendar_weekly_pnl()
        print(f"\nDEBUG: weekly_pnl() returned: {result}")


        first_week_data = next((item for item in result if item["week"].date() == date(2025, 3, 31)), None)
        self.assertIsNotNone(first_week_data)
        self.assertEqual(first_week_data["total_fee"], 1.2 + 3.0 + 3.0)
        self.assertEqual(first_week_data["total_net_pnl"], 98.8 + -103.0 + 197.0)
        self.assertEqual(first_week_data["number_of_trades"], 3)

        second_week_data = next((item for item in result if item["week"].date() == date(2025, 12, 15)), None)
        self.assertIsNotNone(second_week_data)
        self.assertIsNotNone(second_week_data)
        self.assertEqual(second_week_data["total_fee"], 3.0)
        self.assertEqual(second_week_data["total_net_pnl"], 497.0)
        self.assertEqual(second_week_data["number_of_trades"], 1)

     