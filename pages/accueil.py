#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Module d'affichage de la page d'accueil"""

from minitel.tools import (affiche_videotex, traine_caractere)
from minitel.constantes import ENVOI

def accueil(minitel, attendre=True):
	minitel.echo(False)
	minitel.efface('vraimenttout')
	minitel.curseur(False)

	affiche_videotex(minitel, 'arobase.vdt')

	traine_caractere(minitel, 1,14,15,'MINITEL', couleur='vert')
	traine_caractere(minitel, 30,21,15,'+', couleur='vert')
	traine_caractere(minitel, 35,22,15,'ESP32', couleur='vert')

	minitel.position(13,17)
	minitel.couleur(caractere = 'blanc')
	minitel.taille(largeur = 2, hauteur = 2)
	minitel.envoyer('SocketeL')

	minitel.position(7,19)
	minitel.couleur(caractere = 'vert')
	minitel.envoyer('Portal to minitel webservices')
	minitel.position(10,20)
	minitel.couleur(caractere = 'vert')
	minitel.envoyer('written in micropython')
	minitel.position(9,21)
	minitel.couleur(caractere = 'vert')
	minitel.envoyer('for ESP32 microcontroller')

	if attendre:
		minitel.position(12,24)
		minitel.effet(clignotement = True)
		minitel.envoyer("APPUYER SUR ENVOI")

	minitel.position(1,0)
	minitel.couleur(caractere = 'vert')
	minitel.envoyer('github.com/iodeo/socketel')

	if attendre:
		touche = minitel.recevoir_sequence()
		while (not touche.egale(ENVOI)):
			touche = minitel.recevoir_sequence()
