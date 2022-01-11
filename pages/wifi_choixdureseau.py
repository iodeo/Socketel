#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Module de choix du réseau parmis les réseaux WiFi disponibles"""

from minitel.ui.Menu import Menu

def wifi_choixdureseau(minitel, reseau):
    """Affiche la liste des réseaux detectés par l'ESP32 sous forme
    d'une liste permetttant la sélection du réseau souhaité

        returns:
            False : pas de changement de sélection
            True : changement de sélection
    
    """

    # On nettoie la page et on affiche le titre
    minitel.efface()
    minitel.position(4, 4)
    minitel.couleur(caractere = 'bleu')
    minitel.effet(inversion=True)
    minitel.envoyer("Réseaux disponibles")

    # On scanne les réseaux 
    reseaux = reseau.scan()

    # On calcule la largeur necessaire pour afficher les noms de réseau
    largeur = 10
    for ele in reseaux:
        if len(ele[0]) > largeur:
            largeur = len(ele[0])

    # On affiche les titres du menu
    minitel.position(6,7)
    minitel.envoyer("*SSID")

    minitel.position(10+largeur,7)
    minitel.couleur(caractere = 'bleu')
    minitel.envoyer("*RSSI")

    # On prépare les options du menu de sélection de réseau
    # et on affiche les RSSI correspondants
    options = []
    y = 9
    for ele in reseaux:
        options.append(ele[0].decode())
        minitel.position(10+largeur,y)
        minitel.couleur(caractere = 'bleu')
        minitel.envoyer(str(ele[3]))
        y = y + 1

    # On identifie le réseau actuel
    i = 0
    while i < len(options):
        if options[i] == reseau.nom:
            options[i] = options[i] + ' (*)'
            break
        i = i+1

    # On affiche le menu de selection de réseau
    menu = Menu(minitel, options, 5, 8, grille = False)
    menu.affiche()
    
    if menu.executer():
        # On met à jour si un nouveau réseau est selectionné
        if menu.selection != i:
            reseau.nom = options[menu.selection]
            minitel.position(1,0)
            minitel.envoyer('Choix réseau enregistré...        ')
    else:
        minitel.position(1,0)
        minitel.envoyer('Retour au menu...            ')

    return True
