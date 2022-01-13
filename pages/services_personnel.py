#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Module de consultation de l'annuaire personnel

"""

from minitel.ui.Menu import Menu

from parametres import (lire_annuaire_personnel, supprimer_service)

from pages.services_consult import services_consult
from pages.services_connect import services_connect
from pages.services_edit import services_edit

def services_personnel(minitel, reseau):
    """Affiche la liste des services présents dans l'annuaire personnel
    et permet d'ajouter des entrées

        returns:
            True
    """
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
    if annuaire:
        minitel.envoyer("*Nom")
    else:
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
    menu = Menu(minitel, options, 6, 6, grille = False)
    menu.affiche()
    # s'il n' a pas de service, on descend le curseur vers le menu
    if not annuaire:
        selection = menu.option_suivante(0)
        menu.change_selection(selection)
    
    if menu.executer():
        if menu.selection < len(options)-2:
            choix = services_consult(minitel, annuaire[menu.selection], local = True)
        elif menu.selection == len(options)-2:
                minitel.position(1,0)
                minitel.couleur(caractere='vert')
                minitel.envoyer('Edition de service           ')
                services_edit(minitel)
                return True
        else:
            choix = 3
    else:
        # retour menu
        choix = 3

    # on execute la tâche choisie dans le sous-menu services_consult
    if choix == 0:
        # Consulter service
        services_connect(minitel, reseau, annuaire[menu.selection])
    elif choix == 1:
        # Editer service
        minitel.position(1,0)
        minitel.couleur(caractere='vert')
        minitel.envoyer('Edition de service           ')
        services_edit(minitel, annuaire[menu.selection])
    elif choix == 2:
        # Supprimer service
        minitel.position(1,0)
        minitel.couleur(caractere='vert')
        minitel.envoyer('Suppression du service...    ')
        supprimer_service(annuaire[menu.selection]['id'])
    elif choix == 3:
        # Retour menu
        minitel.position(1,0)
        minitel.couleur(caractere='vert')
        minitel.envoyer('Retour au menu...            ')

    return True
