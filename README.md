# SQL to Google Sheets

A Python utility to upload CSV data to Google Sheets.

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set up Google Sheets API:
   - Go to [Google Cloud Console](https://console.cloud.google.com/)
   - Create a new project or select an existing one
   - Enable the Google Sheets API
   - Create credentials (OAuth 2.0 Client ID)
   - Download the credentials and save as `credentials.json` in the project root

3. Place your CSV file in the `data/` directory

## Usage

Run the script:
```bash
python upload_to_sheets.py
```

The script will:
1. Create a new Google Sheet
2. Upload your CSV data
3. Print the URL of the created spreadsheet

## Features

- Handles NaN values properly
- Maintains data types (numbers, strings)
- Creates a new spreadsheet for each upload
- OAuth2 authentication with Google Sheets API

## Requirements

See `requirements.txt` for full list of dependencies 