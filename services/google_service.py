from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from apiclient.http import MediaFileUpload, MediaIoBaseDownload
from google.oauth2 import service_account

import gspread
from oauth2client.service_account import ServiceAccountCredentials
import io
import requests
import pandas as pd
from configs.config import *

class GoogleServiceHandler():
    def __init__(self):
        self.service = GoogleServiceHandler.service_account(path_to_google_drive_service_account_json)
        self.auth_gsr = GoogleServiceHandler.auth_from_gspread(path_to_google_drive_service_account_json)
        self.path_to_download = path_to_download
        self.spreadsheet_id = spreadsheet_id
        self.sheet_name = sheet_name

    @staticmethod
    def credentials_from_file(path_to_service_account_json):

        SCOPES = ['https://www.googleapis.com/auth/drive']
        SERVICE_ACCOUNT_FILE = path_to_service_account_json
        credentials = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
        return credentials

    @staticmethod
    def service_account(path_to_json):

        credentials = GoogleServiceHandler.credentials_from_file(path_to_json)
        version = 'v3'
        service = build('drive', version, credentials=credentials)
        return service

    @staticmethod
    def auth_from_gspread(path_to_service_account_json):
        scope = ['https://spreadsheets.google.com/feeds',
                 'https://www.googleapis.com/auth/drive']

        credentials_gm = ServiceAccountCredentials.from_json_keyfile_name(path_to_service_account_json, scope)
        auth_gsr = gspread.authorize(credentials_gm)
        return auth_gsr

    def docs_downloader_from_drive(self, fileId, mimeType='application/vnd.openxmlformats-officedocument.wordprocessingml.document'):
        request = self.service.files().export_media(fileId=fileId, mimeType=mimeType)

        fh = io.FileIO(os.path.join(path_to_download, 'Task.docx'), 'wb')
        downloader = MediaIoBaseDownload(fh, request)
        done = False
        while done is False:
            status, done = downloader.next_chunk()

    def get_google_sheet_df(self):
        sh = self.auth_gsr.open_by_key(self.spreadsheet_id)
        worksheet = sh.worksheet(self.sheet_name)
        df = pd.DataFrame(worksheet.get_all_records())

        return df, worksheet
