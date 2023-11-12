import ze999tool
import gestionXML
import steam
import googleSheetAPI
import matSheet
import listeFichier
import utils
import os
import shutil
import ImageTelechargement
import patchExe


TOTAL_PROGRESSION = (
    len(listeFichier.LISTE_NOM_FICHIER_AUTRE)
    + len(listeFichier.LISTE_NOM_FICHIER_DESC)
    + len(listeFichier.LISTE_NOM_FICHIER_DLG)
    + len(listeFichier.LISTE_ID_DOSSIER)
    + 20
)
progression_actuelle = 0


def recup_bin_ze_et_chemin_steam():
    """récupère le chemin du ze1_data1.bin et le copie
    dans le dosssier bin_org s'il n'y est pas déjà

    Returns:
        str: chemin du ze1_data.bin du dossier steam du jeu
    """
    chemin_fichier = steam.trouver_bin_zero_escape()
    utils.logging.error(chemin_fichier)
    if not os.path.exists("ZE999Tool.v0.9.8.1\\bin_org\\ze1_data.bin"):
        steam.copier_bin_dans_ZE999Tool(chemin_fichier)
    return chemin_fichier


def recup_arbre_elements_et_mat_sheet_simplifie(
    fichier, noms_colonnes, double_id=False
):
    """_summary_

    Args:
        fichier (str): fichier xml à traiter
        noms_colonnes (list[3](str)): noms des colonnes pour ce fichier
        double_id (bool, optional): True si fichier avec double id. Defaults to False.

    Returns:
        elementTree, list(element), list(list[3](str)): arbre, liste des éléments avec texte
        et matrice des données importante du sheet
    """
    arbre = gestionXML.get_arbre_xml(gestionXML.CHEMIN_XML + fichier)
    racine = gestionXML.get_racine_xml(arbre)
    elements = gestionXML.get_elements_avec_texte(racine)
    mat_sheet = googleSheetAPI.get_matrice_sheet(fichier)
    if not double_id:
        mat_sheet_simp = matSheet.get_matrice_simplifie(mat_sheet, noms_colonnes)
    else:
        mat_sheet_simp = matSheet.get_matrice_simplifie_double_id(
            mat_sheet, noms_colonnes
        )
    return arbre, elements, mat_sheet_simp


def modifier_texte_dans_fichier(elements, mat, double_id=False):
    """met le texte français du sheet dans le xml

    Args:
        elements (list(element)): les élements xml
        mat (list(list[3](str))): données importantes du sheet
        double_id (bool, optional): True si fichier avec double id. Defaults to False.
    """
    for i in range(len(mat)):
        if not double_id:
            texte_ligne = utils.remplace_guillemet(utils.remplace_apostrophe(mat[i][2]))
            gestionXML.set_text_by_id(elements, mat[i][0], texte_ligne)
        else:
            texte_ligne = utils.remplace_guillemet(utils.remplace_apostrophe(mat[i][3]))
            gestionXML.set_text_by_double_id(
                elements, mat[i][0], mat[i][1], texte_ligne
            )


def modifier_texte_dans_fichier_de_merde(elements, mat):
    """met le texte français du sheet dans le xml, pour fichier
    sans id unique pour chaque ligne

    Args:
        elements (list(element)): les élements xml
        mat (list(list[3](str))): données importantes du sheet
    """
    for i in range(len(mat)):
        texte_eng = utils.remplace_guillemet(utils.remplace_apostrophe(mat[i][1]))
        texte_ligne = utils.remplace_guillemet(utils.remplace_apostrophe(mat[i][2]))
        gestionXML.set_text_by_id_and_text_eng(
            elements, mat[i][0], texte_eng, texte_ligne
        )


def recompiler_jeu(chemin_bin_steam):
    """recompile le jeu avec les nouvelles data

    Args:
        chemin_bin_steam (str): chemin du ze1_data.bin du dossier steam du jeu
    """
    ze999tool.compresser_fichier_font()
    ze999tool.compresser_fichiers_modifies()
    ze999tool.appliquer_fichiers_modif_bin(chemin_bin_steam)


def modif_fichier_xml(instance_worker, fichier, nomColonne, double_id=False):
    """modifier un fichier xml avec les valeurs récupérés dans le sheet
    associé, et enregistre le fichier

    Args:
        instance_worker (worker): sert pour update la progression
        fichier (str): fichier à modifier
        nomColonne (list[3](str)): noms des colonnes pour ce fichier
        double_id (bool, optional): True si fichier avec double id. Defaults to False.
    """
    instance_worker.set_text_progress(fichier)
    arbre, elements, mat = recup_arbre_elements_et_mat_sheet_simplifie(
        fichier, nomColonne, double_id
    )

    modifier_texte_dans_fichier(elements, mat, double_id)

    gestionXML.sauvergarder_fichier_xml(gestionXML.CHEMIN_XML + fichier, arbre)


def modif_fichier_xml_de_merde(instance_worker, fichier, nomColonne):
    """modifier un fichier xml avec les valeurs récupérés dans le sheet
    associé, et enregistre le fichier, mais pour fichier sans id unique

    Args:
        instance_worker (worker): sert pour update la progression
        fichier (str): fichier à modifier
        nomColonne (list[3](str)): noms des colonnes pour ce fichier
    """
    instance_worker.set_text_progress(fichier)
    arbre, elements, mat = recup_arbre_elements_et_mat_sheet_simplifie(
        fichier, nomColonne
    )

    modifier_texte_dans_fichier_de_merde(elements, mat)

    gestionXML.sauvergarder_fichier_xml(gestionXML.CHEMIN_XML + fichier, arbre)


def gestion_DLG(instance_worker):
    """modifie les fichiers DLG

    Args:
        instance_worker (worker): sert pour update la progression
    """
    liste_choix_fichiers_DLG = instance_worker.liste_choix_fichiers[1]
    for index, fichier in enumerate(listeFichier.LISTE_NOM_FICHIER_DLG):
        if liste_choix_fichiers_DLG[index]:
            update_texte_progression(instance_worker, fichier)
            modif_fichier_xml(instance_worker, fichier, matSheet.NomsColonnes.DLG)
            incrementer_progression(instance_worker)


def gestion_DESC(instance_worker):
    """modifie les fichiers DESC

    Args:
        instance_worker (worker): sert pour update la progression
    """
    liste_choix_fichiers_DESC = instance_worker.liste_choix_fichiers[0]
    for index, fichier in enumerate(listeFichier.LISTE_NOM_FICHIER_DESC):
        if liste_choix_fichiers_DESC[index]:
            update_texte_progression(instance_worker, fichier)
            modif_fichier_xml(instance_worker, fichier, matSheet.NomsColonnes.DESC)
            incrementer_progression(instance_worker)


def gestion_AUTRE(instance_worker):
    liste_choix_fichiers_AUTRE = instance_worker.liste_choix_fichiers[2]
    if liste_choix_fichiers_AUTRE[0]:
        gestion_AUTRE_NAME(instance_worker)
    if liste_choix_fichiers_AUTRE[1]:
        gestion_AUTRE_MSG(instance_worker)
    if liste_choix_fichiers_AUTRE[2]:
        gestion_AUTRE_FCHART(instance_worker)
    if liste_choix_fichiers_AUTRE[3]:
        gestion_AUTRE_DOC(instance_worker)
    if liste_choix_fichiers_AUTRE[4]:
        gestion_AUTRE_MAP(instance_worker)
    if liste_choix_fichiers_AUTRE[5]:
        gestion_AUTRE_CREDIT(instance_worker)
    if liste_choix_fichiers_AUTRE[6]:
        gestion_AUTRE_ROOM(instance_worker)
    if liste_choix_fichiers_AUTRE[7]:
        gestion_AUTRE_ITEM(instance_worker)


def gestion_AUTRE_NAME(instance_worker):
    """modifie le fichier NAME

    Args:
        instance_worker (worker): sert pour update la progression
    """
    fichier = "00009ed2.name.xml"
    update_texte_progression(instance_worker, fichier)
    modif_fichier_xml(instance_worker, fichier, matSheet.NomsColonnes.NAME)
    incrementer_progression(instance_worker)


def gestion_AUTRE_ROOM(instance_worker):
    """modifie le fichier ROOM

    Args:
        instance_worker (worker): sert pour update la progression
    """
    fichier = "00009ec7.room.xml"
    update_texte_progression(instance_worker, fichier)
    update_texte_progression(instance_worker, fichier)
    modif_fichier_xml(instance_worker, fichier, matSheet.NomsColonnes.ROOM)
    incrementer_progression(instance_worker)


def gestion_AUTRE_MSG(instance_worker):
    """modifie le fichier MSG

    Args:
        instance_worker (worker): sert pour update la progression
    """
    fichier = "00009ed5.msg.xml"
    update_texte_progression(instance_worker, fichier)
    shutil.copy(
        ".\\ZE999Tool.v0.9.8.1\\xml_original\\" + fichier,
        ".\\ZE999Tool.v0.9.8.1\\xml_patch\\",
    )
    modif_fichier_xml_de_merde(instance_worker, fichier, matSheet.NomsColonnes.MSG)
    incrementer_progression(instance_worker)


def gestion_AUTRE_FCHART(instance_worker):
    """modifie le fichier FCHART

    Args:
        instance_worker (worker): sert pour update la progression
    """
    fichier = "00009ec4.fchart.xml"
    update_texte_progression(instance_worker, fichier)
    modif_fichier_xml(instance_worker, fichier, matSheet.NomsColonnes.FCHART)
    incrementer_progression(instance_worker)


def gestion_AUTRE_ITEM(instance_worker):
    """modifie le fichier ITEM

    Args:
        instance_worker (worker): sert pour update la progression
    """
    fichier = "00009ecc.item.xml"
    update_texte_progression(instance_worker, fichier)
    modif_fichier_xml(instance_worker, fichier, matSheet.NomsColonnes.ITEM)
    incrementer_progression(instance_worker)


def gestion_AUTRE_DOC(instance_worker):
    """modifie le fichier DOC

    Args:
        instance_worker (worker): sert pour update la progression
    """
    fichier = "00009ed4.doc.xml"
    update_texte_progression(instance_worker, fichier)
    shutil.copy(
        ".\\ZE999Tool.v0.9.8.1\\xml_original\\" + fichier,
        ".\\ZE999Tool.v0.9.8.1\\xml_patch\\",
    )
    modif_fichier_xml_de_merde(instance_worker, fichier, matSheet.NomsColonnes.DOC)
    incrementer_progression(instance_worker)


def gestion_AUTRE_CREDIT(instance_worker):
    """modifie le fichier CREDIT

    Args:
        instance_worker (worker): sert pour update la progression
    """
    fichier = "00009ed0.credit.xml"
    update_texte_progression(instance_worker, fichier)
    modif_fichier_xml(instance_worker, fichier, matSheet.NomsColonnes.CREDIT, True)
    incrementer_progression(instance_worker)


def gestion_AUTRE_MAP(instance_worker):
    """modifie le fichier MAP

    Args:
        instance_worker (worker): sert pour update la progression
    """
    fichier = "00009ed6.map.xml"
    update_texte_progression(instance_worker, fichier)
    modif_fichier_xml(instance_worker, fichier, matSheet.NomsColonnes.MAP, True)
    incrementer_progression(instance_worker)


def gestion_images_PNG(instance_worker):
    for i in range(len(listeFichier.LISTE_ID_DOSSIER)):
        for j in range(len(listeFichier.LISTE_ID_DOSSIER[i])):
            if instance_worker.liste_choix_images[i][j]:
                update_texte_progression(instance_worker, "téléchargement PNG " + listeFichier.LISTE_NOM_DOSSIER[i][j])
                ImageTelechargement.download_files_in_folder(listeFichier.LISTE_ID_DOSSIER[i][j])
        incrementer_progression(instance_worker)


def gestion_images_DDS(instance_worker):
    if instance_worker.choix_patch_dds:
        update_texte_progression(instance_worker, "téléchargement DDS")
        ImageTelechargement.download_files_in_folder(listeFichier.ID_DOSSIER_DDS)
        incrementer_progression(instance_worker)


def gestion_videos(instance_worker):
    if instance_worker.choix_patch_videos:
        update_texte_progression(instance_worker, "téléchargement vidéos")
        ImageTelechargement.download_files_in_folder(listeFichier.ID_DOSSIER_VIDEO)
        incrementer_progression(instance_worker)


def gestion_exe(instance_worker):
    if instance_worker.choix_patch_exe:
        update_texte_progression(instance_worker, "patch launcher et ze1.exe")
        patchExe.download_files_in_folder(listeFichier.ID_DOSSIER_PATCH_EXE)
        patchExe.patch_ze1_exe()
        patchExe.patch_Launcher_exe()


def incrementer_progression(instance_worker, valeur=1):
    """incrémente la barre de progression

    Args:
        instance_worker (worker): sert à accéder à la barre de progression
        valeur (int, optional): de combien on incrémente. Defaults to 1.
    """
    global progression_actuelle
    progression_actuelle = progression_actuelle + valeur
    instance_worker.set_value_progressbar(
        utils.get_valeur_progression(progression_actuelle, TOTAL_PROGRESSION)
    )


def update_texte_progression(instance_worker, message):
    """change le texte de progression

    Args:
        instance_worker (worker): sert à accéder à au label du texte
        message (str): texte à afficher
    """
    instance_worker.set_text_progress(message)
