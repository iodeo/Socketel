# Socketel

Portal to minitel webservices written in micropython for ESP32 microcontroller.

# What is this ?

Minitel services have been officialy terminated in 2012, making these robust terminals only good to be added to our mountains of electronics rubbish. But this was without counting on some amazing guys who have put online their own minitel services using voip and/or websockets. Thanks to them, anyone with a working minitel terminal (which is not so rare in french house attic), can still try the minitel experience !

One way to connect to the websocket services is to use a microcontroller with Wifi support connected to the DIN port of the Minitel. The microcontroller connects to the WiFi and acts as a gateway between the server and the minitel.

The present application provides a user interface to manage wifi connexion and call to minitel services.

# Ackonwledgments

Merci à l'Association du [Musée du Minitel et de la Télématique](https://www.museeminitel.fr/) et à tous les gens qui oeuvrent à faire vivre le minitel !

# Requirements

* ESP32 with micropython firmware v1.17 installed
* Minitel with "periinformatique" DIN port

# Screenshots 

![accueil](https://raw.githubusercontent.com/iodeo/Socketel/main/screenshots/socketel_accueil.jpg)

![menu](https://raw.githubusercontent.com/iodeo/Socketel/main/screenshots/socketel_menu.jpg)
