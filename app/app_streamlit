import streamlit as st
import requetes_mongodb as r_mongo
import requetes_neo4j as r_neo4j
import pandas as pd
import matplotlib.pyplot as plt

st.title("Analyse de la base de films")
st.markdown("*Les données brutes issues des requêtes ont été traitées et formatées pour améliorer leur présentation et leur visualisation.*")

# Requêtes MongoDB

# 1 - Année avec le plus de films
st.header("1 - Année avec le plus de films")
annee_films = r_mongo.annee_avec_plus_de_films()
if annee_films:
    st.markdown(f"L'année où le plus grand nombre de films ont été sortis est <span style='color: green;'>{annee_films[0]['_id']}</span> avec <span style='color: blue;'>{annee_films[0]['total_films']}</span> films.", unsafe_allow_html=True)
else:
    st.markdown("<span style='color: red;'>Aucune donnée disponible.</span>", unsafe_allow_html=True)

# 2 - Nombre de films après 1999
st.header("2 - Nombre de films après 1999")
films_apres_1999 = r_mongo.nombre_de_films_apres_1999()
if films_apres_1999:
    st.markdown(f"Il y a <span style='color: green;'>{films_apres_1999[0]['total_films_after_1999']}</span> films sortis après 1999.", unsafe_allow_html=True)
else:
    st.markdown("<span style='color: red;'>Aucune donnée disponible.</span>", unsafe_allow_html=True)

# 3 - Moyenne des votes en 2007
st.header("3 - Moyenne des votes en 2007")
moyenne_votes = r_mongo.moyenne_votes_2007()
if moyenne_votes:
    st.markdown(f"La moyenne des votes des films sortis en 2007 est de <span style='color: green;'>{moyenne_votes[0]['avg_votes']:.2f}</span>.", unsafe_allow_html=True)
else:
    st.markdown("<span style='color: red;'>Aucune donnée disponible.</span>", unsafe_allow_html=True)

# 4 - Nombre de films par année (Histogramme)
st.header("4 - Nombre de films par année")
data = r_mongo.films_par_annee()
years = [int(entry["_id"]) for entry in data if entry["_id"] is not None] 
counts = [entry["count"] for entry in data if entry["_id"] is not None]
if years and counts: 
    plt.figure(figsize=(10, 5))
    plt.bar(years, counts, color="skyblue", edgecolor="black")
    plt.xlabel("Année")
    plt.ylabel("Nombre de films")
    plt.title("Nombre de films sortis par année")
    plt.xticks(years, rotation=45)
    st.pyplot(plt)
else:
    st.markdown("<span style='color: red;'>Aucune donnée disponible.</span>", unsafe_allow_html=True)

# 5 - Genres disponibles
st.header("5 - Genres disponibles")
genres = r_mongo.genres_disponibles()
if genres:
    st.markdown(f"Voici les genres disponibles: <span style='color: green;'>{', '.join([g['_id'] for g in genres])}</span>.", unsafe_allow_html=True)
else:
    st.markdown("<span style='color: red;'>Aucune donnée disponible.</span>", unsafe_allow_html=True)

# 6 - Film avec le plus grand revenu
st.header("6 - Film avec le plus grand revenu")
film_revenu = r_mongo.film_avec_plus_gros_revenu()
if film_revenu:
    st.markdown(f"Le film ayant généré le plus de revenus est <span style='color: green;'>{film_revenu[0]['title']}</span> ({film_revenu[0]['year']}) avec un revenu de <span style='color: blue;'>{film_revenu[0]['Revenue (Millions)']}</span> millions de dollars.", unsafe_allow_html=True)
else:
    st.markdown("<span style='color: red;'>Aucune donnée disponible.</span>", unsafe_allow_html=True)

# 7 - Réalisateurs avec plus de 5 films
st.header("7 - Réalisateurs avec plus de 5 films")
realisateurs = r_mongo.realisateurs_avec_plus_de_5_films()
if realisateurs:
    st.markdown("Réalisateurs ayant réalisé plus de 5 films:")
    for realisateur in realisateurs:
        st.markdown(f"- {realisateur['_id']} ({realisateur['number_of_films']} films)", unsafe_allow_html=True)
else:
    st.markdown("<span style='color: red;'>Aucun réalisateur de la base de données n’a réalisé plus de 5 films.</span>", unsafe_allow_html=True)
st.markdown("Comme aucun réalisateur de la base de données n’a réalisé plus de 5 films, nous avons testé jusqu’à obtenir le résultat ci-dessous :")
realisateurs = r_mongo.realisateurs_avec_plus_de_2_films()
if realisateurs:
    data_realisateurs = []
    for realisateur in realisateurs:
        data_realisateurs.append({
            "Réalisateur": realisateur['_id'],
            "Nombre de Films": realisateur['number_of_films']
        })
    df_realisateurs = pd.DataFrame(data_realisateurs)
    st.dataframe(df_realisateurs)
else:
    st.markdown("<span style='color: red;'>Aucun réalisateur de la base de données n’a réalisé plus de 2 films.</span>", unsafe_allow_html=True)
st.markdown("C’est donc <span style='color: green;'>Christopher Nolan</span> qui a réalisé le plus de films dans notre base de données, au nombre de <span style='color: blue;'>4</span> films.", unsafe_allow_html=True)

# 8 - Genre le plus rentable
st.header("8 - Genre le plus rentable")
genre_rentable = r_mongo.genre_avec_plus_gros_revenu_moyen()
if genre_rentable:
    st.markdown(f"Le genre le plus rentable est <span style='color: green;'>{genre_rentable[0]['_id']}</span> avec un revenu moyen de <span style='color: blue;'>{genre_rentable[0]['avg_revenue']:.2f}</span> millions de dollars.", unsafe_allow_html=True)
else:
    st.markdown("<span style='color: red;'>Aucune donnée disponible.</span>", unsafe_allow_html=True)

# 9 - Top 3 films par décennie
st.header("9 - Top 3 films par décennie")
result = r_mongo.top_3_films_par_decennie()
if result:
    top_films = []
    for decade_data in result:
        decade = decade_data.get("_id")
        for movie in decade_data.get("top_movies", []):
            title = movie.get("title", "N/A")
            rating = movie.get("rating", "N/A")
            if title != "N/A" and rating != "N/A":
                top_films.append({"Décennie": decade, "Film": title, "Rating": rating})
    if top_films:
        df_top_films = pd.DataFrame(top_films)
        df_top_films_styled = df_top_films.style.applymap(lambda x: 'color: green' if isinstance(x, str) else '', subset=['Film'])
        st.dataframe(df_top_films_styled)
    else:
        st.markdown("<span style='color: red;'>Aucune donnée valide disponible.</span>", unsafe_allow_html=True)
else:
    st.markdown("<span style='color: red;'>Aucune donnée disponible.</span>", unsafe_allow_html=True)
st.markdown("Comme le rating est soit « G », soit « unrated » (ce qui n’est pas très parlant selon nous), nous avons plutôt décidé d’afficher les 3 films de chaque décennie avec le meilleur Metascore :")
result = r_mongo.top_3_films_par_decenniebis()
if result:
    top_films = []
    for decade_data in result:
        decade = decade_data.get("_id")
        for movie in decade_data.get("top_movies", []):
            title = movie.get("title", "N/A")
            metascore = movie.get("Metascore", "N/A")
            if title != "N/A" and metascore != "N/A":
                top_films.append({"Décennie": decade, "Film": title, "Metascore": metascore})
    if top_films:
        df_top_films = pd.DataFrame(top_films)
        df_top_films_styled = df_top_films.style.applymap(lambda x: 'color: green' if isinstance(x, str) else '', subset=['Film'])
        st.dataframe(df_top_films_styled)
    else:
        st.markdown("<span style='color: red;'>Aucune donnée valide disponible.</span>", unsafe_allow_html=True)
else:
    st.markdown("<span style='color: red;'>Aucune donnée disponible.</span>", unsafe_allow_html=True)

# 10 - Film le plus long par genre
st.header("10 - Film le plus long par genre")
films_long = r_mongo.film_le_plus_long_par_genre()
if films_long:
    data_films_long = []
    for genre in films_long:
        data_films_long.append({
            "Genre": genre['_id'],
            "Titre du Film": genre['longest_film']['title'],
            "Durée (minutes)": genre['longest_film']['Runtime']
        })
    df_films_long = pd.DataFrame(data_films_long)
    df_films_long = df_films_long.style.applymap(lambda x: 'color: green' if isinstance(x, str) else '', subset=['Titre du Film'])
    st.dataframe(df_films_long)
else:
    st.markdown("<span style='color: red;'>Aucune donnée disponible.</span>", unsafe_allow_html=True)

# 11 - Films ayant une note supérieure à 80 et générant plus de 50 millions de dollars
st.header("11 - Films ayant une note supérieure à 80 et générant plus de 50 millions de dollars")
top_films = r_mongo.creer_vue_top_films()
if top_films:
    data_top_films = []
    for film in top_films:
        data_top_films.append({
            "Titre": film['title'],
            "Année": film['year'],
            "Metascore": film['Metascore'],
            "Revenue (millions)": film['revenue']
        })
    df_top_films = pd.DataFrame(data_top_films)
    df_top_films = df_top_films.style.applymap(lambda x: 'color: green' if isinstance(x, str) else '', subset=['Titre'])
    st.dataframe(df_top_films)
else:
    st.markdown("<span style='color: red;'>Aucun film trouvé correspondant aux critères.</span>", unsafe_allow_html=True)

# 12 - Corrélation durée/revenu
st.header("12 - Corrélation durée/revenu")
df_correlation, correlation_result = r_mongo.correlation_duree_revenu1()
if df_correlation is not None:
    df_correlation.rename(columns={'title': 'Film', 'runtime': 'Durée (min)', 'revenue': 'Revenu (millions)'}, inplace=True)
    df_correlation = df_correlation.dropna(subset=['Durée (min)'])
    df_correlation['Durée (min)'] = df_correlation['Durée (min)'].astype(int)
    df_correlation['Revenu (millions)'] = df_correlation['Revenu (millions)'].astype(float).round(2)
    df_styled = df_correlation.style.applymap(lambda x: 'color: green' if isinstance(x, (int, float)) else '', subset=['Durée (min)']) \
                                    .applymap(lambda x: 'color: green' if isinstance(x, (int, float)) else '', subset=['Revenu (millions)'])
    st.dataframe(df_styled)
else:
    st.markdown("<span style='color: red;'>Aucune donnée disponible.</span>", unsafe_allow_html=True)

correlation_result = r_mongo.correlation_duree_revenu()
if isinstance(correlation_result, tuple):
    correlation, p_value = correlation_result
    st.markdown(f"Corrélation de Pearson : <span style='color: green;'>{correlation:.3f}</span>", unsafe_allow_html=True)
    st.markdown(f"P-value : <span style='color: blue;'>{p_value:.3f}</span>", unsafe_allow_html=True)
    st.markdown("Interprétation : La corrélation de Pearson fournit un indice reflétant une relation linéaire entre deux variables continues : ici, la valeur positive de 0.306 signifie qu’il existe une corrélation positive entre la durée des films et leurs revenus, mais la corrélation reste assez faible / modérée. La p-valeur, inférieure au seuil 0.05, indique tout de même que le résultat obtenu est significatif.")
else:
    st.markdown("<span style='color: red;'>Pas assez de données pour calculer la corrélation.</span>", unsafe_allow_html=True)

# 13 - Durée moyenne des films par décennie
st.header("13 - Durée moyenne des films par décennie")
duree_moyenne = r_mongo.evolution_duree_moyenne_par_decennie()
if duree_moyenne:
    df_duree = pd.DataFrame(duree_moyenne)
    df_duree = df_duree[df_duree['_id'].notna() & (df_duree['_id'] != 0)]
    df_duree['_id'] = df_duree['_id'].astype(int)
    df_duree.rename(columns={'_id': 'Décennie', 'avg_runtime': 'Durée Moyenne (minutes)'}, inplace=True)
    df_duree = df_duree.style.applymap(lambda x: 'color: green' if isinstance(x, (int, float)) else '', subset=['Durée Moyenne (minutes)'])
    st.dataframe(df_duree)
    st.markdown("Pas vraiment de évolution claire en termes de durée moyenne des films par décennie, mais on peut noter une légère augmentation dans les années 2000.")
else:
    st.markdown("<span style='color: red;'>Aucune donnée disponible.</span>", unsafe_allow_html=True)

# Requêtes Neo4j

# 14. Acteur ayant joué dans le plus grand nombre de films
st.header("14 - Acteur ayant joué dans le plus grand nombre de films")
acteur_films = r_neo4j.acteur_plus_de_films()
if acteur_films:
    st.write(f"L'acteur ayant joué dans le plus grand nombre de films est <span style='color: green;'>{acteur_films[0]['Actor']}</span> avec un total de <span style='color: blue;'>{acteur_films[0]['NumberOfFilms']} films</span>.", unsafe_allow_html=True)
    st.write("Il faut noter que plusieurs autres acteurs ont joué dans 4 films, donc nous avons retiré le LIMIT pour avoir leur nom : ")
else:
    st.markdown("<span style='color: red;'>Aucune donnée disponible.</span>", unsafe_allow_html=True)

# 14 bis. 
acteurs_films = r_neo4j.acteurs_plus_de_films()
if acteurs_films:
    df_acteurs_films = pd.DataFrame(acteurs_films, columns=["Actor", "NumberOfFilms"])
    df_styled = df_acteurs_films.style.applymap(lambda x: 'color: green', subset=['Actor'])
    st.dataframe(df_styled)
else:
    st.markdown("<span style='color: red;'>Aucune donnée disponible.</span>", unsafe_allow_html=True)

# 15. Acteurs ayant joué avec Anne Hathaway
st.header("15 - Acteurs ayant joué avec Anne Hathaway")
acteurs_anne = r_neo4j.acteurs_avec_anne_hathaway()
if acteurs_anne:
    df_acteurs_anne = pd.DataFrame(acteurs_anne, columns=["Actor", "Film"])
    df_duree = df_acteurs_anne.style.applymap(lambda x: 'color: green;', subset=['Actor'])
    st.dataframe(df_duree)
else:
    st.markdown("<span style='color: red;'>Aucune donnée disponible.</span>", unsafe_allow_html=True)

# 16. Acteur ayant joué dans des films totalisant le plus de revenus
st.header("16 - Acteur ayant joué dans des films totalisant le plus de revenus")
acteur_revenus = r_neo4j.acteur_plus_de_revenus()
if acteur_revenus:
    st.write(f"L'acteur ayant joué dans des films totalisant le plus de revenus est <span style='color: green;'>{acteur_revenus[0]['Actor']}</span>, avec <span style='color: blue;'>{acteur_revenus[0]['NumberOfFilms']} films</span> et un revenu total de <span style='color: blue;'>{acteur_revenus[0]['TotalRevenue']} dollars</span>.", unsafe_allow_html=True)
    st.write("Il faut noter que Robert Downey JR. a joué dans les mêmes films que Chris Evans, donc le revenu total généré est le même pour les deux acteurs.")
else:
    st.markdown("<span style='color: red;'>Aucune donnée disponible.</span>", unsafe_allow_html=True)

# 16 bis. 
acteurs_revenus = r_neo4j.acteurs_plus_de_revenus()
if acteurs_revenus:
    df_acteurs_revenus = pd.DataFrame(acteurs_revenus, columns=["Actor", "NumberOfFilms", "FilmTitles", "TotalRevenue"])
    df_styled = df_acteurs_revenus.style.applymap(lambda x: 'color: green', subset=['Actor'])
    st.dataframe(df_styled)
else:
    st.markdown("<span style='color: red;'>Aucune donnée disponible.</span>", unsafe_allow_html=True)

# 17. Moyenne des votes
st.header("17 - Moyenne des votes")
moyenne_votes = r_neo4j.moyenne_votes()
if moyenne_votes:
    st.write(f"La moyenne des votes pour les films est de <span style='color: green;'>{moyenne_votes[0]['AverageVotes']}</span>.", unsafe_allow_html=True)
else:
    st.markdown("<span style='color: red;'>Aucune donnée disponible.</span>", unsafe_allow_html=True)

# 18. Genre le plus représenté
st.header("18 - Genre le plus représenté")
genre_representé = r_neo4j.genre_plus_representé()
if genre_representé:
    st.write(f"Le genre le plus représenté est <span style='color: green;'>{genre_representé[0]['Genre']}</span>, avec <span style='color: blue;'>{genre_representé[0]['NumberOfFilms']} films</span>.", unsafe_allow_html=True)
else:
    st.markdown("<span style='color: red;'>Aucune donnée disponible.</span>", unsafe_allow_html=True)

# 19. Films des acteurs ayant joué avec Emeline Pellan
st.header("19 - Films des acteurs ayant joué avec Emeline Pellan")
st.write("Pour répondre à cette question, nous avons d’abord créé un nœud Emeline Pellan en tant qu’Acteur, ainsi que la liaison « A_JOUE » vers le film Interstellar.")
films_voisins_emeline_pellan = r_neo4j.films_avec_acteurs_voisins("Emeline Pellan", "Interstellar")
if films_voisins_emeline_pellan:
    df_films_voisins = pd.DataFrame(films_voisins_emeline_pellan)
    st.dataframe(df_films_voisins)
else:
    st.markdown("<span style='color: red;'>Aucune donnée disponible.</span>", unsafe_allow_html=True)

# 20. Réalisateur ayant travaillé avec le plus d'acteurs distincts
st.header("20 - Réalisateur ayant travaillé avec le plus d'acteurs distincts")
realisateur_acteurs = r_neo4j.réalisateur_plus_d_acteurs()
if realisateur_acteurs:
    st.write(f"Le réalisateur ayant travaillé avec le plus grand nombre d'acteurs distincts est <span style='color: green;'>{realisateur_acteurs[0]['Director']}</span>, ayant collaboré avec <span style='color: blue;'>{realisateur_acteurs[0]['NumberOfActors']} acteurs</span>.", unsafe_allow_html=True)
else:
    st.markdown("<span style='color: red;'>Aucune donnée disponible.</span>", unsafe_allow_html=True)

# 21. Films les plus connectés
st.header("21 - Films les plus connectés")
films_connectes = r_neo4j.films_plus_connectés()
if films_connectes:
    df_films_connectes = pd.DataFrame(films_connectes, columns=["Film1", "Film2", "NumberOfSharedActors", "SharedActorsNames"])
    st.dataframe(df_films_connectes)
else:
    st.markdown("<span style='color: red;'>Aucune donnée disponible.</span>", unsafe_allow_html=True)

# 22. 5 acteurs ayant travaillé avec le plus de réalisateurs
st.header("22 - 5 acteurs ayant travaillé avec le plus de réalisateurs")
acteurs_realisateurs = r_neo4j.acteurs_plus_de_réalisateurs()
if acteurs_realisateurs:
    df_acteurs_realisateurs = pd.DataFrame(acteurs_realisateurs, columns=["Actor", "NumberOfDirectors"])
    styled_df = df_acteurs_realisateurs.style.applymap(lambda x: 'color: green;', subset=['Actor'])  
    st.dataframe(styled_df)
else:
    st.markdown("<span style='color: red;'>Aucune donnée disponible.</span>", unsafe_allow_html=True)

# 23. Recommandation d'un film à un acteur (Anne Hathaway) en fonction des genres des films où il a déjà joué
st.header("23 - Recommandation d'un film à un acteur **(A SAISIR)** en fonction des genres des films où il a déjà joué")
st.write("<span style='color: yellow;'>Par exemple, saisissez le nom de l'actrice Anne Hathaway et appuyez <Entrée>.</span>", unsafe_allow_html=True)
actor = st.text_input("Nom de l'acteur")
recommandations_films = r_neo4j.recommander_films(actor)
if recommandations_films:
    for rec in recommandations_films:
        st.write(f"- {rec['RecommendedFilm']} (Genres: {', '.join(rec['Genres'])})")
else:
    st.markdown("<span style='color: red;'>Aucune donnée disponible.</span>", unsafe_allow_html=True)

# 24. Création des relations d'influence entre réalisateurs
st.header("24 - Création des relations d'influence entre réalisateurs")
st.write("Attendre quelques secondes pour le chargement du graphique.")
graph_html = r_neo4j.display_graph()
st.components.v1.html(open(graph_html, "r", encoding="utf-8").read(), height=500, scrolling=True)
st.write("On créé les relations INFLUENCE_PAR seulement si les deux réalisateurs, que l'on compare, ont travaillé sur plus de deux genres en commun.")

# 25. Chemin le plus court entre Tom Hanks et Scarlett Johansson
st.header("25 - Chemin le plus court entre deux acteurs **(A SAISIR)**")
st.write("<span style='color: yellow;'>Par exemple, saisissez le nom de l'acteur Tom Hanks et de l'actrice Scarlett Johansson et appuyez sur le bouton <Trouver le chemin>.</span>", unsafe_allow_html=True)
st.write("On peut aussi essayer avec d'autres acteurs, mais il faut que les deux acteurs soient connectés dans le graphe.")
actor1 = st.text_input("Nom du premier acteur")
actor2 = st.text_input("Nom du deuxième acteur")
if st.button("Trouver le chemin"):
    graph_file = r_neo4j.generate_graph(actor1, actor2)
    if graph_file:
        st.components.v1.html(open(graph_file, "r", encoding="utf-8").read(), height=550)
    else:
        st.warning("<span style='color: red;'>Aucun chemin trouvé entre ces deux acteurs.</span>", unsafe_allow_html=True)

# 26. Analyse des communautés d’acteurs
st.header("26 - Analyse des communautés d’acteurs")
communautes = r_neo4j.communautes_acteurs()
df_communautes = pd.DataFrame(communautes, columns=["Actor1", "Actor2", "CommonMovies", "CommonMoviesTitle"])
if communautes:
    st.dataframe(df_communautes)
    st.write("On ne considère que les acteurs ayant joué dans au moins 2 films en commun.")
else:
    st.markdown("<span style='color: red;'>Aucune donnée disponible.</span>", unsafe_allow_html=True)

# 27. Films avec genres communs mais réalisateurs différents
st.header("27 - Films avec genres communs mais réalisateurs différents")
films_genres_realisateurs = r_neo4j.films_genres_communs_differents_realisateurs()
if films_genres_realisateurs:
    df_films_genres = pd.DataFrame(films_genres_realisateurs, columns=["Film1", "Director1", "Film2", "Director2", "SharedGenres"])
    st.dataframe(df_films_genres)
    st.write("On ne considère que les films ayant au moins 2 genres en commun.")
else:
    st.markdown("<span style='color: red;'>Aucune donnée disponible.</span>", unsafe_allow_html=True)

# 28. Recommandation de films aux utilisateurs en fonction des préférences d’un acteur donnée (Anne Hathaway)
st.header("28 - Recommandation de films aux utilisateurs en fonction des préférences d’un acteur donnée **(A SAISIR)**")
st.write("<span style='color: yellow;'>Par exemple, saisissez le nom de l'actrice Anne Hathaway et appuyez <Entrée>.</span>", unsafe_allow_html=True)
actor3 = st.text_input("Nom de l'acteur", key="actor3")
recommandations_preferences = r_neo4j.recommander_films_preferences(actor3)
if recommandations_preferences:
    for rec in recommandations_preferences:
        st.write(f"- {rec['RecommendedMovie']} (Genres communs: {', '.join(rec['MatchingGenres'])})")
    st.write("On considère les films ayant au moins 2 genres en commun par rapport aux genres de film d'Anne Hathaway.")
else:
    st.markdown("<span style='color: red;'>Aucune donnée disponible.</span>", unsafe_allow_html=True)

# 29. Création des relations de concurrence entre réalisateurs
st.header("29 - Création des relations de concurrence entre réalisateurs")
st.write("Attendre quelques secondes pour le chargement du graphique.")
graph_file = r_neo4j.display_concurrence_graph()
st.components.v1.html(open(graph_file, "r", encoding="utf-8").read(), height=500, scrolling=True)
st.write("On considère les films ayant au moins 2 genres en commun.")

# 30. Analyse des collaborations réalisateur-acteur et succès associé
st.header("30 - Analyse des collaborations réalisateur-acteur et succès associé")
collaborations_succes = r_neo4j.collaborations_succes()
if collaborations_succes:
    df_collaborations_succes = pd.DataFrame(collaborations_succes, columns=["Director", "Actor", "NumberOfFilmsTogether", "AvgRevenue", "AvgMetascore"])
    st.dataframe(df_collaborations_succes)
    st.write("On considère les collaborations entre acteurs et réalisateurs ayant au moins 2 films en commun.")
else:
    st.markdown("<span style='color: red;'>Aucune donnée disponible.</span>", unsafe_allow_html=True)
