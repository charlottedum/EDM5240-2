# coding: utf-8

import csv
import requests
from bs4 import BeautifulSoup

# Le site que tu as choisi est difficile à moissonner. Je t'explique pourquoi et j'offre une solution de contournement.

# POURQUOI? QUEL EST LE PROBLÈME?
# Quand on va sur cette adresse:
url = "http://www.cic.gc.ca/disclosure-divulgation/index-fra.aspx?dept=1&lang=fra&p=3&r=35"
# On voit que seulement les 10 premiers contrats sont affichés.
# Quand on clique sur «Suivant» pour faire afficher les 10 contrats suivants, ou quand on choisit de faire afficher 100 entrées, l'URL de la page ne change pas...
# C'est un problème pour le journaliste moissonneur, car on se base sur l'URL pour faire notre moissonnage. Si on a besoin de moissonner plusieus pages, on veut que leurs URLs changent... Mais si elles ne changent pas, on est coincés...

# LA SOLUTION, ICI?
# J'ai remarqué que lorsque je clique sur un nom de compagnie pour avoir les numéros de contrat, la seule chose qui change est un numéro à la fin. Voici deux exemples:
exemple1 = "http://www.cic.gc.ca/disclosure-divulgation/index-fra.aspx?dept=1&lang=fra&p=4&r=35&c=347"
exemple2 = "http://www.cic.gc.ca/disclosure-divulgation/index-fra.aspx?dept=1&lang=fra&p=4&r=35&c=324"

# Je suis allé voir le trimestre le plus récent et j'ai remarqué le même pattern:
exemple3 = "http://www.cic.gc.ca/disclosure-divulgation/index-fra.aspx?dept=1&lang=fra&p=4&r=50&c=3160"

# J'ai remarqué, aussi, que la partie «&r=» changeait en fonction du trimestre. J'ai enlevé cette partie de l'URL, et ça fonctionne quand même, autant pour les contrats de 2016 que pour les contrats de 2012:
exemple4 = "http://www.cic.gc.ca/disclosure-divulgation/index-fra.aspx?dept=1&lang=fra&p=4&c=3160"
exemple5 = "http://www.cic.gc.ca/disclosure-divulgation/index-fra.aspx?dept=1&lang=fra&p=4&c=347"

# Alors la solution serait de faire une boucle qui passe tous les numéros de 1 jusqu'au plus grand (ici, on va y aller avec 3200 comme limite supérieure)
# Comme ça, on devrait ramasser tous les contrats de Citoyenneté et Immigration Canada, depuis le début.

fichier = "contrat-immigration-JHR.csv"

entetes = {
    "User-Agent":"Charlotte Dumoulin - requête envoyée dans le cadre d'un cours de journalisme informatique à l'UQAM (EDM5240)",
    "From":"charlottedumoulin95@outlook.fr"
}

# La boucle commence ici:

for code in range(1,3201):
    code = str(code) # Ici, il faut transformer la variable «code», qui est un nombre, en un texte (string) afin de pouvoir l'ajouter à l'URL
    url = "http://www.cic.gc.ca/disclosure-divulgation/index-fra.aspx?dept=1&lang=fra&p=4&c=" + code
    # print(url)

    contenu = requests.get(url, headers=entetes)
    page = BeautifulSoup(contenu.text,"html.parser")

    # Comme certains codes ne correspondent à aucun contrat, il faut d'abord vérifier si on a un contrat qui s'affiche.
    # On le fait en vérifiant si la page qu'on obtient contient un élément de type <table>

    if page.table is not None:
        contrat = []
        contrat.append(code)
        contrat.append(url)
        for item in page.find_all("tr"):
            # print(item.td.text)
            contrat.append(item.td.text)

        print(contrat)

        immigration = open(fichier,"a")
        gouv = csv.writer(immigration)
        gouv.writerow(contrat)

    # Je ne mets pas de «else», puisque s'il n'y a pas de contrat, on n'a pas besoin de rien conserver