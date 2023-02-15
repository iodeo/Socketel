#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Reseau est un module permettant de gérer la connexion WiFi

"""

import time
import network
import json
import urequests
import uwebsockets

class Reseau:
    """Une classe de gestion du WiFi pour ESP32

    Reseau se base sur l'objet <WLAN> de la bibliothèque network et inclus les
    attributs nécessaires pour la connexion / déconnexion à un réseau Wifi.

    Le Wifi est désactivé lorsqu'il n'est pas connecté.

    La connexion peut se faire automatiquement

    """
    def __init__(self, params = None):
        """Constructeur de la classe Reseau

        :param params:
            dictionnaire incluant 'nom', 'mdp', 'auto' et 'timeout_ms'
        :type params:
            dictionnaire
        :type nom:
            str
        :type mdp:
            str
        :type auto:
            booléen
        :type timeout_ms:
            int
        """

        # Initialisation des attributs
        # nom: ssid du réseau
        # mdp: mot de passe du réseau
        # auto: connexion automatique à la déclaration d'un objet Reseau
        # timeout_ms: timeout lors d'une tentative de connexion

        if params:
            self.nom = params['nom']
            self.mdp = params['mdp']
            self.auto = params['auto']
            self.timeout_ms = params['timeout_ms']
            self.masque_mdp = params['masque_mdp']
        else:
            self.nom = None
            self.mdp = None
            self.auto = False
            self.timeout_ms = 10000
            self.masque_mdp = True

        self.wlan = network.WLAN(network.STA_IF)

        if self.auto:
            self.connexion()

    def isconnected(self):
        return self.wlan.isconnected()

    def connexion(self):
        """Tente de se connecter au Wifi avec les identifiants fournis
        avec un timeout.

        returns:
            False si la connexion a échouée
            True si la connexion est établie

        """

        assert isinstance(self.nom, str)
        assert isinstance(self.mdp, str)
        assert isinstance(self.timeout_ms, int)

        if not self.wlan.active():
            self.wlan.active(True)
            self.wlan.ifconfig('dhcp')

        if not self.isconnected():
            try:
                self.wlan.connect(self.nom, self.mdp)
            except OSError:
                self.wlan.active(False)
                return False

            start_ms = time.ticks_ms()
            while not self.isconnected():
                time_ms = time.ticks_diff(time.ticks_ms(), start_ms)
                if  time_ms > self.timeout_ms:
                    break

            ifconfigdata = self.wlan.ifconfig()
            print(ifconfigdata)

            if not self.isconnected():
                self.wlan.active(False)
                return False

            # now disconnect, disabling DHCP, and reconnect. grr grr grr.
            self.wlan.disconnect()
            self.wlan.ifconfig(ifconfigdata)
            try:
                self.wlan.connect(self.nom, self.mdp)
            except OSError:
                self.wlan.active(False)
                return False

            start_ms = time.ticks_ms()
            while not self.isconnected():
                time_ms = time.ticks_diff(time.ticks_ms(), start_ms)
                if  time_ms > self.timeout_ms:
                    break

            if not self.isconnected():
                self.wlan.active(False)
                return False

        return True

    def deconnexion(self):

        if self.isconnected():
            self.wlan.disconnect()

        if self.wlan.active():
            self.wlan.active(False)

        return True

    def scan(self):
        if not self.wlan.active():
            self.wlan.active(True)

        return self.wlan.scan()

    def get(self, url):
        if self.isconnected():
            return urequests.get(url)
        return None

    def ws_connect(self, uri, subprotocol = None):
        ws = uwebsockets.connect(uri, subprotocol)
        ws.setblocking(False)
        return ws
