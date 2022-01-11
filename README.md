# Socketel

Portal to minitel webservices written in micropython for ESP32 microcontroller.

# What is this ?

Minitel services have been officialy terminated in 2012, making these robust terminals only good to be added to our mountains of electronics rubbish. But this was without counting on some amazing guys who have put online their own minitel services using voip and/or websockets. Thanks to them, anyone with a working minitel terminal (which is not so rare in french house attic), can still try the minitel experience !

One way to connect to the websocket services is to use a microcontroller with Wifi support connected to the DIN port of the Minitel. The microcontroller connects to the WiFi and acts as a gateway between the server and the minitel.

The present application provides a user interface to:
* manage minitel speed, 
* handle wifi connexion,
* consult online yellow pages of available minitel services
* consult and edit a local repertory of available services
* connect / disconnect minitel services

The application is provided as is with no warranty as per license terms

# Ackonwledgments

* L'Association du [Musée du Minitel et de la Télématique](https://www.museeminitel.fr/)
* zigazou pour sa bibliothèque [PyMinitel](https://github.com/Zigazou/PyMinitel), dont l'adaptation en micropython est disponible ici [µPyMinitel](https://github.com/iodeo/Minitel-ESP32/tree/main/upython/uPyMinitel)
* et tous les gens qui oeuvrent à faire vivre le minitel !

# Requirements

* ESP32 with micropython firmware v1.17 installed
* Minitel with "periinformatique" DIN port

For ESP32 programming with Thonny IDE guidances are provided in [hackaday project instructions](https://hackaday.io/project/180473/instructions)

# Screenshots 

![menu](https://raw.githubusercontent.com/iodeo/Socketel/main/screenshots/socketel_menu.jpg)
