#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Module de saisie du mot de passe WiFi"""

from minitel.ui.Menu import Menu
from parametres import (lire_reseau, ecrire_reseau)

def wifi_parametres(minitel, reseau):

    # on affiche les titres
    minitel.efface()
    minitel.position(4, 4)
    minitel.couleur(caractere = 'bleu')
    minitel.effet(inversion=True)
    minitel.envoyer("Masquer les mots de passe ?")
    minitel.position(4, 9)
    minitel.couleur(caractere = 'bleu')
    minitel.effet(inversion=True)
    minitel.envoyer("Connexion au démarrage ?")
    minitel.position(4, 14)
    minitel.couleur(caractere = 'bleu')
    minitel.effet(inversion=True)
    minitel.envoyer("Sauvegarder le réseau actuel ?")
    minitel.position(4, 19)
    minitel.couleur(caractere = 'bleu')
    minitel.effet(inversion=True)
    minitel.envoyer("Supprimer le réseau sauvegardé ?")

    options = [
        'Oui',    #0 - masquer
        'Non',    #1 - pas de masque
        '-',
        '-',
        '-',
        'Auto',   #5 - connexion auto
        'Manuel', #6 - connexion manuel
        '-',
        '-',
        '-',
        'Oui',   #10 - sauvegarder
        '-',
        '-',
        '-',
        '-',
        'Oui',   #15 - supprimer
    ]

    # on récupère les paramètres
    parametres = lire_reseau()

    # on affiche les réseaux courants associés au menu
    # et leurs mots de passe masqués si nécessaire
    minitel.position(18, 16)
    minitel.couleur(caractere = 'bleu')
    minitel.envoyer(reseau.nom)
    minitel.position(18, 17)
    minitel.couleur(caractere = 'bleu')
    if not reseau.masque_mdp:
        minitel.envoyer(reseau.mdp)
    else:
        minitel.envoyer('*' * len(reseau.mdp))
    minitel.position(18, 21)
    minitel.couleur(caractere = 'bleu')
    minitel.envoyer(parametres['nom'])
    minitel.position(18, 22)
    minitel.couleur(caractere = 'bleu')
    if not reseau.masque_mdp:
        minitel.envoyer(parametres['mdp'])
    else:
        minitel.envoyer('*' * len(parametres['mdp']))

    # on identifie les options actives    
    if parametres['masque_mdp']:
        options[0] = options[0] + ' (*)'
    else:
        options[1] = options[1] + ' (*)'

    if parametres['auto']:
        options[5] = options[5] + ' (*)'
    else:
        options[6] = options[6] + ' (*)'

    # on affiche le menu
    menu = Menu(minitel, options, 6, 5, grille = False)
    menu.affiche()
    
    if menu.executer():
        # on execute la selection
        if menu.selection == 0:
            parametres['masque_mdp'] = True
            reseau.masque_mdp = True
            minitel.position(1,0)
            minitel.envoyer('Masquage mdp activé...')

        elif menu.selection == 1:
            parametres['masque_mdp'] = False
            reseau.masque_mdp = False
            minitel.position(1,0)
            minitel.envoyer('Masquage mdp désactivé...')

        elif menu.selection == 5:
            parametres['auto'] = True
            minitel.position(1,0)
            minitel.envoyer('Connexion auto activé...')

        elif menu.selection == 6:
            parametres['auto'] = False
            minitel.position(1,0)
            minitel.envoyer('Connexion auto désactivé...')

        elif menu.selection == 10:
            parametres['nom'] = reseau.nom
            parametres['mdp'] = reseau.mdp
            minitel.position(1,0)
            minitel.envoyer('Sauvegarde du reseau...')

        elif menu.selection == 15:
            parametres['nom'] = ''
            parametres['mdp'] = ''
            minitel.position(1,0)
            minitel.envoyer('Suppression du reseau...')

        ecrire_reseau(parametres)
    
    else:
        minitel.position(1,0)
        minitel.envoyer('Retour au menu...                   ')

    return True
