import subprocess
import os
import io
import time

from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from google.oauth2 import service_account

from steam import trouver_bin_zero_escape
from credentials import credentials_info

path_xdelta = "ZE999Tool.v0.9.8.1\\xDeltaPatch\\"


credentials = service_account.Credentials.from_service_account_info(credentials_info,
                                                                    scopes=['https://www.googleapis.com/auth/drive'])

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
            download_file(file['id'], file['name'], path_xdelta)


def creer_patch(nom_exe, original=False):
    """_summary_

    Args:
        nom_exe (_type_): _description_
    """
    chemin_bin_steam = os.path.dirname(trouver_bin_zero_escape())

    path_exe_original = chemin_bin_steam + "\\" + nom_exe + ".exe"
    path_exe_patche = chemin_bin_steam + "\\" + nom_exe + "_new.exe"

    path_exe1 = path_exe_original
    path_exe2 = path_exe_patche
    if original:
        nom_exe = nom_exe + "_original"
        path_exe1 = path_exe_patche
        path_exe2 = path_exe_original

    commande_shell = [
        path_xdelta + "xdelta3",
        "-f",
        "-e",
        "-s",
        path_exe1,
        path_exe2,
        path_xdelta + "patch_" + nom_exe + "_exe.xdelta",
    ]

    process = subprocess.run(commande_shell, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                             creationflags=subprocess.CREATE_NO_WINDOW)

    return process.returncode


def patch_any_exe(nom_exe, original=False):
    """patch le texte dans le ze1.exe"""
    chemin_bin_steam = os.path.dirname(trouver_bin_zero_escape())

    if original:
        nom_exe = nom_exe + "_original"
    commande_shell = [
        path_xdelta + "xdelta3",
        "-f",
        "-d",
        "-s",
        chemin_bin_steam + "\\" + nom_exe + ".exe",
        path_xdelta + "patch_" + nom_exe + "_exe.xdelta",
        chemin_bin_steam + "\\" + nom_exe + "_new.exe",
    ]

    process = subprocess.run(commande_shell, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                             creationflags=subprocess.CREATE_NO_WINDOW)
    return process.returncode


def remplace_vieux_exe(nom_exe, process_returncode):
    if process_returncode == 0:
        chemin_bin_steam = os.path.dirname(trouver_bin_zero_escape())
        os.remove(chemin_bin_steam + "\\" + nom_exe + ".exe")
        time.sleep(0.3)
        os.rename(chemin_bin_steam + "\\" + nom_exe + "_new.exe", chemin_bin_steam + "\\" + nom_exe + ".exe")


def patch_exe_full_process(nom_exe):
    if os.path.exists(os.path.join(path_xdelta, nom_exe + "_original_exe.delta")):
        returncode = patch_any_exe(nom_exe, original=True)
        remplace_vieux_exe(nom_exe, returncode)
    returncode = patch_any_exe(nom_exe)
    creer_patch(nom_exe, original=True)
    remplace_vieux_exe(nom_exe, returncode)


def patch_ze1_exe():
    patch_exe_full_process("ze1")


def patch_Launcher_exe():
    patch_exe_full_process("Launcher")


creer_patch("ze1")
# Pour qu'on puisse mettre à jour avec google drive, faudrait
# télécharger le patch, l'appliquer et créer un nouveau exe
# créer un nouveau patch qui permet de passer de l'exe patché au exe original
# quand on rappele xdelta, faut vérifier si un patch de revert existe, si oui l'appliquer,
# puis appliquer la nouvelle version du patch
# puis recréer un patch de revert
