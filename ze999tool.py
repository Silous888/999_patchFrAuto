import subprocess
import os


def unpack_ze1_bin():
    """décompile le bin de 999"""
    subprocess.run(
        "ZE999Tool.v0.9.8.1\\ZE999Tool.exe bin-unpack bin_org\\ze1_data.bin data_ze1",
        shell=True, creationflags=subprocess.CREATE_NO_WINDOW,
    )


def extraire_fichiers_valide():
    """copie les fichiers intéressants pour la traduction dans le dossier sir_org"""
    subprocess.run(
        "ZE999Tool.v0.9.8.1\\ZE999Tool.exe sir-copy-valid data_ze1\\sir sir_org",
        shell=True, creationflags=subprocess.CREATE_NO_WINDOW,
    )


def decompression_textes():
    """rend les fichiers de sir_org compréhensibles en les transformant en xml"""
    subprocess.run(
        "ZE999Tool.v0.9.8.1\\ZE999Tool.exe sir-unpack sir_org xml_unpacked",
        shell=True,
        creationflags=subprocess.CREATE_NO_WINDOW
    )


def generer_fichier_caractere():
    """génère le fichier krchars pour patcher les caractères coréens"""
    subprocess.run(
        "ZE999Tool.v0.9.8.1\\ZE999Tool.exe sir-generate-patch-chars sir_org xml_patch xml_patch\\krchars.txt",
        shell=True, creationflags=subprocess.CREATE_NO_WINDOW,
    )


def compresser_fichier_font():
    """créér les xml et les png des fonts"""
    subprocess.run(
        "ZE999Tool.v0.9.8.1\\ZE999Tool.exe sir-generate-font-data sir_org xml_patch xml_patch\\font\\default.fnt xml_patch\\font\\border.fnt xml_patch",
        shell=True, creationflags=subprocess.CREATE_NO_WINDOW,
    )


def compresser_fichiers_modifies():
    """compresse les xml en .sir"""
    subprocess.run(
        "ZE999Tool.v0.9.8.1\\ZE999Tool.exe sir-patch sir_org xml_patch 3 sir_patched",
        shell=True, creationflags=subprocess.CREATE_NO_WINDOW,
    )


def appliquer_fichiers_modif_bin(chemin_bin_steam):
    """recompile le jeu avec les fichiers patchés

    Args:
        chemin_bin_steam (str): chemin absolu du ze1_data.bin du dossier steam du jeu
    """
    chemin_bin_steam = os.path.dirname(chemin_bin_steam)

    chemin_ze999tool = r"ZE999Tool.v0.9.8.1\\ZE999Tool.exe"
    commande_shell = [
        chemin_ze999tool,
        "bin-patch",
        "bin_org\\ze1_data.bin",
        "sir_patched",
        chemin_bin_steam,
    ]
    subprocess.run(commande_shell, creationflags=subprocess.CREATE_NO_WINDOW)
