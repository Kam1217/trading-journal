# Trading Journal V1

A Django-based web application for tracking and analyzing trading performance with an interactive calendar view and comprehensive P&L analytics.

## Features
### 📊 Dashboard Overview
- **Real-time P&L Statistics**: Gross P&L, Total Fees, Net P&L, and Total Number of Trades
- **Dynamic Data**: Updates automatically when new trading data is uploaded

### 📅 Interactive Calendar
- **Monthly Calendar View**: Visual representation of daily trading performance
- **Daily P&L**: Each day shows daily net P&L, total fees and number of trades for the day 
- **Dynamic Data**: Updates automatically when new trading data is uploaded
- **Weekly Summaries**: Last column shows weekly performance overview (net P&L, fees, total number of trades)
- **Month Navigation**: Easy browsing between different months

### 📁 CSV Data Import
- **Upload csv file(s)**: Simple file upload interface
- **Multiple File Support**: Upload multiple CSV files simultaneously
- **Data Validation**: Comprehensive validation with detailed error messages
- **Duplicate Handling**: Automatically updates existing trades or creates new ones
- **File Size Limits**: Prevents oversized file uploads (2MB limit)
- **File Type**: Only CSV files accepted

### 🎨 Modern UI/UX
- **Custom made design**: Professional logo, background image and UI/UX design
- **Dark Theme**: Professional dark interface with blur effects
- **Custom Styling**: Quicksand font and Material Design icons
- **Background Support**: Custom background image support

### ‼️Error handling
- **User-friendly Error Messages**: Clear explanations of validation failures
- **File-specific Errors**: Shows which file caused each error
- **Data Type Validation**: Validates numeric and date formats
- **Empty Value Detection**: Prevents processing of incomplete data

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

