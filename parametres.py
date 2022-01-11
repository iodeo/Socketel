#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Parametres est un module regroupant l'accés aux paramètres de l'application
dans les fichiers de sauvegarde associés

"""

import json

def lire_vitesse(chemin = '/fichiers/vitesse.json'):
    """ Récupère les paramètres de vitesse de communication
    avec le minitel

    :params chemin:
        chemin vers le fichier de sauvegarde
    :type chemin:
        str

    """
    try:
        fichier = open(chemin,'r')
    except OSError:
        # le fichier n'existe pas, on le crée
        params = {'vitesse': 1200, 'auto': False}
        ecrire_vitesse(params)
        return params

    params = json.load(fichier)
    fichier.close()

    assert 'vitesse' in params
    assert isinstance(params['vitesse'], int)
    assert 'auto' in params
    assert params['auto'] in [True, False]

    return params

def ecrire_vitesse(params, chemin = '/fichiers/vitesse.json'):
    """ Sauvegarde les paramètres de vitesse de communication
    avec le minitel

    :param params:
        dictionnaire incluant 'vitesse' et 'auto'
    :type params:
        dict

    :params chemin:
        chemin vers le fichier de sauvegarde
    :type chemin:
        str
        
    """
    
    assert 'vitesse' in params
    assert isinstance(params['vitesse'], int)
    assert 'auto' in params
    assert params['auto'] in [True, False]

    fichier = open(chemin,'w')
    json.dump(params, fichier)
    fichier.close()
    
    return True

def lire_reseau(chemin = '/fichiers/reseau.json'):
    """ Récupère les paramètres réseau

    :params chemin:
        chemin vers le fichier de sauvegarde
    :type chemin:
        str

    """
    try:
        fichier = open(chemin,'r')
    except OSError:
        
        # le fichier n'existe pas, on le crée
        params = {'nom': '', 'mdp': '', 'auto': False, 'timeout_ms': 10000,
                  'masque_mdp' : True}
        ecrire_reseau(params)
        return params

    params = json.load(fichier)
    fichier.close()

    assert 'nom' in params
    assert isinstance(params['nom'], str)
    assert 'mdp' in params
    assert isinstance(params['mdp'], str)
    assert 'auto' in params
    assert params['auto'] in [True, False]
    assert 'timeout_ms' in params
    assert isinstance(params['timeout_ms'], int)
    assert 'masque_mdp' in params
    assert params['masque_mdp'] in [True, False]

    return params

def ecrire_reseau(params , chemin = '/fichiers/reseau.json'):
    """ Sauvegarde les paramètres réseau
    
    :param params:
        dictionnaire incluant 'nom', 'mdp', 'auto' et 'timeout_ms'
    :type params:
        dict

    :params chemin:
        chemin vers le fichier de sauvegarde
    :type chemin:
        str

    """
    
    assert 'nom' in params
    assert isinstance(params['nom'], str)
    assert 'mdp' in params
    assert isinstance(params['mdp'], str)
    assert 'auto' in params
    assert params['auto'] in [True, False]
    assert 'timeout_ms' in params
    assert isinstance(params['timeout_ms'], int)
    assert 'masque_mdp' in params
    assert params['masque_mdp'] in [True, False]

    fichier = open(chemin,'w')
    json.dump(params, fichier)
    fichier.close()
    
    return True

def lire_annuaire(chemin = '/fichiers/annuaire.json'):
    """ Récupère tout l'annuaire (url + personnel)

    :params chemin:
        chemin vers le fichier de sauvegarde
    :type chemin:
        str

    """
    try:
        fichier = open(chemin,'r')
    except OSError:
        # le fichier n'existe pas, on le crée
        annuaire = creer_annuaire()
        return annuaire

    annuaire = json.load(fichier)
    fichier.close()

    assert 'url' in annuaire
    assert isinstance(annuaire['url'], str)
    assert 'personnel' in annuaire
    assert isinstance(annuaire['personnel'], list)

    return annuaire

def lire_annuaire_url(chemin = '/fichiers/annuaire.json'):
    """ Récupère l'url de l'annuaire en ligne

    :params chemin:
        chemin vers le fichier de sauvegarde
    :type chemin:
        str

    """
    try:
        fichier = open(chemin,'r')
    except OSError:
        # le fichier n'existe pas, on le crée
        annuaire = creer_annuaire()
        return annuaire['url']

    annuaire = json.load(fichier)
    fichier.close()

    assert 'url' in annuaire
    assert isinstance(annuaire['url'], str)
    
    return annuaire['url']

def lire_annuaire_personnel(chemin = '/fichiers/annuaire.json'):
    """ Récupère l'annuaire personnel

    :params chemin:
        chemin vers le fichier de sauvegarde
    :type chemin:
        str

    """
    try:
        fichier = open(chemin,'r')
    except OSError:
        # le fichier n'existe pas, on le crée
        annuaire = creer_annuaire()
        return annuaire['personnel']

    annuaire = json.load(fichier)
    fichier.close()

    assert 'personnel' in annuaire
    assert isinstance(annuaire['personnel'], list)
    
    return annuaire['personnel']

def creer_annuaire(chemin = '/fichiers/annuaire.json'):
    """ Créer le fichier avec l'annuaire par défaut

    :params chemin:
        chemin vers le fichier de sauvegarde
    :type chemin:
        str

    """
    annuaire = {
        'url': 'http://teletel.org/minitel-yp.json',
        'personnel': []
    }
    
    ecrire_annuaire(annuaire)
    
    return annuaire

def ecrire_annuaire(annuaire, chemin = '/fichiers/annuaire.json'):
    """ Ecrit l'annuaire passé en argument dans le fichier spécifié

    :params annuaire:
        dictionnaire incluant 'url', 'personnel'
    :type params:
        dict
    
    :params chemin:
        chemin vers le fichier de sauvegarde
    :type chemin:
        str
    """

    assert 'url' in annuaire
    assert isinstance(annuaire['url'], str)
    assert 'personnel' in annuaire
    assert isinstance(annuaire['personnel'], list)

    fichier = open(chemin,'w')
    json.dump(annuaire, fichier)
    fichier.close()

    return True

def ajouter_service(service, chemin = '/fichiers/annuaire.json'):
    """ Ajoute un service de l'annuaire en ligne dans l'annuaire
    personnel

    :params service:
        dictionnaire incluant au minimum 'id', 'name' & 'address'
    :type params:
        dict
    
    :params chemin:
        chemin vers le fichier de sauvegarde
    :type chemin:
        str
        
    """
    assert 'id' in service
    assert 'name' in service
    assert isinstance(service['name'], str)
    assert 'address' in service
    assert isinstance(service['address'], str)

    annuaire = lire_annuaire(chemin)
    annuaire['personnel'].append(service)
    
    i = 0
    for service in annuaire['personnel']:
        service['id'] = i
        i = i+1

    ecrire_annuaire(annuaire)

    return True

def supprimer_service(id_service, chemin = '/fichiers/annuaire.json'):
    """ Supprime un service de l'annuaire personnel

    :params id_service:
        id du service à supprimer
    :type id_service:
        str

    :params chemin:
        chemin vers le fichier de sauvegarde
    :type chemin:
        str

    """

    annuaire = lire_annuaire(chemin)

    index = 0
    while index < len(annuaire['personnel']):
        if id_service == annuaire['personnel'][index]['id']:
            break
        index = index + 1

    if index == len(annuaire['personnel']):
        return False

    annuaire['personnel'].pop(index)
    
    ecrire_annuaire(annuaire)

    return True

def modifier_service(service, chemin = '/fichiers/annuaire.json'):
    """ Met à jour les paramètres d'un service

    :params service:
        dictionnaire incluant au minimum 'id', 'name' & 'address'
    :type service:
        dict

    :params chemin:
        chemin vers le fichier de sauvegarde
    :type chemin:
        str

    """

    annuaire = lire_annuaire(chemin)

    index = 0
    while index < len(annuaire['personnel']):
        if service['id'] == annuaire['personnel'][index]['id']:
            break
        index = index + 1

    if index == len(annuaire['personnel']):
        return False

    annuaire['personnel'][index] = service

    ecrire_annuaire(annuaire)

    return True
