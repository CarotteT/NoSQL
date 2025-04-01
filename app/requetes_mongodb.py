import pymongo
import pandas as pd
import scipy.stats as stats
from scipy.stats import pearsonr
from connexion_mongodb import get_mongo_collection  

films = get_mongo_collection()

# 1. Afficher l’année où le plus grand nombre de films ont été sortis.
def annee_avec_plus_de_films():
    result = list(films.aggregate([
        {"$group": {"_id": "$year", "total_films": {"$sum": 1}}},
        {"$sort": {"total_films": -1}},
        {"$limit": 1}
    ]))
    return result

# 2. Quel est le nombre de films sortis après l’année 1999.
def nombre_de_films_apres_1999():
    result = list(films.aggregate([
        {"$match": {"year": {"$gt": 1999}}},
        {"$count": "total_films_after_1999"}
    ]))
    return result

# 3. Quelle est la moyenne des votes des films sortis en 2007.
def moyenne_votes_2007():
    result = list(films.aggregate([
        {"$match": {"year": 2007}},
        {"$group": {"_id": None, "avg_votes": {"$avg": "$Votes"}}}
    ]))
    return result

# 4. Affichez un histogramme qui permet de visualiser le nombre de films par année.
def films_par_annee():
    result = list(films.aggregate([
        {"$group": {"_id": "$year", "count": {"$sum": 1}}},
        {"$sort": {"_id": 1}}
    ]))
    return result

# 5. Quels sont les genres de films disponibles dans la base ?
def genres_disponibles():
    result = list(films.aggregate([
        {"$project": {"genre": {"$split": ["$genre", ","]}}},
        {"$unwind": "$genre"},
        {"$group": {"_id": "$genre"}}
    ]))
    return result

# 6. Quel est le film qui a généré le plus de revenu ?
def film_avec_plus_gros_revenu():
    result = list(films.aggregate([
        {"$match": {"Revenue (Millions)": {"$ne": ""}}},
        {"$sort": {"Revenue (Millions)": -1}},
        {"$limit": 1}
    ]))
    return result

# 7. Quels sont les réalisateurs ayant réalisé plus de 5 films dans la base de données ?
def realisateurs_avec_plus_de_5_films():
    result = list(films.aggregate([
        {"$group": {"_id": "$Director", "number_of_films": {"$sum": 1}}},
        {"$match": {"number_of_films": {"$gt": 5}}}
    ]))
    return result

# 7 bis. 
def realisateurs_avec_plus_de_2_films():
    result = list(films.aggregate([
        {"$group": {"_id": "$Director", "number_of_films": {"$sum": 1}}},
        {"$match": {"number_of_films": {"$gt": 2}}}
    ]))
    return result

# 8. Quel est le genre de film qui rapporte en moyenne le plus de revenus ?
def genre_avec_plus_gros_revenu_moyen():
    result = list(films.aggregate([
        {"$match": {"Revenue (Millions)": {"$ne": ""}}},
        {"$project": {"genre": {"$split": ["$genre", ","]}, "revenue": {"$toDouble": "$Revenue (Millions)"}}},
        {"$unwind": "$genre"},
        {"$group": {"_id": "$genre", "avg_revenue": {"$avg": "$revenue"}}},
        {"$sort": {"avg_revenue": -1}},
        {"$limit": 1}
    ]))
    return result

# 9. Quels sont les 3 films les mieux notés (rating) pour chaque décennie ?
def top_3_films_par_decennie():
    result = list(films.aggregate([
        {"$match": {"rating": {"$ne": ""}}},
        {"$addFields": {"decade": {"$subtract": [{"$toInt": "$year"}, {"$mod": [{"$toInt": "$year"}, 10]}]}}},
        {"$sort": {"decade": 1, "rating": -1}},
        {"$group": {"_id": "$decade", "top_movies": {"$push": {"title": "$title", "rating": "$rating"}}}},
        {"$project": {"_id": 1, "top_movies": {"$slice": ["$top_movies", 3]}}},
        {"$sort": {"_id": 1}}
    ]))
    return result

# 9 bis.
def top_3_films_par_decenniebis():
    result = list(films.aggregate([
        {"$match": {"Metascore": {"$ne": ""}}}, 
        {"$addFields": {"decade": {"$subtract": [{"$toInt": "$year"}, {"$mod": [{"$toInt": "$year"}, 10]}]}}},  
        {"$addFields": {"Metascore": {"$toInt": "$Metascore"}}},  
        {"$sort": {"decade": 1, "Metascore": -1}},  
        {"$group": {"_id": "$decade", "top_movies": {"$push": {"title": "$title", "Metascore": "$Metascore"}}}}, 
        {"$project": {"_id": 1, "top_movies": {"$slice": ["$top_movies", 3]}}},  
        {"$sort": {"_id": 1}}
    ]))
    return result

# 10. Quel est le film le plus long (Runtime) par genre ?
def film_le_plus_long_par_genre():
    result = list(films.aggregate([
        {"$match": {"Runtime (Minutes)": {"$ne": ""}}},
        {"$project": {"genre": {"$split": ["$genre", ","]}, "title": 1, "runtime": {"$toInt": "$Runtime (Minutes)"}}},
        {"$unwind": "$genre"},
        {"$sort": {"runtime": -1}},
        {"$group": {"_id": "$genre", "longest_film": {"$first": {"title": "$title", "Runtime": "$runtime"}}}}
    ]))
    return result

# 11. Créer une vue MongoDB affichant uniquement les films ayant une note supérieure à 80 et généré plus de 50 millions de dollars.
def creer_vue_top_films():
    pipeline = [
        {"$match": {"Metascore": {"$ne": "", "$gt": 80}, "Revenue (Millions)": {"$ne": "", "$gt": 50}}}, 
        {"$project": {"title": 1, "year": 1, "Metascore": {"$toInt": "$Metascore"}, "revenue": {"$toDouble": "$Revenue (Millions)"}}}
    ]
    result = list(films.aggregate(pipeline))
    if result:
        try:
            films["top_movies"].insert_many(result, ordered=False, bypass_document_validation=True)
            print("Vue 'top_movies' créée avec succès.")
        except pymongo.errors.BulkWriteError as e:
            print(f"Erreur lors de l'insertion des films : {e.details}")
    else:
        print("Aucun film trouvé correspondant aux critères.")
    top_movies = films["top_movies"].find()
    top_movies_list = list(top_movies)
    return top_movies_list

# 12. Calculer la corrélation entre la durée des films (Runtime) et leur revenu (Revenue).
def correlation_duree_revenu1():
    data = list(films.aggregate([
        {"$match": {"Runtime (Minutes)": {"$ne": ""}, "Revenue (Millions)": {"$ne": ""}}},
        {"$project": {"title": 1, "runtime": {"$toInt": "$Runtime (Minutes)"}, "revenue": {"$toDouble": "$Revenue (Millions)"}}}
    ]))
    if data:
        df = pd.DataFrame(data)
        correlation = stats.pearsonr(df["runtime"], df["revenue"])[0]
        return df, correlation
    return None, None

# 13. Y a-t-il une évolution de la durée moyenne des films par décennie ?
def evolution_duree_moyenne_par_decennie():
    result = list(films.aggregate([
        {"$match": {"Runtime (Minutes)": {"$ne": ""}, "year": {"$ne": ""}}},
        {"$project": {"decade": {"$subtract": [{"$toInt": "$year"}, {"$mod": [{"$toInt": "$year"}, 10]}]}, "runtime": {"$toInt": "$Runtime (Minutes)"}}},
        {"$group": {"_id": "$decade", "avg_runtime": {"$avg": "$runtime"}}},
        {"$sort": {"_id": 1}}
    ]))
    return result

# Fonction pour calculer la corrélation entre la durée et le revenu des films
def correlation_duree_revenu():
    pipeline = [
        {"$match": {"Runtime (Minutes)": {"$ne": ""}, "Revenue (Millions)": {"$ne": ""}}},
        {"$project": { 
            "title": 1,
            "runtime": { "$toInt": "$Runtime (Minutes)" }, 
            "revenue": { "$toDouble": "$Revenue (Millions)" }
        }}
    ]
    data = list(films.aggregate(pipeline))
    df = pd.DataFrame(data)
    df = df.dropna(subset=["runtime", "revenue"])
    if len(df) > 1:
        correlation, p_value = pearsonr(df["runtime"], df["revenue"])
        return correlation, p_value
    else:
        return "Pas assez de données pour calculer une corrélation."
