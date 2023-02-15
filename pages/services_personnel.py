#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Module de consultation de l'annuaire personnel

"""

from minitel.ui.Menu import Menu

from parametres import lire_annuaire_personnel
from pages.services_consult import services_consult
from pages.services_edit import services_edit

def services_personnel(minitel, reseau):
    """Affiche la liste des services présents dans l'annuaire personnel
    et permet d'ajouter des entrées

        returns:
            True
    """
    selection = 0
    while True:
        # On efface l'écran et on affiche le titre
        minitel.efface()
        minitel.position(4, 4)
        minitel.couleur(caractere = 'bleu')
        minitel.effet(inversion=True)
        minitel.envoyer("Services disponibles")

        # On récupère l'annuaire personnel
        annuaire = lire_annuaire_personnel()

        # on affiche les soustitres
        minitel.position(6, 6)
        minitel.couleur(caractere = 'bleu')
        # ~ if annuaire:
            # ~ minitel.envoyer("*Nom")
        # ~ else:
        if not annuaire:
            minitel.envoyer("Aucun service")
        minitel.position(4, 9 + len(annuaire))
        minitel.couleur(caractere = 'bleu')
        minitel.effet(inversion=True)
        minitel.envoyer("Menu de l'annuaire")

        # on crée le de selection de service et d'action
        options = []
        for ele in annuaire:
            options.append(ele['name'])
        # on ajoute les actions possibles en fin de menu
        for i in range(4):
            options.append('-')
        options.append('Ajouter un service')
        options.append('Retourner au menu')

        # On affiche le menu
        menu = Menu(minitel, options, 6, 6, grille = False, selection = selection)
        menu.affiche()
        # s'il n' a pas de service, on descend le curseur vers le menu
        if not annuaire:
            selection = menu.option_suivante(0)
            menu.change_selection(selection)

        if menu.executer():
            if menu.selection < len(options)-2:
                selection = menu.selection
                services_consult(minitel, annuaire[menu.selection], reseau, local = True)

            elif menu.selection == len(options)-2: # ajouter service
                minitel.position(1,0)
                minitel.couleur(caractere='vert')
                minitel.envoyer('Ajout d\'un service           ')
                services_edit(minitel)
                continue

            else: # item retour
                return True
        else:
            # sommaire
            return True
