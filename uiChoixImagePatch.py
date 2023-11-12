from PyQt5.QtWidgets import QGridLayout, QCheckBox, QPushButton, QVBoxLayout, QGroupBox, QDialog, QWidget, QScrollArea

import listeFichier


NOMBRE_GROUPE = 10


class CheckboxWindowImage(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Choix des images à patch')
        self.setGeometry(25, 25, 1000, 400)

        content_widget = QWidget(self)

        # Créez un layout pour le contenu
        layoute = QVBoxLayout(content_widget)

        scroll_area = QScrollArea(self)
        scroll_area.setWidget(content_widget)
        scroll_area.setWidgetResizable(True)  # Permet à son contenu d'être redimensionné

        # Ajoutez le widget de défilement à la boîte de dialogue
        main_layout = QVBoxLayout(self)
        main_layout.addWidget(scroll_area)

        num_rows = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
        num_cols = [9, 6, 5, 10, 10, 4, 9, 3, 9, 4]
        nom_groups = ["AUTRE + CLAVIER - MANETTE + LOGO ITEM + LOGO",
                      "ENIGME", "INTERFACE JEU",
                      "INTERFACE JEU - BARRE LABEL ET SWITCH MODE",
                      "INTERFACE JEU - BOUTONS ANGLE", "INTERFACE JEU - BOUTONS 8 COTES",
                      "INTERFACE JEU - GROS BOUTONS RECTANGLE", "INTERFACE JEU - LABEL",
                      "LETTRE ET CHIFFRE",
                      "MENU PRINCIPAL"]
        nom_checkboxes = [listeFichier.LISTE_NOM_AUTRE_IMAGE + listeFichier.LISTE_NOM_CLAVIER_MANETTE + listeFichier.LISTE_LOGO_ITEM + listeFichier.LISTE_LOGO,
                          listeFichier.LISTE_NOM_ENIGME,
                          listeFichier.LISTE_INTERFACE_JEU,
                          listeFichier.LISTE_INTERFACE_JEU_BARRE_LABEL_ET_SWITCH_MODE,
                          listeFichier.LISTE_INTERFACE_JEU_BOUTONS_ANGLE,
                          listeFichier.LISTE_INTERFACE_JEU_BOUTONS_8_COTES,
                          listeFichier.LISTE_INTERFACE_JEU_GROS_BOUTONS_RECTANGLE,
                          listeFichier.LISTE_INTERFACE_JEU_LABEL,
                          listeFichier.LISTE_LETTRE_ET_CHIFFRE,
                          listeFichier.LISTE_MENU_PRINCIPAL]
        self.checkboxes = [[], [], [], [], [], [], [], [], [], []]  # Pour stocker les checkboxes

        check_all_button = []
        uncheck_all_button = []

        for k in range(NOMBRE_GROUPE):
            group_box = QGroupBox(nom_groups[k])
            group_layout = QGridLayout(group_box)
            for i in range(num_cols[k]):
                for j in range(num_rows[k]):
                    index = i * num_rows[k] + j  # Calcul de l'index pour afficher en colonne
                    checkbox = QCheckBox(f'{nom_checkboxes[k][index]}')
                    self.checkboxes[k].append(checkbox)  # Ajouter la checkbox à la liste
                    group_layout.addWidget(checkbox, j, i)

            check_all_button.append(QPushButton('Cocher tout'))
            group_layout.addWidget(check_all_button[k])
            uncheck_all_button.append(QPushButton('Décocher tout'))
            group_layout.addWidget(uncheck_all_button[k])

            group_box.setLayout(group_layout)
            layoute.addWidget(group_box)

        check_all_button[0].clicked.connect(self.check_all1)
        check_all_button[1].clicked.connect(self.check_all2)
        check_all_button[2].clicked.connect(self.check_all3)
        check_all_button[3].clicked.connect(self.check_all4)
        check_all_button[4].clicked.connect(self.check_all5)
        check_all_button[5].clicked.connect(self.check_all6)
        check_all_button[6].clicked.connect(self.check_all7)
        check_all_button[7].clicked.connect(self.check_all8)
        check_all_button[8].clicked.connect(self.check_all9)
        check_all_button[9].clicked.connect(self.check_all10)

        uncheck_all_button[0].clicked.connect(self.uncheck_all1)
        uncheck_all_button[1].clicked.connect(self.uncheck_all2)
        uncheck_all_button[2].clicked.connect(self.uncheck_all3)
        uncheck_all_button[3].clicked.connect(self.uncheck_all4)
        uncheck_all_button[4].clicked.connect(self.uncheck_all5)
        uncheck_all_button[5].clicked.connect(self.uncheck_all6)
        uncheck_all_button[6].clicked.connect(self.uncheck_all7)
        uncheck_all_button[7].clicked.connect(self.uncheck_all8)
        uncheck_all_button[8].clicked.connect(self.uncheck_all9)
        uncheck_all_button[9].clicked.connect(self.uncheck_all10)

        ok_button = QPushButton('OK')
        ok_button.clicked.connect(self.ok_clicked)

        button_layout = QVBoxLayout()
        button_layout.addWidget(ok_button)

        main_layout.addLayout(layoute)
        main_layout.addLayout(button_layout)

        self.setLayout(main_layout)

        self.ok_clicked()

    def check_all1(self):
        for checkbox in self.checkboxes[0]:
            checkbox.setChecked(True)

    def uncheck_all1(self):
        for checkbox in self.checkboxes[0]:
            checkbox.setChecked(False)

    def check_all2(self):
        for checkbox in self.checkboxes[1]:
            checkbox.setChecked(True)

    def uncheck_all2(self):
        for checkbox in self.checkboxes[1]:
            checkbox.setChecked(False)

    def check_all3(self):
        for checkbox in self.checkboxes[2]:
            checkbox.setChecked(True)

    def uncheck_all3(self):
        for checkbox in self.checkboxes[2]:
            checkbox.setChecked(False)

    def check_all4(self):
        for checkbox in self.checkboxes[3]:
            checkbox.setChecked(True)

    def uncheck_all4(self):
        for checkbox in self.checkboxes[3]:
            checkbox.setChecked(False)

    def check_all5(self):
        for checkbox in self.checkboxes[4]:
            checkbox.setChecked(True)

    def uncheck_all5(self):
        for checkbox in self.checkboxes[4]:
            checkbox.setChecked(False)

    def check_all6(self):
        for checkbox in self.checkboxes[5]:
            checkbox.setChecked(True)

    def uncheck_all6(self):
        for checkbox in self.checkboxes[5]:
            checkbox.setChecked(False)

    def check_all7(self):
        for checkbox in self.checkboxes[6]:
            checkbox.setChecked(True)

    def uncheck_all7(self):
        for checkbox in self.checkboxes[6]:
            checkbox.setChecked(False)

    def check_all8(self):
        for checkbox in self.checkboxes[7]:
            checkbox.setChecked(True)

    def uncheck_all8(self):
        for checkbox in self.checkboxes[7]:
            checkbox.setChecked(False)

    def check_all9(self):
        for checkbox in self.checkboxes[8]:
            checkbox.setChecked(True)

    def uncheck_all9(self):
        for checkbox in self.checkboxes[8]:
            checkbox.setChecked(False)

    def check_all10(self):
        for checkbox in self.checkboxes[9]:
            checkbox.setChecked(True)

    def uncheck_all10(self):
        for checkbox in self.checkboxes[9]:
            checkbox.setChecked(False)

    def ok_clicked(self):
        self.checkbox_values = []
        for i in range(NOMBRE_GROUPE):
            self.checkbox_values.append([checkbox.isChecked() for checkbox in self.checkboxes[i]])
        self.close()

    def get_checkbox_values(self):
        return self.checkbox_values
