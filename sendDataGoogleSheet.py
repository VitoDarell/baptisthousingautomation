import csv
import os.path
import os
from dotenv import load_dotenv

from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

load_dotenv()

print("Sending data to Google Sheets")
# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

# The ID of your spreadsheet.
SPREADSHEET_ID = os.getenv("SPREADSHEET_ID")  # Replace with spreadsheet ID
SHEET_NAME = "completedUsers" #Replace with sheet name.
SERVICE_ACCOUNT_FILE = os.getenv("GOOGLE_API_TOKEN")

def send_csv_to_sheets(csv_file_path, spreadsheet_id, sheet_name, service_account_file):
    try:
        creds = service_account.Credentials.from_service_account_file(
            service_account_file, scopes=SCOPES
        )
        service = build("sheets", "v4", credentials=creds)

        with open(csv_file_path, "r", newline="", encoding="utf-8") as csvfile:
            reader = csv.reader(csvfile)
            values = list(reader)

        body = {"values": values}

        # Clear the sheet before writing the new data (optional but recommended).
        clear_body = {}
        clear_result = (
            service.spreadsheets()
            .values()
            .clear(spreadsheetId=spreadsheet_id, range=sheet_name, body=clear_body)
            .execute()
        )

        result = (
            service.spreadsheets()
            .values()
            .update(
                spreadsheetId=spreadsheet_id,
                range=sheet_name,
                valueInputOption="RAW",
                body=body,
            )
            .execute()
        )

        print(f"{result.get('updatedCells')} cells updated.")
        os.remove("downloads/completedUserTemp.csv")

    except HttpError as err:
        print(f"An error occurred: {err}")

csv_file = "downloads/completedUserTemp.csv"  # Replace with your csv filepath.
send_csv_to_sheets(csv_file, SPREADSHEET_ID, SHEET_NAME, SERVICE_ACCOUNT_FILE)