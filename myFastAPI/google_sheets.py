from googleapiclient.discovery import build
from auth.oauth import authentical_google_sheets

SHEET_ID = '116y__DBKypd3oGp-zrzLjeSWvmeeTdMTc-AFatI3rZs'
RANGE_NAME = "Sheet!A1"

def write_to_google_sheets(data):
    
    service = build('sheets', 'v4', credentials=authentical_google_sheets())
    sheet = service.spreadsheets()


    values = [
        [
            data["store_name"],
            data["store_location"],
            data["date"],
            ', '.join([f"{prod['name']} ({prod['quantity']} x {prod['price']})" for prod in data["products"]])

        ]
    ]

    body = {
        'values': values
    }

    result = sheet.values().append(
        spreadsheetID = SHEET_ID,
        range=RANGE_NAME,
        valueInputOption="RAW",
        body=body
    ).execute()

    return result