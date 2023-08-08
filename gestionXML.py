import utils
from lxml import etree as ET

CHEMIN_XML = "ZE999Tool.v0.9.8.1\\xml_patch\\"


def get_arbre_xml(chemin_fichier):
    """renvoie l'arbre du fichier xml

    Args:
        chemin_fichier (str): chemin du fichier

    Returns:
        ElementTree: arbre de fichier xml
    """
    with open(chemin_fichier, "r", encoding="UTF-8") as fichier:
        return ET.parse(fichier)


def sauvergarder_fichier_xml(chemin_fichier, arbre):
    """sauvegarde les modifications du fichier xml

    Args:
        chemin_fichier (str): chemin du fichier xml
        arbre (ElementTree): arbre modifié du fichier xml
    """
    arbre.write(chemin_fichier, encoding="utf-8")


def get_racine_xml(arbre_xml):
    """renvoie la racine de l'arbre xml

    Args:
        arbre_xml (ElementTree): arbre du fichier xml

    Returns:
        element: racine de l'arbre
    """
    return arbre_xml.getroot()


def afficher_elements(racine):
    """affiche les différents sous-élément d'un élément

    Args:
        racine (element): élément dont on veut afficher les sous-éléments
    """
    for element in racine:
        print("Element : ", element.tag)


def get_elements_avec_texte(racine):
    """renvoie tous les élements avec un attribut contenant du texte lié à la traduction

    Args:
        racine (element): racine contenant tous les sous-élément à parcourir

    Returns:
        list(element): liste de tous les éléments avec du texte
    """
    liste_noeuds = []
    return get_elements_avec_texte_reccursion(racine, liste_noeuds)


def get_elements_avec_texte_reccursion(racine, liste_noeuds):
    """fonction récursive pour récupérer tous les éléments et sous-éléments
    contenant du texte lié à la traduction

    Args:
        racine (element): element où on vérifie la présence de texte
        liste_noeuds (_type_): liste où on stocke les éléments présentant du texte

    Returns:
        list(element): liste où on stocke les éléments présentant du texte mise à jour
    """
    if ( # si l'élément contient du texte à traduire,
        "text" in racine.attrib
        or "text1" in racine.attrib
        or "value" in racine.attrib
        or "name" in racine.attrib
    ):
        liste_noeuds.append(racine) # alors on l'ajoute
    for sous_element in racine: # on rappelle la fonction pour tous les enfants de l'élément
        liste_noeuds = get_elements_avec_texte_reccursion(sous_element, liste_noeuds)
    return liste_noeuds


def set_text_by_id(liste_elements, id, texte):
    """met le nouveau texte dans l'élément correspondant à l'id

    Args:
        liste_elements (list(element)): tous les éléments avec du texte
        id (str): id de l'élément où on veut placer le texte
        texte (str): texte qu'on veut placer
    """
    for element in liste_elements:
        if "id" in element.attrib and element.attrib["id"] == id:
            if "text" in element.attrib:
                element.attrib["text"] = texte
                continue
            elif "value" in element.attrib:
                element.attrib["value"] = texte
                continue
            elif "text1" in element.attrib:
                element.attrib["value"] = texte
                continue
            elif "value" in element.attrib:
                element.attrib["value"] = texte
                continue
        elif "key" in element.attrib and element.attrib["key"] == utils.supprime_amp(
            id
        ): # pour le fichier xml name, il faut faire ça
            if "name" in element.attrib:
                element.attrib["name"] = texte
                continue
            elif "text1" in element.attrib:
                if id != texte:
                    element.attrib["text1"] = texte
                    continue
        elif "id1" in element.attrib and element.attrib["id1"] == id:
            if "text" in element.attrib:
                element.attrib["text"] = texte
                continue
        else: # cas de l'id présent dans le parent
            if (
                "key" in element.getparent().attrib
                and element.getparent().attrib["key"] == id
            ):
                if "value" in element.attrib:
                    element.attrib["value"] = texte
                    continue


def set_text_by_id_and_text_eng(liste_elements, id, texte_eng, texte):
    """met le nouveau texte dans l'élément correspondant à l'id, et au texte anglais,
    parce que fichier mal foutu avec plusieurs ligne avec le même id

    Args:
        liste_elements (list(element)): tous les éléments avec du texte
        id (str): id de l'élément où on veut placer le texte
        texte_eng (str): texte se trouvant actuellement dans l'xml où on veut placer le texte
        texte (str): texte qu'on veut placer
    """
    for element in liste_elements:
        if (
            "key" in element.getparent().attrib
            and element.getparent().attrib["key"] == id
        ):
            if "value" in element.attrib:
                if element.attrib["value"] == texte_eng:
                    element.attrib["value"] = texte
                    continue
        if (
            "key1" in element.getparent().attrib
            and element.getparent().attrib["key1"] == id
        ):
            if "text" in element.attrib:
                if element.attrib["text"] == texte_eng:
                    element.attrib["text"] = texte
                    continue
        if "key1" in element.attrib and element.attrib["key1"] == id:
            if "text1" in element.attrib:
                if element.attrib["text1"] == texte_eng:
                    element.attrib["text1"] = texte
                    continue


def set_text_by_double_id(liste_elements, idparent, id, texte):
    """met le nouveau texte dans l'élément correspondant à deux id,

    Args:
        liste_elements (list(element)): tous les éléments avec du texte
        idparent (str): id du parent de l'élément où on veut placer le texte
        id (str): id de l'élément où on veut placer le texte
        texte (str): texte qu'on veut placer
    """
    for element in liste_elements:
        if "key" in element.attrib and element.attrib["key"] == id:
            if "text" in element.attrib:
                if (
                    "name" in element.getparent().attrib
                    and element.getparent().attrib["name"] == idparent
                ):
                    element.attrib["text"] = texte
                    continue
        elif "id" in element.attrib and element.attrib["id"] == id:
            if "text" in element.attrib:
                if (
                    "name" in element.getparent().attrib
                    and element.getparent().attrib["name"] == idparent
                ):
                    element.attrib["text"] = texte
                    continue
