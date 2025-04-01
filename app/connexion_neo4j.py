from neo4j import GraphDatabase
from config import NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD

# URI examples: "neo4j://localhost", "neo4j+s://xxx.databases.neo4j.io"
URI = NEO4J_URI
AUTH = (NEO4J_USER, NEO4J_PASSWORD)

# Fonction pour établir la connexion à Neo4j
def get_neo4j_connection():
    driver = None
    try:
        # Établir la connexion
        driver = GraphDatabase.driver(URI, auth=AUTH)
        # Vérifier la connectivité
        driver.verify_connectivity()
        print("Connexion réussie à la base de données Neo4j!")
        return driver
    except Exception as e:
        print(f"Erreur de connexion à Neo4j : {e}")
        return None
    finally:
        if driver:
            driver.close()  
            print("Connexion fermée.")

driver = get_neo4j_connection()

'''
from neo4j import GraphDatabase
from config import NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD

def connect_neo4j():
    uri = NEO4J_URI
    user = NEO4J_USER
    password = NEO4J_PASSWORD
    driver = GraphDatabase.driver(uri, auth=(user, password))
    return driver
'''
