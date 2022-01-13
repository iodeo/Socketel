#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Module de connexion à un service

"""
import gc

def services_connect(minitel, reseau, service):
    """Permet de se connecter à un service avec le minitel
    et de gérer l'affichage et le clavier

        returns:
            False: Connexion impossible
            True:  Connexion établie et terminée normalement

    """
    # on verifie que la connexion wifi est établie
    if not reseau.isconnected():
        minitel.position(1,0)
        minitel.couleur(caractere='vert')
        minitel.envoyer('WiFi déconnecté !            ')
        return False
    
    # on verifie qu'on a bien une adresse de service
    try:
        uri = service['address']
    except KeyError:
        minitel.position(1,0)
        minitel.couleur(caractere='vert')
        minitel.envoyer('Adresse manquante !          ')
        return False

    # s'il n'y a pas de subprotocol, on met None
    if 'subprotocol' in service:
        subprotocol = service['subprotocol']
    else:
        subprotocol = None
        
    # on affiche les infos préalable
    minitel.efface('vraimenttout')
    minitel.position(1,0)
    minitel.couleur(caractere='vert')
    minitel.envoyer('Connexion au serveur')
    minitel.position(6,8)
    minitel.envoyer('Appuyer sur')
    minitel.position(6,10)
    minitel.effet(inversion = True)
    minitel.envoyer('Shift')
    minitel.effet(inversion = False)
    minitel.envoyer(' + ')
    minitel.effet(inversion = True)
    minitel.envoyer('ConnexionFin')
    minitel.position(6,12)
    minitel.envoyer('Pour démarrer la connexion')
    minitel.position(6,13)
    minitel.envoyer('et y mettre fin à tout moment')
    
    # on attends la touche de connexion
    while True:
        data = minitel.recevoir(nbytes = 4)
        if data == '\x13I': # SHIFT + CONNEXION_FIN
            minitel.position(1,0)
            minitel.couleur(caractere='vert')
            minitel.effet(clignotement = True)
            minitel.envoyer('Connexion au serveur...')
            break
        elif data == '\x13F': # SOMMAIRE
            # retour menu
            minitel.position(1,0)
            minitel.couleur(caractere='vert')
            minitel.envoyer('Retour au menu...            ')
            return True

    # on essaye de se connecter
    try:
        ws = reseau.ws_connect(uri, subprotocol)
    except OSError:
        minitel.position(1,0)
        minitel.couleur(caractere='vert')
        minitel.envoyer('Echec de la connexion !      ')
        return False

    # on efface l'écran et on laisse place au service
    minitel.efface('vraimenttout')
    minitel.configurer_clavier()
    
    # uwebsockets ne supportant pas la modification de la taille du buffer,
    # on reboucle manuellement la lecture du websocket en bypassant l'analyse
    # de l'en-tête de la trame (MemoryError observé pour size > 5000)
    buffer_size = 2048
    new_frame = True

    while True:
        
        # on nettoie la mémoire
        data = None
        gc.collect()
        
        # websocket > minitel
        try:
            if new_frame:
                # on lit les frames websockets
                data = ws.recv(max_size = buffer_size)
            else:
                # on bypass l'analyse de frame websocket si le msg n'a pas été lu en entier
                data = ws.sock.read(buffer_size)
        except:
            print('WS: unable to read frame. websocket is closed')
            ws.close()
            break
        if data:
            minitel.envoyer_brut(data)
            if len(data) == buffer_size:
                # la frame n'a probablement pas été lu en entier, on reboucle au cas où
                new_frame = False
                print('WS: received max_size')
                continue
            else:
                print('WS: received ' + str(len(data)) + ' bytes')
                new_frame = True
        else:
            new_frame = True

        # minitel > websocket
        data = minitel.recevoir(nbytes = 4)
        if data:
            if data == '\x13I': # SHIFT + CONNEXION_FIN
                ws.close()
                break
            else:
                ws.send(data)

    minitel.position(1,0)
    minitel.couleur(caractere='vert')
    minitel.envoyer('Déconnexion du service...        ')

    return True
