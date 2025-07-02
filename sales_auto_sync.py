# This script will:
#     Load your sales.csv
#     Clean it with pandas
#     Connect to your Google Sheet via API
#     Push the data into the sheet
#     Add a timestamp cell showing the sync time


import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
import numpy as np

# define the scope and credentials:
scope =[
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

creds = ServiceAccountCredentials.from_json_keyfile_name(
    'sales-sync-automation-dbe6b9c8399b.json', 
    scope
)

# authorize the client:
client = gspread.authorize(creds)

# define the Google Sheet name:
mySheet = "Sales Sync Test"

# open the Google Sheet:
sheet = client.open(mySheet).sheet1

# open the csv file":
df = pd.read_csv('sales.csv')

# Clean the column names (strip spaces, capitalize):
df.columns = [col.strip().capitalize() for col in df.columns]

df


# convert date columns to datetime format:
df['Date'] = pd.to_datetime(df['Date'])

#clear the sheet before writing new data:
sheet.clear()

# convert datetime columns to string format for Google Sheets compatibility:
df['Date'] = df['Date'].dt.strftime('%Y-%m-%d')

# update the sheet with the DataFrame:
sheet.update([df.columns.values.tolist()] + df.values.tolist())


# calculate where to place the sync timestamp
last_row = len(df) + 3  # +3 add a few rows for space

#add "Last Synced" label and timestamp
sheet.update_cell(last_row, 1, "Last Synced")
# sheet.update_cell(last_row, 2, datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

# in case we want to add a timezone (eg Lagos time):
from pytz import timezone
lagos_time_now = datetime.now(timezone('Africa/Lagos')).strftime('%Y-%m-%d %H:%M:%S')

# update the timestamp with timezone
sheet.update_cell(last_row, 2, lagos_time_now)

