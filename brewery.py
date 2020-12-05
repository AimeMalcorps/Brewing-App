#!/usr/bin/env python

import os
import time
import glob
import sys
import pickle
import logging
import RPi.GPIO as GPIO

#Initialiser les sorties raspberry
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(17,GPIO.OUT)
GPIO.output(17,GPIO.LOW)

#detect sonde(a retrouver sur la raspberry)
fichier_sonde = '/sys/bus/w1/devices/XXXXXXXXXXXXXXX/w1_slave'

def read_temp_raw():
    f = open(fichier_sonde, 'r')
    lines = f.readlines()
    while len(lines) == 0:
        time.sleep(0.2)
        lines = f.readlines()
    f.close()
    return lines

def read_temp():
    lines = read_temp_raw()
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0
        return temp_c

def init_sonde():
    for i in range(5):
        temp = read_temp()
        time.sleep(0.2)
    return temp

class CountdownTask:

    def __init__(self):
        self._running = True

    def terminate(self):
        self._running = False
        GPIO.output(17,GPIO.LOW)

    def run(self, id):
        s = True
        #Pickle du temps restant
        heure_debut = "En chauffe"
        pickle.dump(heure_debut,open('debut.p', 'wb'))
        while self._running and s == True:
            recettes = pickle.load(open('recettes.p', 'rb'))
            recette = recettes[id - 1]
            i = pickle.load(open('cycletracker.p', 'rb'))
            temperature = recette['content{}'.format(i)]
            temperature = float(temperature)
            duree = recette['content{}'.format(i+1)]
            pickle.dump(duree,open('duree.p', 'wb'))
            duree = float(duree)*60
            temperature_reelle = init_sonde()

            while self._running and temperature_reelle < temperature:
                GPIO.output(17,GPIO.HIGH)
                time.sleep(5)
                temperature_reelle = read_temp()

            GPIO.output(17,GPIO.LOW)

            heure_debut = time.time()   #heure de début
            heure_fin = heure_debut + duree
            pickle.dump(heure_debut,open('debut.p', 'wb'))
            #Tant que le minuteur tourne
            while self._running and time.time() < heure_fin:
                temperature_reelle = read_temp()
                    #Analyse de temperature
                if temperature_reelle < temperature:
                    GPIO.output(17,GPIO.HIGH)
                else:
                    GPIO.output(17,GPIO.LOW)
                time.sleep(5)

            GPIO.output(17,GPIO.LOW)
            print("Programme terminé")
            heure_debut = "Cycle terminé"
            pickle.dump(heure_debut,open('debut.p', 'wb'))
            s = False
