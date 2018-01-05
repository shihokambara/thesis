# -*- coding: utf-8 -*-
import pandas as pd
pd.options.mode.chained_assignment = None
import numpy as np
import re
import nltk
import seaborn as sns
import networkx as nx

from gensim.models import word2vec

from sklearn.manifold import TSNE
import matplotlib.pyplot as plt


relationships = []

model = word2vec.Word2Vec.load("bible.model")
seed_word = 'god'
topn = 10

for a in model.most_similar(positive=seed_word , topn = topn):
    to_node1 = a[0]
    relationships.append([seed_word , to_node1 , 1])
    for b in model.most_similar(to_node1 , topn = topn):
        print(to_node1)
        to_node2 = b[0]
        relationships.append([to_node1 , to_node2, 2])
        for c in model.most_similar(to_node2 , topn = topn):
            to_node3 = c[0]
            relationships.append([to_node2 , to_node3 , 3])
#            for d in model.most_similar(to_node3 , topn = topn):
#                to_node4 = d[0]
#                relationships.append([to_node3 , to_node4 , 4])
#                for e in model.most_similar(to_node4 , topn = topn):
#                    to_node5 = e[0]
#                    relationships.append([to_node4 , to_node5 , 5])

relationships[0:30]
print(relationships)


# put relationships into a df
df_edges = pd.DataFrame(relationships,columns=["src","dst","step"])
# do some cleaning of things that are probably junk
df_edges = df_edges[df_edges["dst"].str.contains("_") == True]
df_edges = df_edges[df_edges["src"].str.contains("_") == True]

# add a weight to each edge if we so wished we could calculate something more fancy to put here
df_edges['weight'] = 1

# make a final list from the clean df
relationships_final = list(zip(df_edges['src'].tolist(),df_edges['dst'].tolist()))
relationships_final[0:20]

# make a networkx graph and save edges file
G = nx.from_pandas_dataframe(df_edges, 'src', 'dst', ['step','weight'])

# save the graph as a gml file
nx.write_gml(G, "edges.gml")

# Use R to run the make_network_graph.R script.
