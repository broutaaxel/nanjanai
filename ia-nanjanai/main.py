


def main():
    print("salut")
    ouvrir = ["ouvre", "lance"]
    rechercher = ["recherche", "trouve sur"]
    fermer = ["tu peux disposer", "tais-toi", "salut"]
    demarer = ["nanjanaye", "nane janaye"]
    loop = True
    while loop:
        for ouverture in range(len(ouvrir)):
            if ouverture is not none:


def reco_vocale():
    print("je suis la reco vocale")
    r = sr.Recognizer()
    r.energy_threshold = 4000
    pas_compris = "Désolé, je n'ai pas compris ."
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source)
        r.pause_threshold = 0.7
        print(".... ")
        audio = r.listen(source)
        if internet():
            try:
                vocal = r.recognize_google(audio, language='fr-FR')
                print(vocal)
                return vocal
            except sr.UnknownValueError:
                assistant_voix(pas_compris)
        else:
            try:
                vocal = r.recognize_sphinx(audio, language='fr-fr')
                print(vocal)
                return vocal
            except sr.UnknownValueError:
                assistant_voix(pas_compris)


def application():
    print("je suis une application")

def wikipedia():
    print("je suis wikipedia")

def internet():
    print("je suis internet")






if __name__ == '__main__':
    main()
