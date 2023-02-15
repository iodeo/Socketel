#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Module de consultation des paramètres d'un service

"""

from minitel.ui.Menu import Menu
# ~ from parametres import (lire_annuaire_personnel, supprimer_service)
from parametres import supprimer_service, ajouter_service
from pages.services_connect import services_connect
from pages.services_edit import services_edit

def services_consult(minitel, service, reseau, local = False):
    """Permet d'afficher les paramètres d'un service et de l'ajouter,
    l'éditer ou le supprimer suivant qu'il se trouve dans l'annuaire
    en ligne ou dans l'annuaire personnel

    *param local*
        Vrai si on est dans l'annuaire personnel, Faux si on est dans
        l'annuaire en ligne
    *type local*
        [Vrai, Faux]

        returns:
            True

    """

    # on efface l'écran et on affiche le titre
    minitel.efface()
    minitel.position(4, 4)
    minitel.couleur(caractere = 'bleu')
    minitel.effet(inversion=True)
    minitel.envoyer("Paramètre du service")

    # on affiche les paramètres
    y = 6
    for key in service:
        # on affiche pas l'id
        if key == 'id':
            continue
        if service[key]:
            minitel.position(6,y)
            minitel.couleur(caractere = 'bleu')
            minitel.envoyer(key)
            minitel.position(18,y)
            minitel.envoyer(str(service[key])[:22])
            y = y+1

    # On affiche le titre menu du service
    y = y+2
    minitel.position(4, y)
    minitel.couleur(caractere = 'bleu')
    minitel.effet(inversion=True)
    minitel.envoyer("Menu du service")

    # On crée le contenu du menu en fonction de l'annuaire courant
    if local:
        options = [
            "Consulter le service",
            "Editer le service",
            "Supprimer de l'annuaire",
            "Retourner au menu"
        ]
    else:
        options = [
            "Consulter le service",
            "Ajouter dans l'annuaire personnel",
            "Retourner au menu"
        ]

    # On affiche le menu
    menu = Menu(minitel, options, 6, y+1, grille = False)
    menu.affiche()

    if menu.executer():
        try:
            # On renvoit la sélection
            # ~ return menu.selection
            # on execute la tâche choisie dans le sous-menu services_consult
            if menu.selection == 0:
                # Consulter service
                services_connect(minitel, reseau, service)

                # Après la connexion, remettre deux trois trucs en ordre...
                minitel.configurer_clavier(etendu = True, curseur = False, minuscule = True)
                minitel.echo(False)
                minitel.curseur(False)

            elif menu.selection == 1:
                # Editer service
                minitel.position(1,0)
                minitel.couleur(caractere='vert')
                if local:
                    minitel.envoyer('Edition de service           ')
                    services_edit(minitel, service)
                else:
                    minitel.envoyer('Ajout du service...          ')
                    ajouter_service(service)

            elif menu.selection == 2 and local:
                # Supprimer service
                minitel.position(1,0)
                minitel.couleur(caractere='vert')
                minitel.envoyer('Suppression du service...    ')
                supprimer_service(service['id'])
            elif menu.selection == 2 or menu.selection == 3:
                # Retour menu
                minitel.position(1,0)
                minitel.couleur(caractere='vert')
                minitel.envoyer('Retour au menu...            ')

        except Exception as e:
            minitel.position(1,0)
            minitel.envoyer('ERREUR '+str(e))

    else:
        return True
