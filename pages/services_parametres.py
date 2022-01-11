#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Module de saisie du mot de passe WiFi"""

from minitel.ui.ChampTexte import ChampTexte
from parametres import lire_annuaire, ecrire_annuaire

def services_parametres(minitel):

    # on efface l'ecran et on affiche les titres
    minitel.efface()
    minitel.position(4, 4)
    minitel.couleur(caractere = 'bleu')
    minitel.effet(inversion=True)
    minitel.envoyer("Annuaire en ligne")
    minitel.position(4,7)
    minitel.couleur(caractere = 'bleu')
    minitel.envoyer('url :')
    
    # on récupère l'url de l'annuaire
    annuaire = lire_annuaire()
    url = annuaire['url']

    # on affiche le champ de saisie de l'url
    champ = ChampTexte(minitel, 10, 7, 30, 60, valeur = url)
    champ.affiche()
    champ.gere_arrivee()
    valid = champ.executer()
    champ.gere_depart()
    
    if valid:
        annuaire['url'] = champ.valeur
        ecrire_annuaire(annuaire)
        minitel.position(1,0)
        minitel.envoyer('Url enregistré...            ')
    
    else:
        minitel.position(1,0)
        minitel.envoyer('Retour au menu...            ')

    return True
