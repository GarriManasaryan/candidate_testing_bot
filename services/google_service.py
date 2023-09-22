# google sheets
from googleapiclient.discovery import build
from apiclient.http import MediaFileUpload, MediaIoBaseDownload
from google.oauth2 import service_account
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# email
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib

import io
import requests
import pandas as pd
from apiclient.http import MediaFileUpload, MediaIoBaseDownload
from google.oauth2 import service_account
from googleapiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials

from configs.config import *


class GoogleServiceHandler:
    def __init__(self):
        self.service = GoogleServiceHandler.generate_service(
            path_to_google_drive_service_account_json
        )
        self.auth_gsr = GoogleServiceHandler.auth_from_gspread(
            path_to_google_drive_service_account_json
        )
        self.path_to_download = path_to_download
        self.spreadsheet_id = spreadsheet_id
        self.sheet_name = sheet_name
        self.docx_mimetype = (
            "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )
        self.excel_mimetype = (
            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

    @staticmethod
    def generate_service(path_to_json):
        scopes = ["https://www.googleapis.com/auth/drive"]
        credentials = service_account.Credentials.from_service_account_file(
            path_to_json, scopes=scopes
        )

        version = "v3"
        service = build("drive", version, credentials=credentials)
        return service

    @staticmethod
    def auth_from_gspread(path_to_service_account_json):
        scope = [
            "https://spreadsheets.google.com/feeds",
            "https://www.googleapis.com/auth/drive",
        ]

        credentials = ServiceAccountCredentials.from_json_keyfile_name(
            path_to_service_account_json, scope
        )
        auth_gsr = gspread.authorize(credentials)
        return auth_gsr

    def file_downloader_from_drive(self, file_name, file_id, file_type):
        if file_type == 'xlsx':
            mimeType = self.excel_mimetype
        elif file_type == 'docx':
            mimeType = self.docx_mimetype

        request = self.service.files().export_media(
            fileId=file_id, mimeType=mimeType
        )

        fh = io.FileIO(os.path.join(path_to_download, file_name), "wb")
        downloader = MediaIoBaseDownload(fh, request)
        done = False
        while done is False:
            status, done = downloader.next_chunk()

    def get_google_sheet_df(self):
        sh = self.auth_gsr.open_by_key(self.spreadsheet_id)
        worksheet = sh.worksheet(self.sheet_name)
        df = pd.DataFrame(worksheet.get_all_records())

        return df, worksheet

    def create_google_folder(self, parent_folder_id, folder_name):
        file_metadata = {
            "name": folder_name,
            "mimeType": "application/vnd.google-apps.folder",
            "parents": [parent_folder_id],
        }

        return self.service.files().create(body=file_metadata, fields="id").execute()

    def add_file_to_google_folder(
        self, parent_folder_id, file_name, file_full_path, file_type
    ):
        file_metadata = {"name": file_name, "parents": [parent_folder_id]}

        if file_type == "docx":
            mimetype = self.docx_mimetype

        elif file_type == "excel":
            mimetype = self.excel_mimetype

        media = MediaFileUpload(file_full_path, mimetype=mimetype)

        return (
            self.service.files().create(body=file_metadata, media_body=media).execute()
        )

    def update_row(self, worksheet, list_of_values, row_num):
        worksheet.update(f"{row_num}:{row_num}", [list_of_values])

    def send_email_confirmation(self, destination_email, subject, body):
        # prepare message with subject and body
        message = MIMEMultipart()
        message["from"] = email_from
        message["to"] = destination_email
        message["subject"] = subject
        message.attach(MIMEText(body))

        with smtplib.SMTP(host="smtp.gmail.com", port=587) as smtp:
            smtp.ehlo()
            smtp.starttls()
            smtp.login(source_email, email_password)
            smtp.send_message(message)