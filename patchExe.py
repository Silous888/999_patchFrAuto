import subprocess
import os
import time

from steam import trouver_bin_zero_escape



def patch_any_exe(nom_exe):
    """patch le texte dans le ze1.exe"""
    
    path_xdelta = "ZE999Tool.v0.9.8.1\\xDeltaPatch\\"
    chemin_bin_steam = os.path.dirname(trouver_bin_zero_escape())

    commande_shell = [
        path_xdelta + "xdelta3",
        "-f",
        "-d",
        "-s",
        chemin_bin_steam + "\\" + nom_exe + ".exe",
        path_xdelta + "patch_" + nom_exe + "exe.xdelta",
        chemin_bin_steam + "\\" + nom_exe + "new.exe",
    ]

    process = subprocess.run(commande_shell, stdout=subprocess.PIPE, stderr=subprocess.PIPE, creationflags=subprocess.CREATE_NO_WINDOW)
    if process.returncode == 0:
        os.remove(chemin_bin_steam + "\\" + nom_exe + ".exe")
        time.sleep(0.3)
        os.rename(chemin_bin_steam + "\\" + nom_exe + "new.exe", chemin_bin_steam + "\\" + nom_exe + ".exe")


def patch_ze1_exe():
    patch_any_exe("ze1")


def patch_Launcher_exe():
    patch_any_exe("Launcher")


patch_Launcher_exe()