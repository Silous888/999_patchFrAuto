from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from google.oauth2 import service_account as sc
from credentials import credentials_info
import io
import os

dossier_telechargement = "./ZE999Tool.v0.9.8.1/sir_patched"


credentials = sc.Credentials.from_service_account_info(credentials_info, scopes=['https://www.googleapis.com/auth/drive'])

drive_service = build('drive', 'v3', credentials=credentials)


def download_file(file_id, file_name, download_folder):
    file_path = os.path.join(download_folder, file_name)
    request = drive_service.files().get_media(fileId=file_id)
    fh = io.FileIO(file_path, mode='wb')
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while not done:
        status, done = downloader.next_chunk()


def download_files_in_folder(folder_id):
    results = drive_service.files().list(
        q=f"'{folder_id}' in parents and trashed=false",
        fields='files(id, name, mimeType)'
    ).execute()
    files = results.get('files', [])
    for file in files:
        if file['mimeType'] == 'application/vnd.google-apps.folder':
            download_files_in_folder(file['id'])
        else:
            download_file(file['id'], file['name'], dossier_telechargement)
