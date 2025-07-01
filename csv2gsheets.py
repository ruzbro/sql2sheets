import pandas as pd
import numpy as np
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import os.path
import pickle

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

def get_google_sheets_credentials():
    creds = None
    # The file token.pickle stores the user's access and refresh tokens
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'ggAPIcredentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    return creds

def clean_value(val):
    if pd.isna(val):  # Check for NaN values
        return ""
    if isinstance(val, (int, float)):
        return val
    return str(val)

def upload_to_sheets():
    # Read the CSV file
    df = pd.read_csv('data/PNQ Farm Crop Performance 2025wk10-27.csv')
    
    # Get Google Sheets credentials
    creds = get_google_sheets_credentials()
    service = build('sheets', 'v4', credentials=creds)

    # Create a new spreadsheet
    spreadsheet = {
        'properties': {
            'title': 'PNQ Farm Crop Performance 2025wk10-27'
        }
    }
    spreadsheet = service.spreadsheets().create(body=spreadsheet).execute()
    spreadsheet_id = spreadsheet['spreadsheetId']
    
    # Convert dataframe to values list, cleaning the data
    headers = df.columns.tolist()
    values = [headers]
    
    for _, row in df.iterrows():
        cleaned_row = [clean_value(val) for val in row]
        values.append(cleaned_row)
    
    # Prepare the request body
    body = {
        'values': values
    }
    
    # Update the spreadsheet with the data
    result = service.spreadsheets().values().update(
        spreadsheetId=spreadsheet_id,
        range='A1',
        valueInputOption='RAW',
        body=body
    ).execute()
    
    print(f'Spreadsheet created successfully! ID: {spreadsheet_id}')
    print(f'URL: https://docs.google.com/spreadsheets/d/{spreadsheet_id}')

if __name__ == '__main__':
    upload_to_sheets() 