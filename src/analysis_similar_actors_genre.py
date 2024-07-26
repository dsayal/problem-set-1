'''
PART 2: SIMILAR ACTROS BY GENRE
Using the imbd_movies dataset:
- Create a data frame, where each row corresponds to an actor, each column represents a genre, and each cell captures how many times that row's actor has appeared in that column’s genre 
- Using this data frame as your “feature matrix”, select an actor (called your “query”) for whom you want to find the top 10 most similar actors based on the genres in which they’ve starred 
- - As an example, select the row from your data frame associated with Chris Hemsworth, actor ID “nm1165110”, as your “query” actor
- Use sklearn.metrics.DistanceMetric to calculate the euclidean distances between your query actor and all other actors based on their genre appearances
- - https://scikit-learn.org/stable/modules/generated/sklearn.metrics.DistanceMetric.html
- Output a CSV continaing the top ten actors most similar to your query actor using cosine distance 
- - Name it 'similar_actors_genre_{current_datetime}.csv' to `/data`
- - For example, the top 10 for Chris Hemsworth are:  
        nm1165110 Chris Hemsworth
        nm0000129 Tom Cruise
        nm0147147 Henry Cavill
        nm0829032 Ray Stevenson
        nm5899377 Tiger Shroff
        nm1679372 Sudeep
        nm0003244 Jordi Mollà
        nm0636280 Richard Norton
        nm0607884 Mark Mortimer
        nm2018237 Taylor Kitsch
- Describe in a print() statement how this list changes based on Euclidean distance
- Make sure your code is in line with the standards we're using in this class
'''

#Write your code below
import json
import pandas as pd
from sklearn.metrics import pairwise_distances
from datetime import datetime

def build_genre_df(file_path):
    """
    Build a DataFrame where each row corresponds to an actor and each column represents a genre.
    Each cell captures how many times the actor has appeared in that genre.

    Parameters:
    file_path (str): The path to the JSON file containing the IMDB movies dataset.

    Returns:
    pd.DataFrame: DataFrame where each row represents an actor and columns represent genre counts.
    dict: Dictionary mapping actor IDs to actor names.
    """
     # Open the JSON file and read it line by line
    with open(file_path, 'r') as f:
        movies = [json.loads(line) for line in f]

    # Extract unique genres
    unique_genres = set()
    for movie in movies:
        for genre in movie.get('genres', []):
            unique_genres.add(genre)
    
    genre_list = list(unique_genres)

    # Create a dictionary to count genre appearances
    actor_genre_count = {}
    actor_names = {}

    for movie in movies:
        actors = movie.get('actors', [])
        genres = movie.get('genres', [])
        for actor_id, actor_name in actors:
            if actor_id not in actor_genre_count:
                actor_genre_count[actor_id] = [0] * len(genre_list)
                actor_names[actor_id] = actor_name
            for genre in genres:
                if genre in genre_list:
                    genre_index = genre_list.index(genre)
                    actor_genre_count[actor_id][genre_index] += 1

    # Create DataFrame
    genre_df = pd.DataFrame.from_dict(actor_genre_count, orient='index', columns=genre_list)
    genre_df.index.name = 'actor_id'

    return genre_df, actor_names

def find_similar_actors(genre_df, actor_names):
    query_actor_id = 'nm1165110'  # Chris Hemsworth's actor ID
    query_actor_genres = genre_df.loc[query_actor_id].values.reshape(1, -1)
    distances = pairwise_distances(genre_df, query_actor_genres, metric='cosine').flatten()
    similar_indices = distances.argsort()[1:11]  # Exclude the first one since it's the query actor

    similar_actors = genre_df.iloc[similar_indices]
    similar_actors['distance'] = distances[similar_indices]
    similar_actors = similar_actors.reset_index()
    similar_actors['actor_name'] = similar_actors['actor_id'].map(actor_names)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_path = f'data/similar_actors_genre_{timestamp}.csv'
    similar_actors[['actor_id', 'actor_name', 'distance']].to_csv(output_path, index=False)

    print(f"Output saved to {output_path}")
    print(similar_actors[['actor_id', 'actor_name', 'distance']])

if __name__ == "__main__":
    file_path = 'data/imdb_movies_2000to2022.prolific.json'
    genre_df, actor_names = build_genre_df(file_path)
    find_similar_actors(genre_df, actor_names)

