#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Module de saisie du mot de passe WiFi"""

from minitel.ui.ChampTexte import ChampTexte

def wifi_motdepasse(minitel, reseau):

    # on efface l'ecran et on affiche les titres
    minitel.efface()
    minitel.position(4, 4)
    minitel.couleur(caractere = 'bleu')
    minitel.effet(inversion=True)
    minitel.envoyer("Identifiants réseau")
    minitel.position(4,7)
    minitel.couleur(caractere = 'bleu')
    minitel.envoyer('nom : ')
    minitel.couleur(caractere = 'blanc')
    minitel.envoyer(reseau.nom)
    minitel.position(4,9)
    minitel.couleur(caractere = 'bleu')
    minitel.envoyer('mdp :')
    minitel.position(4, 12)
    minitel.envoyer('NB : ')
    minitel.couleur(caractere = 'bleu')
    minitel.envoyer('Clavier en mode minuscule')

    # on affiche le pied de page
    minitel.position(17,24)
    minitel.couleur(caractere='vert')
    minitel.envoyer('Retour au menu: ')
    minitel.effet(inversion = True)
    minitel.envoyer('SOMMAIRE')

    # on affiche le champ de saisie du mot de passe
    champ = ChampTexte(minitel, 10, 9, 30, 60, valeur = reseau.mdp,
                       champ_cache = reseau.masque_mdp)
    champ.affiche()
    champ.gere_arrivee()
    valid = champ.executer()
    champ.gere_depart()
    
    if valid:
        reseau.mdp = champ.valeur
        minitel.position(1,0)
        minitel.couleur(caractere='vert')
        minitel.envoyer('Mot de passe enregistré...          ')
    else:
        minitel.position(1,0)
        minitel.couleur(caractere='vert')
        minitel.envoyer('Retour au menu...                   ')

    return True
