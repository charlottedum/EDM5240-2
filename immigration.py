# coding: utf-8


# créer mon environnement virtuel:
    # virtualenv -p /usr/bin/python3 py3env
    
# Activer ensuite l'environnement virtuel:
    # source py3env/bin/activate

# Installer les modules externes:
    # sudo pip install requests
    # sudo pip install BeautifulSoup4
    
# Étape de l'importation des modules:
import csv
import requests
from bs4 import BeautifulSoup

# Voici l'URL de départ choisi pour le travail:
url = "http://www.cic.gc.ca/disclosure-divulgation/index-fra.aspx?dept=1&lang=fra&p=3&r=35"

# Je nomme le fichier csv dans lequel sera verser le contenu demandé:
fichier = "contrat-immigration.csv"

# Les entetes qui seront envoyés pendant le moissonnage des données seront:
entetes = {
    "User-Agent":"Charlotte Dumoulin - requête envoyée dans le cadre d'un cours de journalisme informatique à l'UQAM (EDM5240)",
    "From":"charlottedumoulin95@outlook.fr"
}

# J'identifie mes variables «contenu» et «page»:
contenu = requests.get(url, headers=entetes)
page = BeautifulSoup(contenu.text,"html.parser")

print(page)

# Création d'une variable compteur pour ne pas que lors du moissonnage
# Il nous sorte la ligne du tableau qui décrit les variables dans les colonnes
i = 0

# On crée une boucle pour obtenir dans une liste tous les éléments "html" de type "Tr" qui compose chacune
# des lignes du tableau choisi:
for ligne in page.find_all("tr"):
    if i != 0:
        print(ligne)

# Étape pour recueillir l'hyperlien, car on veut la sous-page qui nous fournira plus d'information sur le contrat
        lien = ligne.a.get("href")
        print(lien)

# Le lien n'est pas encore complet, on doit le compléter ainsi:
        hyperlien = "http://www.cic.gc.ca/" + lien
        print(hyperlien)

# Pour aller chercher notre contrat, on doit maintenant répéter l'étape de Soupe:
        contenu2 = requests.get(hyperlien, headers=entetes)
        page2 = BeautifulSoup(contenu2.text, "html.parser")
 
# Création de la liste où les infos sur le contrat seront jointes:   
        contrat = [ ]

# Le premier item qu'on met dans la liste est l'hyperlien:
        contrat.append(lien)

# Création d'une deuxième boucle pour pour recueillir chacun des items du tableau:   
        for item in page2.find_all("tr"):
            print(item)

# Mettre la condition suivante
# Si la cellule n'est pas du none, insérer son contenu dans la liste "contrat"
            if item.td is not None:
                contrat.append(item.td.text)

# Si ce n'est pas le cas, ajouter la cellule à la liste:
            else:
                contrat.append(None)
        
        print(contrat)

# Étape pour inscrire la liste contrat dans une nouvelle ligne d'un fichier csv: 
        immigration = open(fichier,"a")
        gouv = csv.writer(immigration)
        gouv.writerow(contrat)
        
# Étape pour augmenter le compteur de 1: 
    i += 1
