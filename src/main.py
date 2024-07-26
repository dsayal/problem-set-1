'''
Pull down the imbd_movies dataset here and save to /data as imdb_movies_2000to2022.prolific.json
You will run this project from main.py, so need to set things up accordingly
'''

import json
import os
import requests
from datetime import datetime
import analysis_network_centrality
import analysis_similar_actors_genre

# Ingest and save the imbd_movies dataset
DATA_URL = "https://github.com/cbuntain/umd.inst414/blob/main/data/imdb_movies_2000to2022.prolific.json?raw=true"
LOCAL_DATA_PATH = "data/imdb_movies_2000to2022.prolific.json"

def download_dataset(url, path):
    if not os.path.exists(path):
        import urllib.request
        print(f"Downloading dataset from {url}")
        urllib.request.urlretrieve(url, path)
        print(f"Dataset downloaded and saved to {path}")
    else:
        print(f"Dataset already exists at {path}")

def main():
    # Ensure data directory exists
    os.makedirs('data', exist_ok=True)
    
    # Download the dataset if it does not exist
    download_dataset(DATA_URL, LOCAL_DATA_PATH)

    # Build the graph and find central actors
    g = analysis_network_centrality.build_graph(LOCAL_DATA_PATH)
    
    # Create the genre DataFrame
    genre_df, actor_names = analysis_similar_actors_genre.build_genre_df(LOCAL_DATA_PATH)
    
    # Find similar actors
    analysis_similar_actors_genre.find_similar_actors(genre_df, actor_names)

if __name__ == "__main__":
    main()
