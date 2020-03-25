from oauth2client.service_account import ServiceAccountCredentials
import gspread

def get_sheet(sheetname):
    # use creds to create a client to interact with the Google Drive API
    scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']

    creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
    print(creds)
    print(type(creds))
    # print(creds)
    client = gspread.authorize(creds)
    # Find a workbook by name and open the first sheet
    # Make sure you use the right name here.
    sheet = client.open(sheetname).sheet1
    return sheet
