#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Module d'identification du Minitel en cours d'utilisation"""

def minitel_materiel(minitel):
    # on efface l'écran et on affiche le titre
    minitel.efface()
    minitel.position(4, 4)
    minitel.couleur(caractere = 'bleu')
    minitel.effet(inversion=True)
    minitel.envoyer("Matériel détecté")

    # on affiche le pied de page
    minitel.position(17,24)
    minitel.couleur(caractere='vert')
    minitel.envoyer('Retour au menu: ')
    minitel.effet(inversion = True)
    minitel.envoyer('SOMMAIRE')

    # on détecte le matériel en lisant la rom du minitel
    minitel.identifier()

    # on affiche le résultat
    y = 6
    for ele in minitel.capacite:
        minitel.position(6,y)
        minitel.couleur(caractere = 'bleu')
        minitel.envoyer(ele)
        minitel.position(20,y)
        val = str(minitel.capacite[ele])
        minitel.envoyer(val)
        y = y+1
    
    # on attend la saisie d'une touche clavier pour revenir au menu
    touche = minitel.recevoir_sequence()
    minitel.position(1,0)
    minitel.couleur(caractere='vert')
    minitel.envoyer('Retour au menu...        ')

    return True
