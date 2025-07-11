# Trading Journal V1

A Django-based web application for tracking and analyzing trading performance with an interactive calendar view and comprehensive P&L analytics.
<img width="1918" height="947" alt="image" src="https://github.com/user-attachments/assets/ef694043-d78b-46da-9597-615031d73dfc" />

## Features
### 📊 Dashboard Overview
- **Real-time P&L Statistics**: Gross P&L, Total Fees, Net P&L, and Total Number of Trades
- **Dynamic Data**: Updates automatically when new trading data is uploaded
<img width="1694" height="139" alt="image" src="https://github.com/user-attachments/assets/14fc2bd1-969c-4f32-b06f-f4c44bb41f26" />

### 📅 Interactive Calendar
- **Monthly Calendar View**: Visual representation of daily trading performance
- **Daily P&L**: Each day shows daily net P&L, total fees and number of trades for the day 
- **Dynamic Data**: Updates automatically when new trading data is uploaded
- **Weekly Summaries**: Last column shows weekly performance overview (net P&L, fees, total number of trades)
- **Month Navigation**: Easy browsing between different months
<img width="1696" height="748" alt="image" src="https://github.com/user-attachments/assets/d93ef6ff-4167-422c-aad5-c4fda9ba3536" />

### 📁 CSV Data Import
- **Upload csv file(s)**: Simple file upload interface
- **Multiple File Support**: Upload multiple CSV files simultaneously
- **Data Validation**: Comprehensive validation with detailed error messages
- **Duplicate Handling**: Automatically updates existing trades or creates new ones
- **File Size Limits**: Prevents oversized file uploads (2MB limit)
- **File Type**: Only CSV files accepted
<img width="283" height="53" alt="image" src="https://github.com/user-attachments/assets/653f167a-6c5e-4517-9630-c0750be9b6ae" />
<img width="768" height="144" alt="image" src="https://github.com/user-attachments/assets/cff14100-1d5b-44dd-b1ed-68e95428bc0c" />

### ‼️Error handling
- **User-friendly Error Messages**: Clear explanations of validation failures
- **File-specific Errors**: Shows which file caused each error
- **Data Type Validation**: Validates numeric and date formats
- **Empty Value Detection**: Prevents processing of incomplete data
<img width="962" height="58" alt="image" src="https://github.com/user-attachments/assets/84b1c55f-eb27-4f74-8652-dace2fb51d45" />

### 🎨 Modern UI/UX
- **Custom made design**: Professional logo, background image and UI/UX design
- **Dark Theme**: Professional dark interface with blur effects
- **Custom Styling**: Quicksand font and Material Design icons
- **Background Support**: Custom background image support
<img width="197" height="201" alt="image" src="https://github.com/user-attachments/assets/5e4d7bde-c4a0-4ba2-aff9-2ec3be9b2048" />
<img width="1296" height="642" alt="image" src="https://github.com/user-attachments/assets/56280e82-cb00-4206-9fb9-05d4af0904a5" />
<img width="591" height="442" alt="image" src="https://github.com/user-attachments/assets/4c8c1e3b-4799-41fe-9c12-f43182a8b0bd" />

## Technology Stack
- **Backend**: Django 4.x
- **Frontend**: HTML5, CSS3
- **Database**: SQLite (default)
- **Styling**: Custom CSS with Quicksand Google Font
- **Icons**: Material Symbols by Google
- **File Processing**: Python CSV library with custom validation

### Prerequisites
- Python 3.8+
- pip
- virtualenv (recommended)

### Setup Instructions
**Clone the repository**
   ```bash
   git clone <repository-url>
   cd trading-journal
```
**Navigate to project directory**
   ```bash
   cd trading-journal
```
**Create virtual environment**
   ```bash
   python -m venv trading_env
```
**Install dependencies**
   ```bash
   pip install -r requirements.txt
```
**Set up database**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
```
**Create superuser (optional)**
   ```bash
   python manage.py createsuperuser
```
**Run the development server**
   ```bash
  cd trading_portfolio
  python manage.py runserver
```
**Access the application**
- Open your browser and access the aplication

**Upload CSV file(s)**
- Upload csv file(s) using the "choose files" and "upload" button to see trading data

### CSV File format
It is very important that this csv format is followed (follows and supports the current Quantower csv format):
  | Date/Time | Gross P/L | Fee | Net P/L | Trade ID |
  |-----------|-----------|-----|---------|----------|
  |01/01/2024 10:30:00 +0000 |150.25|2.50 |147.75|TRADE001|
  |02/01/2024 14:15:00 +0000 |-75.00|1.75|-76.75|TRADE002| 

### Final Steps
- Upload your trading CSV files
- Navigate through different months using the calendar
- View your P&L analytics on the dashboard

### Extras:
**Customize the background image and styling as needed (optional)**
- Place your logo in static/images/
- Place your background image in static/images/
- Make sure you name your logo image "logo.svg"
- Makes sure you name your background image "background.png"
- Or update the CSS file to match your logo/image name

