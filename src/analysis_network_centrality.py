'''
PART 1: NETWORK CENTRALITY METRICS

Using the imbd_movies dataset
- Guild a graph and perform some rudimentary graph analysis, extracting centrality metrics from it. 
- Below is some basic code scaffolding that you will need to add to. 
- Tailor this code scaffolding and its stucture to however works to answer the problem
- Make sure the code is line with the standards we're using in this class 
'''

import numpy as np
import json
import networkx as nx
import pandas as pd
from datetime import datetime

# Build the graph
g = nx.Graph()

with open(file_path, 'r') as f:
    for line in f:
        this_movie = json.loads(line)
        # Print the structure to understand it
        print(this_movie)  
            
        # Extract actors correctly
        actors = [(actor[0], actor[1]) for actor in this_movie.get('actors', [])]
            for actor_id, actor_name in actors:
                g.add_node(actor_id, actor_name=actor_name)
            
            for i, (left_actor_id, left_actor_name) in enumerate(actors):
                for right_actor_id, right_actor_name in actors[i+1:]:
                    current_weight = g[left_actor_id][right_actor_id]['weight'] if g.has_edge(left_actor_id, right_actor_id) else 0
                    g.add_edge(left_actor_id, right_actor_id, weight=current_weight + 1)
    
    print(f"Nodes: {len(g.nodes)}")
    
    centrality = nx.degree_centrality(g)
    centrality_df = pd.DataFrame({
        'actor_name': [g.nodes[node]['actor_name'] for node in centrality.keys()],
        'centrality': list(centrality.values()),
        'unique_id': list(centrality.keys())
    })
    centrality_df.sort_values(by='centrality', ascending=False, inplace=True)
    output_path = f"data/network_centrality_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    centrality_df.to_csv(output_path, index=False)
    print(f"Output saved to {output_path}")


