#!/usr/bin/env python
# coding: utf-8

# In[3]:

import streamlit as st

st.title('Classsification des mineraux')
st.text('Veuillez saisir le nom du mineral que vous voulez classifier: ')


# formule_chimique = st.text_input("Saisissez le nom ici:")

# Display the input text
# st.write("You entered:", user_input)


def analyse_formule_chimique(formule_chimique):
    liste_caracteres = []
    i = 0

    while i < len(formule_chimique):
        caractere = formule_chimique[i]

        if caractere.isalpha():
            # Si le caractère est alphabétique, c'est potentiellement le début d'un symbole chimique
            symbole_chimique = caractere

            # Utiliser itertools.takewhile pour obtenir les caractères suivants en minuscule ou les chiffres
            from itertools import takewhile
            symbole_chimique += ''.join(takewhile(lambda c: c.islower() or c.isdigit(), formule_chimique[i + 1:]))
            liste_caracteres.append(symbole_chimique)

            i += len(symbole_chimique)

        elif caractere.isdigit():
            # Si le caractère est un chiffre, utiliser itertools.takewhile pour former un nombre
            from itertools import takewhile
            nombre = caractere + ''.join(takewhile(lambda c: c.isdigit(), formule_chimique[i + 1:]))
            liste_caracteres.append(nombre)

            i += len(nombre)
        elif caractere == '(' or caractere == ')':
            # Si le caractère est '(' ou ')', ne pas l'ajouter à la liste
            i += 1

        else:
            # Si le caractère n'est ni alphabétique ni un chiffre, l'ajouter à la liste directement
            liste_caracteres.append(caractere)
            i += 1

    return liste_caracteres




def trouver_cle_par_element(formule_chimique, gc):
    # Appliquer la fonction analyse_formule_chimique pour obtenir la liste résultante
    resultat = analyse_formule_chimique(formule_chimique)
# Extraire les premiers éléments de chaque liste associée aux clés du dictionnaire gc
    valeurs_premieres = set(map(lambda valeurs: valeurs[0], gc.values()))

    # Initialiser un ensemble pour stocker les clés correspondantes aux éléments trouvés
    cles_trouvees = set()
    #print(valeurs_premieres)

    # Parcourir la liste résultante
    for element in resultat:
        # Vérifier si l'élément est présent dans la liste des premiers éléments
        if element in valeurs_premieres:
            # Si oui, rechercher la ou les clés associées à cet élément
            for cle, valeurs in gc.items():
                if element == valeurs[0]:
                    cles_trouvees.add(cle)  # Utiliser add pour ajouter des éléments à un ensemble

    return list(cles_trouvees)  # Convertir l'ensemble en liste avant de renvoyer

import pandas as pd





def verifier_formule_chimique(base_de_donnees_csv, formule_chimique):
    # Charger la base de données depuis le fichier CSV
    try:
        df = pd.read_csv(base_de_donnees_csv)
    except FileNotFoundError:
        return "Fichier CSV introuvable"
    
    
    if formule_chimique in df['IMA Chemistry (concise)'].values:
        nom_formule = df[df['IMA Chemistry (concise)'] == formule_chimique]['Mineral Name'].iloc[0]
        return nom_formule
    else : 
        return False


def trouver_formule_chimique_par_nom(base_de_donnees_csv, nom_mineral):
    try:
        df = pd.read_csv(base_de_donnees_csv)
    except FileNotFoundError:
        return "Fichier CSV introuvable"
    
    # Vérifier si le nom du minéral est présent dans la base de données
    if nom_mineral in df['Mineral Name'].values:
        formule_chimique = df[df['Mineral Name'] == nom_mineral]['IMA Chemistry (concise)'].iloc[0]
        return formule_chimique
    else:
        return False






def map_cles_aux_categories(resultat_cles):
    categories = {
        "Sulfures-Sulfosels": ["Sulfure-Sulfosels1", "Sulfure-Sulfosels2", "Sulfure-Sulfosels3", "Sulfure-Sulfosels4", "Sulfure-Sulfosels5"],
        "Halogenures": ["Halogenure1", "Halogenure2", "Halogenure3", "Halogenure4"],
        "Oxydes-Hydroxydes": ["Oxydes-Hydroxydes"], 
        "Carbonates": ["Carbonates", "Borates", "Nitrates"],
        "Sulfates": ["Sulfates", "Chromates", "Molybdates", "Tungstates"],
        "Phosphates": ["Phosphates", "Arseniates", "Vanadates", "Antimoniates"],
        "Silicates": ["Silicates"],
        "Elements-Organiques": ["Elements-Organiques"]
    }
    
    categories_trouvees = []
    
    for categorie, cles in categories.items():
        if any(cle in resultat_cles for cle in cles):
            categories_trouvees.append(categorie)
    
    return categories_trouvees if categories_trouvees else None


# Exemple d'utilisation de la fonction
base_de_donnees_csv = "Base-De-Données-F.csv"

gc = {
    "Sulfure-Sulfosels1": ["S"],"Sulfure-Sulfosels2": ["As"],"Sulfure-Sulfosels3": ["Te"],"Sulfure-Sulfosels4": ["Se"],"Sulfure-Sulfosels5": ["Tb"],
    "Halogenure1": ["Cl"], "Halogenure2": ["Br"], "Halogenure3": ["F"], "Halogenure4": ["I"],
    "Oxydes-Hydroxydes": ["O"], 
    "Carbonates": ["C", "O", "_"], "Borates": ["B", "O", "_"], "Nitrates": ["N", "O", "_"],
    "Sulfates": ["S", "O", "_"],  "Chromates": ["Cr", "O", "_"],  "Molybdates": ["Mo", "O", "_"],  "Tungstates": ["W", "O", "_"],
    "Phosphates": ["P", "O", "_"], "Arseniates": ["As", "O", "_"], "Vanadates": ["V", "O", "_"], "Antimoniates": ["Sb", "O", "_"], 
    "Silicates": ["Si", "O", "_"],
    "Elements-Organiques": ["C"]
}



nom_mineral =st.text_input("Saisissez le nom ici:")

formule_chimique = trouver_formule_chimique_par_nom(base_de_donnees_csv, nom_mineral)


if formule_chimique:
    if len(analyse_formule_chimique(formule_chimique)) == 1:
        st.write(f"Le minéral '{nom_mineral}' de formule chimique :'{formule_chimique}' appartient à la classe des : Elements Natifs")
    else: 
        resultat_cles = trouver_cle_par_element(formule_chimique, gc)
        categorie_trouvee = map_cles_aux_categories(resultat_cles)
        if categorie_trouvee:
            st.write(f"Le minéral '{nom_mineral}' de formule chimique: '{formule_chimique}' , peut appartenir à : {categorie_trouvee}")
else:
    st.write(f"Le minéral '{nom_mineral}' n'est pas présent dans la base de données.")







