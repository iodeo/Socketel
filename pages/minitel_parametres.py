#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Module de gestion des paramètres Minitel"""

from minitel.ui.Menu import Menu
from minitel.constantes import CAPACITES_BASIQUES
from parametres import ecrire_vitesse

def minitel_parametres(minitel):
    # on efface l'écran et on affiche le titre
    minitel.efface()
    minitel.position(4, 4)
    minitel.couleur(caractere = 'bleu')
    minitel.effet(inversion=True)
    minitel.envoyer("Vitesse par défaut au démarrage :")

    # on définit les options du menu
    options = [
        'Aucune',
        'Vitesse actuelle'
    ]

    # on affiche le menu
    menu = Menu(minitel, options, 6, 5, grille = False)
    menu.affiche()
    
    if menu.executer():
        # on enregistre le choix
        if menu.selection == 0:
            minitel.position(1,0)
            minitel.envoyer('Vitesse auto désactivé')
            ecrire_vitesse({'auto': False, 'vitesse': 1200})
        elif menu.selection == 1:
            minitel.position(1,0)
            minitel.envoyer('Vitesse auto à ' + str(minitel.vitesse) + ' bps')
            ecrire_vitesse({'auto': True, 'vitesse': minitel.vitesse})
    else:
        minitel.position(1,0)
        minitel.envoyer('Retour au menu...            ')
    
    return True
