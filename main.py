
from urllib.request import urlopen
from googletrans import Translator
from random import choice
import speech_recognition as sr
import pyttsx3
import subprocess
import wolframalpha
import webbrowser
import wikipedia
import random
from pymongo import MongoClient
from configparser import ConfigParser
import urllib

from dearpygui.core import *
from dearpygui.simple import *


""" the portion is for the config file  """

file = 'config.ini'
config = ConfigParser()
config.read(file)

cluster = MongoClient(config['credentials']['bdd'])
db = cluster[config['credentials']['cluster']]
collection = db[config['credentials']['collection']]

"""post = {"name": "jho"}

collection.insert_one(post)"""

def assistant_voix(sortie):
    if sortie != None:
        voix = pyttsx3.init()
        print("Nanjanai : " + sortie)
        voix.say(sortie)
        voix.runAndWait()

def internet():
    try:
        urlopen('https://www.google.com', timeout=1)
        print("Connecté")
        return True
    except:
        print("Déconnecté")
        return False


def reconnaissance():
    r = sr.Recognizer()
    r.energy_threshold = 4000
    pas_compris = "Désolé, je n'ai pas compris ."
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source)
        r.pause_threshold = 0.7
        print("... ")
        audio = r.listen(source)
        if internet():
            try:
                vocal = r.recognize_google(audio, language = 'fr-FR')
                print(vocal)
                return vocal
            except sr.UnknownValueError:
                assistant_voix(pas_compris)
        else:
            try:
                vocal = r.recognize_sphinx(audio, language = 'fr-fr')
                print(vocal)
                return vocal
            except sr.UnknownValueError:
                assistant_voix(pas_compris)

def application(entree):
    if entree != None:
        dico_apps = {
            "note": ["notepad","note pad"],
            "sublime": ["sublime","sublime texte"],
            "obs": ["obs","obs capture","capture l'ecran"],
            "edge": ["microsoft edge","edge"],
            "rocket": ["Rocket League", "rocket", "rocketleague"]
        }
        fini = False
        while not fini:
            for x in dico_apps["note"]:
                if x in entree.lower():
                    assistant_voix("Ouverture de Notepad .")
                    subprocess.Popen('C:\\Windows\\System32\\notepad.exe')
                    fini = True
            for x in dico_apps["sublime"]:
                if x in entree.lower():
                    assistant_voix("Ouverture de Sublime Text .")
                    subprocess.Popen('C:\\Program Files\\Sublime Text 3\\sublime_text.exe')
                    fini = True
            for x in dico_apps["obs"]:
                if x in entree.lower():
                    assistant_voix("Ouverture de Obs .")
                    subprocess.Popen('C:\\Program Files\\obs-studio\bin\\64bit\\obs64')
                    fini = True
            for x in dico_apps["edge"]:
                if x in entree.lower():
                    assistant_voix("Ouverture de Edge .")
                    subprocess.Popen('C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe')
                    fini = True
            for x in dico_apps["rocket"]:
                if x in entree.lower():
                    assistant_voix("Ouverture de Rocket .")
                    subprocess.Popen('B:\\01-Game\\SteamLibrary\\steamapps\\common\\rocketleague\\Binaries\\Win64\\RocketLeague.exe')
                    fini = True
            fini = True

def calcul(entree):
    if entree != None:
        traducteur = Translator()
        traduction = traducteur.translate(text = entree, dest = "en").text
        app_id = "L5H3JP-ERXK3EVKGW"
        client = wolframalpha.Client(app_id) 
        res = client.query(traduction) 
        try:
            reponse = next(res.results).text
            traduction_reponse = traducteur.translate(text = reponse, dest = "fr").text
            assistant_voix("le résultat est %d" %(traduction_reponse))
        except:
            assistant_voix("Il y'a eu une erreur, désolé")

def compliment(entree):
    if entree != None:
        liste_compliment = ["tu es le plus beau specimen que j'ai vu de ma vie", "tu es vraiment un bg extrême !",
                            "oulala votre êtes tellement beau que j'ai cru que c'était un mirage",
                            "votre amitié est une oasis dans le desert de mes relations",
                            "tu es un rayon de soleil pour mes jours sans lumières ",
                            "tu es les étoiles de ma nuit sans sommeil",
                            "ton sourir éclaire mes journées",
                            "tu comme le soleil tu es là même quand on ne te vois pas",
                            "un aveugle retrouverait la vue rien que pour te voir",
                            "tu es une bouffé d'ai pour mes ventillateur",
                            "tu es mon nerd facial c'est grâce à toi que je souris",
                            "On m'a dit de faire le tour du monde et j'ai tourné autour de toi",
                            "tu es comme ma jugulaire si l'on me coupe de toi je ne vie plus"]

        assistant_voix(random.choice(liste_compliment))

def enregistrement_du_nom(entree):
    if entree != None:
        nom = entree.replace("je m'appelle", "")
        filter = {"name": nom}
        finded = []
        for document in collection.find(filter):
            finded.append(document)

        if len(finded) != 0:
            assistant_voix("ça fait plaisir de vous revoir humain " + nom + ". Que puis-je faire pour vous ?")
        else:
          collection.insert_one({"name": nom})
          assistant_voix("Bienvenue humain" + nom + ", je tâcherai de me souvenir de vous la prochaine fois. Je vous ecoute humain" + nom )


def sur_le_net(entree):
    if entree != None:
        if "youtube" in entree.lower(): 
            indx = entree.lower().split().index("youtube") 
            recherche = entree.lower().split()[indx + 1:]
            if len(recherche) != 0:
                assistant_voix("recherche sur YouTube .")
                webbrowser.open("http://www.youtube.com/results?search_query=" + "+".join(recherche), new = 2)
        elif "wikipédia" in entree.lower(): 
            wikipedia.set_lang("fr")
            try:
                recherche = entree.lower().replace("cherche sur wikipédia","")
                if len(recherche) != 0:
                    resultat = wikipedia.summary(recherche, sentences = 1)
                    assistant_voix("recherche sur Wikipédia .")
                    assistant_voix(resultat)
            except:
                assistant_voix("Désolé, aucune page trouvée .") 
        else: 
            if "google" in entree.lower():
                indx = entree.lower().split().index("google") 
                recherche = entree.lower().split()[indx + 1:]
                if len(recherche) != 0:
                    assistant_voix("recherche sur Google .")
                    webbrowser.open("https://www.google.com/search?q=" + "+".join(recherche), new = 2)
            elif "cherche" in entree.lower() or "recherche" in entree.lower():
                indx = entree.lower().split().index("cherche") 
                recherche = entree.lower().split()[indx + 1:]
                if len(recherche) != 0:
                    assistant_voix("recherche par défaut .")
                    webbrowser.open("https://www.google.com/search?q=" + "+".join(recherche), new = 2)
            elif "recherche" in entree.lower():
                    indx = entree.lower().split().index("recherche")
                    recherche = entree.lower().split()[indx + 1:]
                    if len(recherche) != 0:
                        assistant_voix("recherche sur Google .")
                        webbrowser.open("http://www.google.com/search?q="+"+".join(recherche), new = 2)

def main():
    assistant_voix("Bonjour. Je m'appelle Nanejanaille, c'est moi qui vais vous servir. Comment vous appelez-vous ? ")
    fermer = ["arrête-toi","tais-toi"]
    ouvrir = ["ouvre","ouvrir"]
    cherche = ["cherche sur youtube","cherche sur google","cherche sur wikipédia","cherche"]
    calculs = ["calcule la somme de","calcule la différence de"," calcule   le produit de","calcule le quotient de","calcule"]
    flaterie = ["complimente moi", "fais-moi des compliment"]
    nom = ["je m'appelle", "mon nom est", "mon prénom est"]
    actif = True
    while actif:
        if (entree := reconnaissance()) is not None:
            for x in range(len(fermer)):
                if fermer[x] in entree.lower():
                    assistant_voix("A bientôt humain.")
                    actif = False
            for x in range(len(ouvrir)):
                if ouvrir[x] in entree.lower():
                    application(entree)
                    break
            for x in range(len(cherche)):
                if cherche[x] in entree.lower():
                    sur_le_net(entree)
                    break
            for x in range(len(calculs)):
                if calculs[x] in entree.lower():
                    calcul(entree)
                    break
            for x in range(len(flaterie)):
                if flaterie[x] in entree.lower():
                    compliment(entree)
            for x in range(len(nom)):
                if nom[x] in entree.lower():
                    enregistrement_du_nom(entree)



if __name__ == '__main__':
    main()