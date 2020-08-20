import numpy as np
import networkx as nx

## Functions for generating seeds
def generateRandSeed(num,Graph):
    """ A simple function to generate "num" random seeds"""
    return(np.random.choice(list(range(Graph.number_of_nodes())),num,replace=False))

def generateEigSeed(num,Graph):
    """ A simple function to find "num" seeds with highest eigen-vector centrality """
    eig_cen=nx.eigenvector_centrality_numpy(Graph)
    return(list({key: eig_cen[key] for key in sorted(eig_cen, key=eig_cen.get, reverse=True)[:num]}))

def generateDegSeed(num,Graph):
    """ A simple function to find "num" seeds with highest degree centrality """
    deg_cen=nx.degree_centrality(Graph)
    return(list({key: deg_cen[key] for key in sorted(deg_cen, key=deg_cen.get, reverse=True)[:num]}))