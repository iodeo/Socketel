#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Module d'édition des paramètres d'un service
    
"""

from minitel.ui.ChampTexte import ChampTexte
from minitel.ui.Conteneur import Conteneur
from minitel.ui.Label import Label
from minitel.ui.Menu import Menu

from parametres import (ajouter_service, modifier_service)

def services_edit(minitel, service = None):
    """Permet d'afficher des champs d'edition des paramètres d'un
    service de l'annuaire personnel

    *param service*
        dictionnaire des paramètres du service à éditer
        si omis, un nouveau service est crée
    *type service*
        dict

    returns:
        True

    """
    # on efface l'écran et on affiche les titres
    minitel.efface()
    minitel.position(4, 4)
    minitel.couleur(caractere = 'bleu')
    minitel.effet(inversion=True)
    minitel.envoyer("Paramètre du service")
    minitel.position(4, 15)
    minitel.couleur(caractere = 'bleu')
    minitel.effet(inversion=True)
    minitel.envoyer("Menu d'édition")

    # on affiche le pied de page
    minitel.position(17,24)
    minitel.couleur(caractere='vert')
    minitel.envoyer('Retour au menu: ')
    minitel.effet(inversion = True)
    minitel.envoyer('SOMMAIRE')

    # si aucun service n'est fourni on en crée un template
    if not service:
        service = {
            'id': -1,
            'name': '',
            'address': '',
            'ping': 0,
            'subprotocol': ''
        }

    # on crée les champs d'edition
    labelName = Label(minitel, 6, 6, 'name    :', couleur = 'bleu')
    champName = ChampTexte(minitel, 16, 6, 10, 10, valeur = service['name'])
    labelAddress = Label(minitel, 6, 7, 'address :', couleur = 'bleu')
    champAddress = ChampTexte(minitel, 16, 7, 24, 60, valeur = service['address'])
    labelOptional = Label(minitel, 6, 9, '- optional -', couleur = 'bleu')
    labelPing = Label(minitel, 6, 11, 'ping (s):', couleur = 'bleu')    
#     champPing = ChampTexte(minitel, 16, 11, 6, 6, valeur = str(service['ping']))
    labelPingMsg = Label(minitel, 16, 11, 'None', couleur = 'bleu')
    labelSubprotocol = Label(minitel, 6, 12, 'subprot.:', couleur = 'bleu')
    champSubprotocol = ChampTexte(minitel, 16, 12, 10, 10, valeur = service['subprotocol'])

    # on crée le menu d'édition
    options = [
        'Enregistrer',
        'Annuler'
    ]
    menu = Menu(minitel, options, 6, 16, grille = False)

    # on ajoute les champs et le menu dans un conteneur
    conteneur = Conteneur(minitel, 1, 1, 40, 20)
    conteneur.ajoute(labelName)
    conteneur.ajoute(champName)
    conteneur.ajoute(labelAddress)
    conteneur.ajoute(champAddress)
    conteneur.ajoute(labelOptional)
    conteneur.ajoute(labelPing)
#     conteneur.ajoute(champPing)
    conteneur.ajoute(labelPingMsg)
    conteneur.ajoute(labelSubprotocol)
    conteneur.ajoute(champSubprotocol)
    conteneur.ajoute(menu)

    # on affiche le conteneur
    conteneur.affiche()
    valid = conteneur.executer()
    minitel.curseur(False)
    # on gere l'edition si validée
    if valid:
        if menu.selection == 0:
            # On enregistre le service
            minitel.position(1,0)
            minitel.couleur(caractere='vert')
            minitel.envoyer('Enregistrement du service...   ')
            # on récupère les paramètres
            service['name'] = champName.valeur
            service['address'] = champAddress.valeur
            #service['ping'] = champPing.valeur
            service['subprotocol'] = champSubprotocol.valeur
            if service['id'] == -1:
                # on ajoute le nouveau service
                ajouter_service(service)
            else:
                # on modifie le service existant
                modifier_service(service)
            return True

    # sinon on retourne au menu
    minitel.position(1,0)
    minitel.couleur(caractere='vert')
    minitel.envoyer('Retour au menu...            ')
    return True
