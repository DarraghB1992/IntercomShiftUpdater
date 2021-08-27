import os
import json
import datetime as dt
import requests
from google.oauth2 import service_account
from googleapiclient.discovery import build

# Google Sheets Setup
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SERVICE_ACCOUNT_FILE = 'token.json'
credentials = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
SPREADSHEET_ID = os.environ.get('SpreadsheetID')
service = build('sheets', 'v4', credentials=credentials)
sheet = service.spreadsheets()

# Intercom Setup
AccessToken = os.environ.get('AccessToken')
IntercomUrl = 'https://api.intercom.io/admins'
headers = {
    'Authorization': 'Bearer ' + AccessToken,
    'Accept': 'application/json',
    'Content-Type': 'application/json'
}


def get_shift_information():
    google_sheet = sheet.values().get(spreadsheetId=SPREADSHEET_ID, range='Hours!A2:Z100').execute()
    admin_info = google_sheet['values']
    for admin in admin_info:
        admin_id = admin[2]
        admin_start_hour = int(admin[3])
        admin_finish_hour = int(admin[4])
        check_hours(admin_start_hour, admin_finish_hour, admin_id)


def check_hours(admin_start_hour, admin_finish_hour, admin_id):
    current_hour = dt.datetime.now().hour
    print(current_hour)
    if current_hour in range(admin_start_hour, admin_finish_hour):
        set_admin_as_online(admin_id)
    else:
        set_admin_as_away(admin_id)


def set_admin_as_online(admin_id):
    set_online_params = {
        'away_mode_enabled': False,
        'away_mode_reassign': False,
    }
    print('Setting teammate online')
    update_admin_status(admin_id, set_online_params)


def set_admin_as_away(admin_id):
    set_offline_params = {
        'away_mode_enabled': True,
        'away_mode_reassign': True,
    }
    print('Setting teammate away and reassigning conversations')
    update_admin_status(admin_id, set_offline_params)


def update_admin_status(admin_id, params):
    r = requests.put(IntercomUrl + '/' + admin_id + '/away', headers=headers, json=params)
    print(r.status_code)
    print(r.headers)
    print(r.text)


# Can be called for setup purposes.
def get_admin_ids():
    r = requests.get(IntercomUrl, headers=headers)
    admin_json = json.loads(r.text)
    admins = admin_json['admins']
    print(admins)


if __name__ == '__main__':
    get_shift_information()
