#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Module de consultation des paramètres d'un service
    
"""

from minitel.ui.Menu import Menu

def services_consult(minitel, service, local = False):
    """Permet d'afficher les paramètres d'un service et de l'ajouter,
    l'éditer ou le supprimer suivant qu'il se trouve dans l'annuaire
    en ligne ou dans l'annuaire personnel
    
    *param local*
        Vrai si on est dans l'annuaire personnel, Faux si on est dans
        l'annuaire en ligne
    *type local*
        [Vrai, Faux]

        returns:
            True
            
    """
    
    # on efface l'écran et on affiche le titre
    minitel.efface()
    minitel.position(4, 4)
    minitel.couleur(caractere = 'bleu')
    minitel.effet(inversion=True)
    minitel.envoyer("Paramètre du service")

    # on affiche les paramètres
    y = 6
    for key in service:
        # on affiche pas l'id
        if key == 'id':
            continue
        if service[key]:
            minitel.position(6,y)
            minitel.couleur(caractere = 'bleu')
            minitel.envoyer(key)
            minitel.position(18,y)
            minitel.envoyer(str(service[key])[:22])
            y = y+1

    # On affiche le titre menu du service
    y = y+2
    minitel.position(4, y)
    minitel.couleur(caractere = 'bleu')
    minitel.effet(inversion=True)
    minitel.envoyer("Menu du service")
    
    # On crée le contenu du menu en fonction de l'annuaire courant
    if local:
        options = [
            "Consulter le service",
            "Editer le service",
            "Supprimer de l'annuaire",
            "Retourner au menu"
        ]
    else:
        options = [
            "Consulter le service",
            "Ajouter dans l'annuaire personnel",
            "Retourner au menu"
        ]
    
    # On affiche le menu
    menu = Menu(minitel, options, 6, y+1, grille = False)
    menu.affiche()
    
    if menu.executer():
        # On renvoit la sélection
        return menu.selection
    else:
        # On force le retour menu
        if local:
            return 3
        else:
            return 2
