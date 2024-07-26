'''
PART 1: NETWORK CENTRALITY METRICS

Using the imbd_movies dataset
- Guild a graph and perform some rudimentary graph analysis, extracting centrality metrics from it. 
- Below is some basic code scaffolding that you will need to add to. 
- Tailor this code scaffolding and its stucture to however works to answer the problem
- Make sure the code is line with the standards we're using in this class 
'''

import json
import networkx as nx
import pandas as pd
from datetime import datetime

def build_graph(file_path):
    """
    Build a graph from the IMDB movies dataset, calculate centrality metrics, and save the results to a CSV file.

    Parameters:
    file_path (str): The path to the JSON file containing the IMDB movies dataset.

    Returns:
    networkx.Graph: The graph built from the dataset.
    """
    #create empty graph
    g = nx.Graph()
    # Open the JSON file and read it line by line
    with open(file_path, 'r') as f:
        # Parse each line as a JSON object representing a movie
        for line in f:
            this_movie = json.loads(line)
            actors = [(actor[0], actor[1]) for actor in this_movie.get('actors', [])]
            for i, (left_actor_id, left_actor_name) in enumerate(actors):
                for right_actor_id, right_actor_name in actors[i + 1:]:
                    if g.has_edge(left_actor_id, right_actor_id):
                        g[left_actor_id][right_actor_id]['weight'] += 1
                    else:
                        g.add_edge(left_actor_id, right_actor_id, weight=1)
    # Calculate degree centrality for each node (actor) in the graph
    centrality = nx.degree_centrality(g)
    centrality_df = pd.DataFrame(centrality.items(), columns=['actor_id', 'centrality'])
    actor_names_df = pd.DataFrame(actors, columns=['actor_id', 'actor_name']).drop_duplicates()
    centrality_df = centrality_df.merge(actor_names_df, on='actor_id')
    centrality_df = centrality_df.sort_values(by='centrality', ascending=False).head(10)
    # Generate a timestamp for the output filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_path = f'data/network_centrality_{timestamp}.csv'
    centrality_df.to_csv(output_path, index=False)
     # Print the number of nodes and the output file path
    print(f"Nodes: {g.number_of_nodes()}")
    print(f"Output saved to {output_path}")

    return g



