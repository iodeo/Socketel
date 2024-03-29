#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Module de consultation de l'annuaire en ligne

"""

from minitel.ui.Menu import Menu

from parametres import lire_annuaire_url #, ajouter_service
from pages.services_consult import services_consult

def services_annuaire(minitel, reseau):
    """Affiche la liste des services présents dans l'annuaire en ligne
    L'url utilisé est présent récupéré du fichier annuaire.json
    et modifiable avec la page services_parametres

        returns:
            True

    """

    # On efface l'ecran et affiche le titre
    minitel.efface()
    minitel.position(4, 4)
    minitel.couleur(caractere = 'bleu')
    minitel.effet(inversion=True)
    minitel.envoyer("Services disponibles")

    # On verifie que la connexion wifi est établie
    if not reseau.isconnected():
        minitel.position(1,0)
        minitel.couleur(caractere='vert')
        minitel.envoyer('WiFi déconnecté !            ')
        return False

    # on récupère l'annuaire en ligne
    url = lire_annuaire_url()
    try:
        annuaire = reseau.get(url).json()
        annuaire = annuaire['servers']
    except:
        annuaire = []

    # on affiche les soustitres
    minitel.position(6, 6)
    minitel.couleur(caractere = 'bleu')
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
    options.append('Retourner au menu')

    # on affiche le menu
    menu = Menu(minitel, options, 6, 6, grille = False)
    menu.affiche()
    # s'il n' a pas de service, on descend le curseur vers le menu
    if not annuaire:
        selection = menu.option_suivante(0)
        menu.change_selection(selection)

    if menu.executer():
        if menu.selection < len(options)-1:
            service = menu.selection
            # Voir les paramètres du service selectionné
            services_consult(minitel, annuaire[menu.selection], reseau)
    else:
        return True
