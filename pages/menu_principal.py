#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Module du menu principal"""

import time

from minitel.ui.Menu import Menu

from pages.minitel_materiel import minitel_materiel
from pages.minitel_vitesse import minitel_vitesse
from pages.minitel_parametres import minitel_parametres

from pages.wifi_choixdureseau import wifi_choixdureseau
from pages.wifi_motdepasse import wifi_motdepasse
from pages.wifi_parametres import wifi_parametres

from pages.services_annuaire import services_annuaire
from pages.services_personnel import services_personnel
from pages.services_parametres import services_parametres

def menu_principal(minitel, reseau, select = 0):
    # on réinitialise le clavier
    minitel.configurer_clavier(etendu = True, curseur = False, minuscule = True)
    minitel.echo(False)
    minitel.efface()
    minitel.curseur(False)

    # on affiche les titres
    minitel.position(4,3)
    minitel.couleur(caractere = 'bleu')
    minitel.effet(inversion = True)
    minitel.envoyer('MINITEL')
    minitel.position(4,10)
    minitel.couleur(caractere = 'bleu')
    minitel.effet(inversion = True)
    minitel.envoyer('WIFI')
    minitel.effet(inversion = False)
    if reseau.isconnected():
        minitel.envoyer(' (connecté)')
    else:
        minitel.envoyer(' (déconnecté)')
    minitel.position(4,18)
    minitel.couleur(caractere = 'bleu')
    minitel.effet(inversion = True)
    minitel.envoyer('SERVICES')

    # on définit les options du menu avec les séparateurs
    options = [
        'Matériel',   #0 Section Minitel
        'Vitesse',    #1 "
        'Paramètres', #2 "
        '-',
        '-',
        '-',
        '-',
        'Choix du réseau',  #7 Section Wifi
        'Mot de passe',     #8 "
        '',                 #9 " (Conn./Deconn.)
        'Paramètres',       #10 "
        '-',
        '-',
        '-',
        '-',
        'Annuaire en ligne',  #15
        'Annuaire personnel', #16
        'Paramètres'          #17
    ]
    
    # on adapte l'option Connexion / Deconnexion en fonction
    # de l'état actuel
    if reseau.isconnected():
        options[9] = 'Déconnexion'
    else:
        options[9] = 'Connexion'

    # on affiche le menu
    menu = Menu(minitel, options, 6, 4, grille = False,
                selection = select)
    menu.affiche()
    
    if menu.executer():
        
        # on execute l'option selectionnée
        if menu.selection == 0:
            minitel.position(1,0)
            minitel.envoyer('Minitel: Matériel')
            minitel_materiel(minitel) 
        elif menu.selection == 1:
            minitel.position(1,0)
            minitel.envoyer('Minitel: Vitesse')
            minitel_vitesse(minitel)
        elif menu.selection == 2:
            minitel.position(1,0)
            minitel.envoyer('Minitel: Paramètres')
            minitel_parametres(minitel)
        elif menu.selection == 7:
            minitel.position(1,0)
            minitel.envoyer('Wifi: Choix du réseau')
            wifi_choixdureseau(minitel, reseau)
        elif menu.selection == 8:
            minitel.position(1,0)
            minitel.envoyer('Wifi: Mot de passe')
            wifi_motdepasse(minitel, reseau)
        elif menu.selection == 9:
            minitel.position(1,0)
            minitel.envoyer('Wifi: ')
            if reseau.isconnected():
                minitel.envoyer('Deconnexion')
                reseau.deconnexion()
            else:
                minitel.effet(clignotement = True)
                minitel.envoyer('Connexion')
                reseau.connexion()
        elif menu.selection == 10:
            minitel.position(1,0)
            minitel.envoyer('Wifi: Paramètres')
            wifi_parametres(minitel, reseau)
        elif menu.selection == 15:
            minitel.position(1,0)
            minitel.envoyer('Services: Annuaire en ligne')
            services_annuaire(minitel, reseau)
        elif menu.selection == 16:
            minitel.position(1,0)
            minitel.envoyer('Services: Annuaire personnel')
            services_personnel(minitel, reseau)
            #TODO ajout / retrait / connect
        elif menu.selection == 17:
            minitel.position(1,0)
            minitel.envoyer('Services: Paramètres')
            services_parametres(minitel)
    else:
        minitel.position(1,0)
        minitel.envoyer('Sommaire...                     ')

    # on laisse le temps de lire le statut
    start_ms = time.ticks_ms()
    while True:
        time_ms = time.ticks_diff(time.ticks_ms(), start_ms)
        if  time_ms > 1000:
            break

    # on réinitialise le statut
    minitel.position(1,0)
    minitel.envoyer('Menu                             ')

    return menu.selection
