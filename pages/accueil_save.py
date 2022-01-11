#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Module d'affichage de la page d'accueil"""

from minitel.tools import (affiche_videotex, traine_caractere)
from minitel.constantes import ENVOI

def accueil(minitel):

    minitel.echo(False)
    minitel.efface('vraimenttout')
    minitel.curseur(False)

    affiche_videotex(minitel, 'arobase.vdt')

    traine_caractere(minitel, 1,13,15,'MINITEL', couleur='bleu')
    traine_caractere(minitel, 30,21,15,'+', couleur='bleu')
    traine_caractere(minitel, 35,23,15,'ESP32', couleur='bleu')

    minitel.position(13,17)
    minitel.couleur(caractere = 'bleu', fond = 'noir')
    minitel.taille(largeur = 2, hauteur = 2)
    minitel.envoyer('Socketel')

    minitel.position(6,19)
    minitel.couleur(caractere = 'blanc', fond = 'bleu')
    minitel.envoyer(' PORTAL TO MINITEL WEBSERVICES ')

    minitel.position(12,22)
    minitel.effet(clignotement = True)
    minitel.envoyer("APPUYER SUR ENVOI")

    touche = minitel.recevoir_sequence()
    while (not touche.egale(ENVOI)):
        touche = minitel.recevoir_sequence()

