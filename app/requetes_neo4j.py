from connexion_neo4j import get_neo4j_connection
from pyvis.network import Network
from py2neo import Graph
import networkx as nx
import streamlit as st
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import tempfile
import os

driver = get_neo4j_connection()

# 14. Quel est l’acteur ayant joué dans le plus grand nombre de films ?
def acteur_plus_de_films():
    query = """
    MATCH (a:Actor)-[:A_JOUE]->(f:Film)
    WITH a, COUNT(f) AS filmCount
    ORDER BY filmCount DESC
    RETURN a.name AS Actor, filmCount AS NumberOfFilms LIMIT 1;
    """
    with driver.session() as session:
        result = session.run(query)
        return [record for record in result]
    
# 14 bis. 
def acteurs_plus_de_films():
    query = """
    MATCH (a:Actor)-[:A_JOUE]->(f:Film)
    WITH a, COUNT(f) AS filmCount
    ORDER BY filmCount DESC
    RETURN a.name AS Actor, filmCount AS NumberOfFilms;
    """
    with driver.session() as session:
        result = session.run(query)
        return [record for record in result]

# 15. Quels sont les acteurs ayant joué dans des films où l’actrice Anne Hathaway a également joué ?
def acteurs_avec_anne_hathaway():
    query = """
    MATCH (a1:Actor)-[:A_JOUE]->(f:Film)<-[:A_JOUE]-(a2:Actor)
    WHERE a1.name = 'Anne Hathaway' AND a1 <> a2
    RETURN DISTINCT a2.name AS Actor, f.title AS Film;
    """
    with driver.session() as session:
        result = session.run(query)
        return [record for record in result]

# 16. Quel est l’acteur ayant joué dans des films totalisant le plus de revenus ?
def acteur_plus_de_revenus():
    query = """
    MATCH (a:Actor)-[:A_JOUE]->(f:Film)
    WHERE f.revenue IS NOT NULL  
    WITH a, COLLECT(f.title) AS film_titles, COUNT(f) AS films_count, SUM(f.revenue) AS total_revenue
    ORDER BY total_revenue DESC
    RETURN a.name AS Actor, films_count AS NumberOfFilms, film_titles AS FilmTitles, total_revenue AS TotalRevenue LIMIT 1;
    """
    with driver.session() as session:
        result = session.run(query)
        return [record for record in result]
    
# 16 bis.
def acteurs_plus_de_revenus():
    query = """
    MATCH (a:Actor)-[:A_JOUE]->(f:Film)
    WHERE f.revenue IS NOT NULL  
    WITH a, COLLECT(f.title) AS film_titles, COUNT(f) AS films_count, SUM(f.revenue) AS total_revenue
    ORDER BY total_revenue DESC
    RETURN a.name AS Actor, films_count AS NumberOfFilms, film_titles AS FilmTitles, total_revenue AS TotalRevenue;
    """
    with driver.session() as session:
        result = session.run(query)
        return [record for record in result]

# 17. Quelle est la moyenne des votes ?
def moyenne_votes():
    query = """
    MATCH (f:Film)
    WHERE f.votes IS NOT NULL
    RETURN AVG(f.votes) AS AverageVotes;
    """
    with driver.session() as session:
        result = session.run(query)
        return [record for record in result]

# 18. Quel est le genre le plus représenté dans la base de données ?
def genre_plus_representé():
    query = """
    MATCH (f:Film)-[:A_POUR_GENRE]->(g:Genre)
    RETURN g.name AS Genre, COUNT(f) AS NumberOfFilms
    ORDER BY NumberOfFilms DESC
    LIMIT 1;
    """
    with driver.session() as session:
        result = session.run(query)
        return [record for record in result]

# 19. Quels sont les films dans lesquels les acteurs ayant joué avec vous ont également joué ?
def films_avec_acteurs_voisins(actor_name, film_title):
    create_query = """
    MERGE (a:Actor {name: $actor_name})
    MERGE (f:Film {title: $film_title})
    MERGE (a)-[:A_JOUE]->(f);
    """
    find_coactors_query = """
    MATCH (a1:Actor {name: $actor_name})-[:A_JOUE]->(f1:Film)<-[:A_JOUE]-(a2:Actor),
          (a2)-[:A_JOUE]->(f2:Film)
    WHERE f2 <> f1  
    RETURN DISTINCT a2.name AS CoActor, f2.title AS FilmTitle;
    """
    with driver.session() as session:
        session.run(create_query, actor_name=actor_name, film_title=film_title)
        result = session.run(find_coactors_query, actor_name=actor_name, film_title=film_title)
        return [{"CoActor": record["CoActor"], "FilmTitle": record["FilmTitle"]} for record in result]

# 20. Quel réalisateur a travaillé avec le plus grand nombre d’acteurs distincts ?
def réalisateur_plus_d_acteurs():
    query = """
    MATCH (d:Director)-[:A_REALISE]->(f:Film)<-[:A_JOUE]-(a:Actor)
    WITH d, COUNT(DISTINCT a) AS num_actors
    ORDER BY num_actors DESC
    LIMIT 1
    RETURN d.name AS Director, num_actors AS NumberOfActors;
    """
    with driver.session() as session:
        result = session.run(query)
        return [record for record in result]

# 21. Quels sont les films les plus “connectés”, c’est-à-dire ceux qui ont le plus d’acteurs en commun avec d’autres films ?
def films_plus_connectés():
    query = """
    MATCH (f1:Film)<-[:A_JOUE]-(a:Actor)-[:A_JOUE]->(f2:Film)
    WHERE f1 <> f2 AND f1.title < f2.title
    WITH f1, f2, COLLECT(DISTINCT a.name) AS shared_actors_names, COUNT(DISTINCT a) AS common_actors
    ORDER BY common_actors DESC
    LIMIT 5
    RETURN f1.title AS Film1, f2.title AS Film2, common_actors AS NumberOfSharedActors, shared_actors_names AS SharedActorsNames;
    """
    with driver.session() as session:
        result = session.run(query)
        return [record for record in result]

# 22. Trouver les 5 acteurs ayant joué avec le plus de réalisateurs différents.
def acteurs_plus_de_réalisateurs():
    query = """
    MATCH (a:Actor)-[:A_JOUE]->(f:Film)<-[:A_REALISE]-(d:Director)
    WITH a, COUNT(DISTINCT d) AS num_directors
    ORDER BY num_directors DESC
    LIMIT 5
    RETURN a.name AS Actor, num_directors AS NumberOfDirectors;
    """
    with driver.session() as session:
        result = session.run(query)
        return [record for record in result]

# 23. Recommander un film à un acteur en fonction des genres des films où il a déjà joué.
def recommander_films(actor_name):
    query = """
    MATCH (a:Actor {name: $actor_name})-[:A_JOUE]->(f:Film)-[:A_POUR_GENRE]->(g:Genre)
    MATCH (r:Film)-[:A_POUR_GENRE]->(g)
    WHERE NOT (a)-[:A_JOUE]->(r) 
    RETURN DISTINCT r.title AS RecommendedFilm, COLLECT(DISTINCT g.name) AS Genres
    ORDER BY SIZE(COLLECT(DISTINCT g.name)) DESC
    LIMIT 1;
    """
    with driver.session() as session:
        result = session.run(query, actor_name=actor_name)
        return [record for record in result]

# 24. Créer une relation INFLUENCE_PAR entre les réalisateurs en se basant sur des similarités dans les genres de films qu’ils ont réalisés.
def relation_influence_par():
    query = """
    MATCH (d1:Director)-[:A_REALISE]->(f1:Film)-[:A_POUR_GENRE]->(g1:Genre)
    WITH d1, COLLECT(DISTINCT g1.name) AS genres_d1
    MATCH (d2:Director)-[:A_REALISE]->(f2:Film)-[:A_POUR_GENRE]->(g2:Genre)
    WHERE d1 <> d2
    WITH d1, d2, genres_d1, COLLECT(DISTINCT g2.name) AS genres_d2
    WHERE size(apoc.coll.intersection(genres_d1, genres_d2)) > 2  
    MERGE (d1)-[:INFLUENCE_PAR]->(d2)
    MERGE (d2)-[:INFLUENCE_PAR]->(d1);
    """
    with driver.session() as session:
        session.run(query)

# 25. Quel est le “chemin” le plus court entre deux acteurs donnés (ex : Tom Hanks et Scarlett Johansson) ?
def chemin_plus_court(actor1, actor2):
    query = """
    MATCH (a1:Actor {name: $actor1}), (a2:Actor {name: $actor2})
    MATCH path = shortestPath((a1)-[:A_JOUE*]-(a2))
    RETURN path;
    """
    with driver.session() as session:
        result = session.run(query, actor1=actor1, actor2=actor2)
        #return [record for record in result]
        paths = [record['path'] for record in result]
        return paths

# Fonction pour afficher le chemin le plus court entre deux acteurs
def generate_graph(actor1, actor2):
    paths = chemin_plus_court(actor1, actor2)
    
    if not paths:
        return None
    
    net = Network(height="500px", width="100%", bgcolor="#222222", font_color="white", notebook=False)
    
    seen_nodes = set()
    
    for path in paths:
        for rel in path.relationships:
            node1 = str(rel.start_node.get("title", rel.start_node.get("name", "Inconnu")))
            node2 = str(rel.end_node.get("title", rel.end_node.get("name", "Inconnu")))
            
            if node1 not in seen_nodes:
                net.add_node(node1, label=node1, color="#ffcc00")
                seen_nodes.add(node1)
            if node2 not in seen_nodes:
                net.add_node(node2, label=node2, color="#ff5733")
                seen_nodes.add(node2)
            net.add_edge(node1, node2, color="cyan")
    
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".html")
    net.save_graph(temp_file.name)
    return temp_file.name

# 26. Analyser les communautés d’acteurs : Quels sont les groupes d’acteurs qui ont tendance à travailler ensemble ?
def communautes_acteurs():
    query = """
    MATCH (a1:Actor)-[:A_JOUE]->(f:Film)<-[:A_JOUE]-(a2:Actor)
    WHERE a1 <> a2 AND a1.name < a2.name
    WITH a1, a2, COUNT(f) AS common_movies, COLLECT(f.title) AS common_movies_titles
    WHERE common_movies > 1
    RETURN a1.name AS Actor1, a2.name AS Actor2, common_movies AS CommonMovies, common_movies_titles AS CommonMoviesTitle;
    """
    with driver.session() as session:
        result = session.run(query)
        return [record for record in result]

# 27. Quels sont les films qui ont des genres en commun mais qui ont des réalisateurs différents ?
def films_genres_communs_differents_realisateurs():
    query = """
    MATCH (f1:Film)-[:A_POUR_GENRE]->(g:Genre)<-[:A_POUR_GENRE]-(f2:Film)
    MATCH (f1)<-[:A_REALISE]-(d1:Director), (f2)<-[:A_REALISE]-(d2:Director)
    WHERE f1 <> f2 AND d1 <> d2
    WITH f1, d1, f2, d2, COLLECT(DISTINCT g.name) AS shared_genres
    WHERE size(shared_genres) >= 2
    RETURN f1.title AS Film1, d1.name AS Director1, 
           f2.title AS Film2, d2.name AS Director2, 
           shared_genres
    ORDER BY size(shared_genres) DESC
    LIMIT 10;
    """
    with driver.session() as session:
        result = session.run(query)
        return [record for record in result]

# 28. Recommander des films aux utilisateurs en fonction des préférences d’un acteur donné.
def recommander_films_preferences(actor_name):
    query = """
    MATCH (a:Actor {name: $actor_name})-[:A_JOUE]->(f:Film)-[:A_POUR_GENRE]->(g:Genre)
    WITH a, COLLECT(DISTINCT g) AS annee_genres
    MATCH (r:Film)-[:A_POUR_GENRE]->(g:Genre)
    WHERE g IN annee_genres 
    WITH r, COLLECT(DISTINCT g.name) AS genre_overlap
    WHERE size(genre_overlap) >= 2
    ORDER BY genre_overlap DESC 
    LIMIT 10
    RETURN r.title AS RecommendedMovie, genre_overlap AS MatchingGenres;
    """
    with driver.session() as session:
        result = session.run(query, actor_name=actor_name)
        return [record for record in result]

# 29. Créer une relation de “concurrence” entre réalisateurs ayant réalisé des films similaires la même année.
def relation_concurrence():
    query = """
    MATCH (d1:Director)-[:A_REALISE]->(f1:Film)-[:A_POUR_GENRE]->(g:Genre),
          (d2:Director)-[:A_REALISE]->(f2:Film)-[:A_POUR_GENRE]->(g:Genre)
    WHERE d1 <> d2 
    AND f1.year = f2.year 
    WITH d1, d2, f1.year AS year, f1, f2, COUNT(DISTINCT g) AS num_genres
    WHERE num_genres >= 2 
    MERGE (d1)-[:CONCURRENCE {shared_genres: num_genres, year: year}]->(d2);
    """
    with driver.session() as session:
        session.run(query)

# 30. Identifier les collaborations les plus fréquentes entre réalisateurs et acteurs, puis analyser si ces collaborations sont associées à un succès commercial ou critique.
def collaborations_succes():
    query = """
    MATCH (d:Director)-[:A_REALISE]->(f:Film)<-[:A_JOUE]-(a:Actor)
    WHERE f.revenue IS NOT NULL AND f.metascore IS NOT NULL
    AND toFloat(f.revenue) IS NOT NULL AND toFloat(f.metascore) IS NOT NULL
    WITH d, a, COUNT(f) AS common_films, AVG(toFloat(f.revenue)) AS avg_revenue, AVG(toFloat(f.metascore)) AS avg_metascore
    WHERE common_films >= 2
    RETURN d.name AS Director, 
           a.name AS Actor, 
           common_films AS NumberOfFilmsTogether, 
           avg_revenue AS AvgRevenue, 
           avg_metascore AS AvgMetascore
    ORDER BY common_films DESC, avg_revenue DESC;
    """
    with driver.session() as session:
        result = session.run(query)
        return [record for record in result]

# Fonction pour récupérer les relations INFLUENCE_PAR
def get_influence_relations():
    query = """
    MATCH (d1:Director)-[:INFLUENCE_PAR]->(d2:Director)
    MATCH (d2)-[:INFLUENCE_PAR]->(d1)
    RETURN d1.name AS director1, d2.name AS director2
    """
    with driver.session() as session:
        results = session.run(query)
        return [(record["director1"], record["director2"]) for record in results]

# Fonction pour afficher le graphe INFLUENCE_PAR
def display_graph():
    relation_influence_par()  
    relations = get_influence_relations()
    net = Network(height="500px", width="100%", bgcolor="#222222", font_color="white", notebook=False, directed=True)
    seen_nodes = set()
    for d1, d2 in relations:
        if d1 not in seen_nodes:
            net.add_node(d1, label=d1, color="#ffcc00" , shape="circle")  
            seen_nodes.add(d1)
        if d2 not in seen_nodes:
            net.add_node(d2, label=d2, color="#ff5733", shape="circle") 
            seen_nodes.add(d2)
        edge_label = "Influence artistique"
        net.add_edge(d1, d2, color="cyan", title=edge_label, arrows="to") 
    net.force_atlas_2based(gravity=-50, central_gravity=0.01, spring_length=100, spring_strength=0.08, damping=0.9)
    net.save_graph("graph.html")
    return "graph.html"

def create_graph(result):
    G = nx.Graph()
    for record in result:
        path = record['path']
        for rel in path.relationships:
            start_node = rel.start_node
            end_node = rel.end_node
            G.add_node(start_node['name'], label='Actor' if 'Actor' in start_node.labels else 'Film')
            G.add_node(end_node['name'], label='Actor' if 'Actor' in end_node.labels else 'Film')
            G.add_edge(start_node['name'], end_node['name'], label=rel.type)
    return G

# Fonction pour récupérer les relations de concurrence
def get_concurrence_relations():
    query = """
    MATCH (d1:Director)-[r:CONCURRENCE]->(d2:Director)
    RETURN d1.name AS director1, d2.name AS director2, r.year AS year, r.shared_genres AS shared_genres
    """
    with driver.session() as session:
        results = session.run(query)
        return [(record["director1"], record["director2"], record["year"], record["shared_genres"]) for record in results]

# Fonction pour afficher le graphe de concurrence
def display_concurrence_graph():
    relation_concurrence()
    relations = get_concurrence_relations()
    
    net = Network(height="500px", width="100%", bgcolor="#222222", font_color="white", notebook=False, directed=True)
    
    seen_nodes = set()
    
    for d1, d2, year, shared_genres in relations:
        if d1 not in seen_nodes:
            net.add_node(d1, label=d1, color="#ffcc00", shape="circle")
            seen_nodes.add(d1)
        if d2 not in seen_nodes:
            net.add_node(d2, label=d2, color="#ff5733", shape="circle")
            seen_nodes.add(d2)
        edge_label = f"Genres communs: {shared_genres}, Année: {year}"
        net.add_edge(d1, d2, color="cyan", title=edge_label, arrows="to")  # Ajout des flèches
    net.force_atlas_2based(gravity=-50, central_gravity=0.01, spring_length=100, spring_strength=0.08, damping=0.9)
    net.save_graph("concurrence_graph.html")
    return "concurrence_graph.html"
