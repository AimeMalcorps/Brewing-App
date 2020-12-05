#coding: utf8

from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime
import pickle
import os
import time
import glob
import sys
import logging
import brewery
import threading

#Initialisation des variables
c = brewery.CountdownTask()
i = 1
pickle.dump(i,open('cycletracker.p', 'wb'))

app = Flask(__name__)

@app.context_processor
def inject_now():
    return {'now': datetime.now()}

@app.route('/')
def home():
    try:
        recettes = pickle.load(open('recettes.p', 'rb'))
        return render_template('home.html', recettes=recettes)
    except :
        return render_template('nouvelle_recette.html')

@app.route('/continue/<int:id>')
def cycleNext(id):
    c.terminate()
    x = 0
    while x != "Cycle terminé":
        time.sleep(1)
        x = pickle.load(open('debut.p','rb'))
    i = pickle.load(open('cycletracker.p', 'rb'))
    i = i + 2
    if i > 5:
        return render_template('fini.html')
    pickle.dump(i,open('cycletracker.p', 'wb'))
    return redirect(url_for('.start', id=id))

@app.route('/start/<int:id>')
def start(id):
    c.__init__()
    t = threading.Thread(target = c.run, args=(id, ))
    t.start()
    return redirect(url_for('.recette_start', id=id))

@app.route('/cycle/<int:id>')
def recette_start(id):
    i = pickle.load(open('cycletracker.p', 'rb'))
    temps_debut = pickle.load(open('debut.p','rb'))
    recettes = pickle.load(open('recettes.p', 'rb'))
    recette = recettes[id - 1]
    temp = recette.get("content{}".format(i))
    duree = recette.get("content{}".format(i+1))
    if i == 3:
        i = 2
    if i == 5:
        i = 3
    if type(temps_debut) == str:
        temps_restant = temps_debut
    if type(temps_debut) == float:
        temps_restant = time.strftime("%M:%S",time.localtime((temps_debut + float(recette['total'])*60) - time.time()))
    temperature_reelle=round(brewery.read_temp(),2)
    return render_template('recette_start.html', recette=recette, temperature_reelle=temperature_reelle,
                            temps_restant=temps_restant,temp=temp,duree=duree, i=i, id=id)

@app.route('/cycle/actu')
def liretemperature():
    t = round(brewery.read_temp(),2)
    t = str(t)
    return t

@app.route('/cycle/timer')
def liretemps():
    temps_debut = pickle.load(open('debut.p','rb'))
    duree = pickle.load(open('duree.p','rb'))
    if type(temps_debut) == str:
        n = temps_debut
    if type(temps_debut) == float:
        n = time.strftime("%M:%S",time.localtime((temps_debut + float(duree)*60) - time.time()))
    return n


@app.route('/annule')
def annule():
    c.terminate()
    i = 1
    pickle.dump(i,open('cycletracker.p', 'wb'))
    return redirect(url_for('.recette_annule'))

@app.route('/recette/annule')
def recette_annule():
    return render_template('stop.html')

@app.route('/shutdown')
def shutdown():
    return render_template('shutdown.html')

@app.route('/turnoff')
def turnoff():
    os.system('sudo halt')
    recettes = pickle.load(open('recettes.p', 'rb'))
    return render_template('home.html', recettes=recettes)

@app.route('/recette/<int:id>')
def recette_show(id):
    recettes = pickle.load(open('recettes.p', 'rb'))
    recette = recettes[id - 1]
    return render_template('recette_show.html', recette=recette)

@app.route('/delete/<int:id>')
def delete_recette(id):
    recettes = pickle.load(open('recettes.p', 'rb'))
    del recettes[id - 1]
    for recette in recettes:
        recette['id'] = recette['id'] - 1
        if recette['id'] == 0:
            recette['id'] = recette['id'] + 1
    if len(recettes) > 0 :
        pickle.dump(recettes,open('recettes.p', 'wb'))
    else :
        os.remove("recettes.p")
    return render_template('delete.html')


@app.route('/nouvellerecette', methods=['GET','POST'])
def nouvelle_recette():
    if request.method == "GET":
        return render_template('nouvelle_recette.html')
    if request.method == "POST":
        try:
            recettes = pickle.load(open('recettes.p', 'rb'))
        except:
            recettes = []
        duree_totale=(int(request.form.get('duree1')) + int(request.form.get('duree2')) + int(request.form.get('duree3')))
        temperature1={'id': len(recettes)+1 , 'titre': request.form.get('nomrecette'),
                    'content1': request.form.get('temperature1'), 'content2': request.form.get('duree1'),
                    'content3': request.form.get('temperature2'), 'content4': request.form.get('duree2'),
                    'content5': request.form.get('temperature3'), 'content6': request.form.get('duree3'),
                    'total' : duree_totale,
                    }

        recettes.append(temperature1)
        pickle.dump(recettes,open('recettes.p', 'wb'))

        return render_template('nouvelle_recette_view.html', temperature1=temperature1, duree_totale=duree_totale)



@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/about')
def about():
    return render_template('about.html')

#Rentrer l'IP voulue
if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')
