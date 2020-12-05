# Brewing-App

Projet réalisé pour la création d'une micro-brasserie.
L'objectif est d'automatiser une cuve de brassage, au travers d'un site web responsif avec Bootstrap.

Pour faire fonctionner le programme, vous aurez besoin d'une Raspberry Pi et une sonde DS-18B20.
Sur le GPIO-17 de la Raspberry Pi, est branché un relais qui commandera les résistances de la cuve de brassage.
Vous pouvez changer de GPIO ou en utiliser d'autres en modifiant le fichier 'brewery.py'.

Pour lancer le serveur, modifiez l'adresse IP en fin de script 'main.py'.

Un fois sur le site, vous pourrez créer une nouvelle recette, composée des trois cycles de brassage de votre choix.
Vous verrez la température et le timer s'actualiser via une fonction JavaScript.

Lorsqu'un des cycles se termine, la résistance se coupe vous permettant d'apporter les modification à votre moût.

Bon brassage !

