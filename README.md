# Application Python : Exploration de Bases de Données NoSQL avec Streamlit

## Introduction
Ce projet vise à explorer deux types de bases de données NoSQL : **MongoDB** (base orientée document) et **Neo4j** (base orientée graphe). L'application Python, développée avec **Streamlit**, permet de se connecter à ces bases hébergées dans le cloud, d'exécuter des requêtes pour extraire des données pertinentes, et de visualiser les résultats de manière interactive.

## Objectifs du projet
- Établir une connexion sécurisée avec les instances cloud de MongoDB et Neo4j.
- Effectuer des requêtes sur MongoDB pour récupérer des informations sur les films.
- Utiliser Neo4j pour modéliser les relations entre films, acteurs et réalisateurs.
- Réaliser des analyses statistiques et des visualisations des données obtenues.

## Configuration et mise en place

### 1. Environnement virtuel
Création d'un environnement virtuel pour une bonne gestion des dépendances :
```bash
python -m venv .venv
source .venv/bin/activate  # Sur macOS/Linux
# ou
.venv\Scripts\activate  # Sur Windows
```

### 2. Installation des dépendances
Installe toutes les bibliothèques nécessaires :
```bash
pip install -r requirements.txt
```

### 3. Lancer l'application 
Après avoir configuré l'environnement et installé les dépendances, assure-toi que tes bases de données sont bien configurées et accessibles, puis lance l'application avec la commande suivante :
```bash
streamlit run app_streamlit.py
```
Cette commande ouvrira une interface web interactive où tu pourras exécuter les requêtes et visualiser les résultats.

## Structure du projet
```
NoSQL_Project/
│-- app_streamlit.py       # Interface utilisateur avec Streamlit
│-- connexion_mongodb.py   # Connexion à MongoDB
│-- connexion_neo4j.py     # Connexion à Neo4j
│-- queries_mongodb.py     # Requêtes MongoDB
│-- queries_neo4j.py       # Requêtes Neo4j
│-- requirements.txt       # Bibliothèques nécessaires
│-- config.py              # Configuration des bases de données
```

## Fonctionnalités principales
### Requêtes MongoDB
- Trouver l'année avec le plus grand nombre de films.
- Calculer la moyenne des votes des films sortis en 2007.
- Afficher un histogramme du nombre de films par année.

### Requêtes Neo4j
- Identifier l'acteur ayant joué dans le plus grand nombre de films.
- Déterminer le film le plus populaire selon les revenus.

### Interface Streamlit
- Interface intuitive permettant d'exécuter les requêtes dynamiquement.
- Visualisation des résultats sous forme de tableaux et graphiques interactifs.

## Références
- [Documentation MongoDB](https://www.mongodb.com/docs/)
- [Documentation Neo4j](https://neo4j.com/docs/)
- [Documentation Streamlit](https://docs.streamlit.io/)

