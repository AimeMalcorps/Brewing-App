# Brewing-App


Projet réalisé pour la création d'une micro-brasserie.
L'objectif est d'automatiser une cuve de brassage, au travers d'un site web responsif avec Bootstrap.

Pour faire fonctionner le programme, vous aurez besoin d'une Raspberry Pi et une sonde DS-18B20.
Sur le GPIO-17, est branché un relais qui commandera les résistances de la cuve de brassage.
Vous pouvez changer de GPIO ou en utiliser d'autres en modifiant le fichier 'brewery.py'.

Pour lancer le serveur Flask, modifiez l'adresse IP en fin de script 'main.py'.

Un fois sur le site, vous pourrez créer une nouvelle recette, composée des trois cycles de brassage de votre choix.
Vous verrez la température et le timer s'actualiser via une fonction JavaScript.

Lorsqu'un des cycles se termine, la résistance se coupe vous permettant d'apporter les modification à votre moût.

Bon brassage !

_______________________________________________________________


[ENGLISH VESION]

This project was created for a micro-brewery.
The purpose is to control a brewing tank through a responsive website using Bootstrap.

In order to run the program you'll need a Raspberry Pi and a DS-18B20 sensor.
On GPIO-17, an electric relay is plugged in to command the heating elements.
You can change the GPIO or use more of them by editing the 'brewery.py' file.

To run the Flask server simply modify the IP adress at the end of the 'main.py' file.

Once on the web site, you can create a new recipe, composed of three brewing cycles.
You'll see the temperature and the timer update through a JavaScript function.

When a brewing cycle ends, the heating elements will be turned off, giving you the time to process your brew. 

Happy Brewing !
