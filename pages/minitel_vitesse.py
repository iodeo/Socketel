#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Module de gestion de la vitesse de communication avec le Minitel"""

from minitel.ui.Menu import Menu
from minitel.constantes import CAPACITES_BASIQUES

def minitel_vitesse(minitel):
    # on identifie le matériel pour connaitre le vitesse max
    if minitel.capacite == CAPACITES_BASIQUES:
        minitel.identifier()

    # on efface l'écran et on affiche le pied de page
    minitel.efface()
    minitel.position(17,24)
    minitel.couleur(caractere='vert')
    minitel.envoyer('Retour au menu: ')
    minitel.effet(inversion = True)
    minitel.envoyer('SOMMAIRE')

    # on affiche les titres et le contenu
    minitel.position(4, 4)
    minitel.couleur(caractere = 'bleu')
    minitel.effet(inversion=True)
    minitel.envoyer("Vitesse (bits par seconde)")
    minitel.position(6,6)
    minitel.couleur(caractere = 'bleu')
    minitel.envoyer('Actuelle')
    minitel.position(20,6)
    minitel.envoyer(str(minitel.vitesse))
    minitel.position(6,7)
    minitel.couleur(caractere = 'bleu')
    minitel.envoyer('Maximale')
    minitel.position(20,7)
    minitel.envoyer(str(minitel.capacite['vitesse']))
    minitel.position(4, 10)
    minitel.couleur(caractere = 'bleu')
    minitel.effet(inversion=True)
    minitel.envoyer('Changement de vitesse               ')

    # on définit les options de base pour le changement de vitesse
    options = [
        'Non',
        ' 300 bps - FIXME',
        '1200 bps',
    ]

    # on ajoute les vitesses en fonction de la capacite du minitel
    if minitel.capacite['vitesse'] > 1200:
        options.append('4800 bps')
    if minitel.capacite['vitesse'] > 4800:
        options.append('9600 bps')
 
    # on affiche le menu de selection de vitesse
    menu = Menu(minitel, options, 6, 11, grille = False)
    menu.affiche()
    
    if menu.executer():
        # on définit le vitesse souhaitée
        if menu.selection == 0:
            minitel.position(1,0)
            minitel.couleur(caractere='vert')
            minitel.envoyer('Retour au menu...                   ')
        elif menu.selection == 1:
            minitel.position(1,0)
            minitel.couleur(caractere='vert')
            minitel.envoyer('Passage à 300 bps...                ')
            minitel.definir_vitesse(300)
        elif menu.selection == 2:
            minitel.position(1,0)
            minitel.couleur(caractere='vert')
            minitel.envoyer('Passage à 1200 bps...               ')
            minitel.definir_vitesse(1200)
        elif menu.selection == 3:
            minitel.position(1,0)
            minitel.couleur(caractere='vert')
            minitel.envoyer('Passage à 4800 bps...               ')
            minitel.definir_vitesse(4800)
        elif menu.selection == 4:
            minitel.position(1,0)
            minitel.couleur(caractere='vert')
            minitel.envoyer('Passage à 9600 bps...               ')
            minitel.definir_vitesse(9600)
    else:
        minitel.position(1,0)
        minitel.couleur(caractere='vert')
        minitel.envoyer('Retour au menu...                   ')
        
    return True
