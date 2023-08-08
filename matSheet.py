class NomsColonnes:
    """noms des 3 colonnes avec les données intéressantes pour chaque type de fichier
    la première colonne est celle de l'ID, ensuite celle du texte anglais, puis celle du texte français
    """

    DLG = ["id", "text", "VF"]
    DESC = ["id", "byte/value", "ValueFR"]
    NAME = ["key", "name", "nameFr"]
    ROOM = ["id", "text", "textFr"]
    MSG = ["key", "unknown1/text", "unknown1/textFr"]
    FCHART = ["id1", "text", "textFr"]
    ITEM = ["key", "text1", "textFr"]
    DOC = ["key", "text", "textFr"]
    MAP = ["name/key", "text", "textFr"]
    CREDIT = ["id", "text", "textFr"]


def get_matrice_simplifie(mat, liste_noms_colonnes):
    """renvoie la matrice simplifié du sheet, avec seulement les données nécessaires

    Args:
        mat (list(list(str))): toutes les valeurs présentes dans la sheet
        liste_noms_colonnes (list\[3](str)): les noms des colonnes dont on veut les valeurs

    Returns:
        list(list\[3](str)): matrice avec les données intéressantes
    """
    try:
        position_id, position_eng, position_fr = get_positions_colonnes(
            mat[0], liste_noms_colonnes
        )
    except:
        print("valeur non trouvée")
        return []
    new_mat = []
    id_msg = ""
    id_doc = ""
    for i in range(
        2, len(mat)
    ):  # les sheet ont des datas intéressantes à partir de la ligne 2
        if len(mat[i]) == 0:  # si une ligne est vide
            continue
        if (
            liste_noms_colonnes == NomsColonnes.DOC and len(mat[i][position_id]) != 0
        ):  # le ficher doc a un seul id pour plusieurs lignes
            id_doc = mat[i][position_id]
        if len(mat[i]) > position_eng:
            if (
                liste_noms_colonnes == NomsColonnes.MSG
                and mat[i][position_eng].isdigit()  # le fichier MSG a ses id dans la
            ):  # colonne de l'anglais, et ce sont des nombres
                id_msg = mat[i][position_id]
                continue
            if liste_noms_colonnes == NomsColonnes.MSG:
                new_mat.append([id_msg, mat[i][position_eng]])
                new_mat[-1].append(
                    _ajouter_texte_fr_dans_mat_simp(mat[i], position_fr, position_eng)
                )
            else:
                value_mat_id = mat[i][position_id]
                if len(value_mat_id) == 0 and liste_noms_colonnes == NomsColonnes.DOC:
                    value_mat_id = id_doc
                if (
                    liste_noms_colonnes != NomsColonnes.DESC
                    or "▼" in mat[i][position_eng] # on ajoute juste les lignes de script pour
                ):                                 # les fichiers DESC
                    new_mat.append([value_mat_id, mat[i][position_eng]])
                    new_mat[-1].append(
                        _ajouter_texte_fr_dans_mat_simp(
                            mat[i], position_fr, position_eng
                        )
                    )
    return new_mat


def get_matrice_simplifie_double_id(mat, liste_noms_colonnes):
    """renvoie la matrice simplifié du sheet, avec seulement les données nécessaires
    pour les sheet présentant 2 id pour identifier une ligne

    Args:
        mat (list(list(str))): toutes les valeurs présentes dans la sheet
        liste_noms_colonnes (list\[3](str)): les noms des colonnes dont on veut les valeurs

    Returns:
        list(list\[4](str)): matrice avec les données intéressantes
    """
    try:
        position_id, position_eng, position_fr = get_positions_colonnes(
            mat[0], liste_noms_colonnes
        )
    except:
        print("valeur non trouvée")
        return []
    new_mat = []
    id_parent = ""
    for i in range(2, len(mat)):  # les sheet ont des datas intéressantes à partir de la ligne 2
        if len(mat[i]) == 0:  # si une ligne est vide
            continue
        if len(mat[i]) <= position_eng:  # si une ligne n'a pas de texte anglais
            id_parent = mat[i][position_id]  # on stocke l'id principal
            continue
        new_mat.append([id_parent, mat[i][position_id], mat[i][position_eng]])
        new_mat[-1].append(_ajouter_texte_fr_dans_mat_simp(mat[i], position_fr, position_eng))
    return new_mat


def _ajouter_texte_fr_dans_mat_simp(mat_ligne, position_fr, position_eng):
    """renvoie le texte à placer dans la colonne 3 de la ligne

    Args:
        mat_ligne (list(str)): ligne avec les valeurs à ajouter
        position_fr (int): position du texte fr dans la ligne
        position_eng (int): position du texte eng dans la ligne

    Returns:
        _type_: _description_
    """
    if len(mat_ligne) > position_fr and len(mat_ligne[position_fr]) > 0:
        return mat_ligne[position_fr]  # renvoie le texte fr s'il y en a un
    else:
        return mat_ligne[position_eng]  # sinon renvoie le texte anglais


def get_positions_colonnes(mat_ligne0, liste_noms_colonnes):
    """renvoie l'index des colonnes id eng et fr

    Args:
        mat_ligne0 (list): ligne 0 de la liste de liste du sheet
        liste_noms_colonnes (list[3](str)): nom des colonnes dont on veut l'index

    Returns:
        int, int, int: index de id, puis eng, puis fr
    """
    position_id = mat_ligne0.index(liste_noms_colonnes[0])
    position_eng = mat_ligne0.index(liste_noms_colonnes[1])
    position_fr = mat_ligne0.index(liste_noms_colonnes[2])
    return position_id, position_eng, position_fr
