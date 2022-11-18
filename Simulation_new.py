#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 15 15:16:51 2022
@author: Mahdi Shahrabi

Simulating SIR Model
"""

import GenerateSeed as GS
import networkx as nx
import pandas as pd
import numpy as np
from random import uniform


## SIR Simulation
# @profile
def SIR (Graph,Neighbors_List,c=0.3, Seeds = [1],Neighbors_List_provided = False):
    """ A function to run "SIR" model simulation on a Graph 
        
    ...
    Parameters
    ----------
    Graph: networkx.Graph,
        A graph to run the simulation on
        
    c: float, default values is 0.3
        The probabilty of passing information to another node.
        
   Seeds: list, default value is [1]
        Initial infected nodes
        
   Neighbors_List: list of sets,
       List of neighbors for each node
       
  Neighbors_List_provided: boolean, default value = False
    if list is not provided we calculate list ourselves
    """
    
    # Size of Graph
    lng = Graph.number_of_nodes()
        
    # Creating Neighbor List if it is not provided
    if not Neighbors_List_provided:
        Neighbors_List = []
        Nodes = list(Graph.nodes())
        Nodes.sort(reverse=False)
        # Finding Neighbors of each node
        for node in list(Nodes):
            Neighbors_List.append(set(dict(Graph.adj[node])))
   
        

    # Initializing the Status Lists of Normal and Informed Nodes
    Normal = list(range(lng))
    Informed = list()

    # Adding initial seeds to Informed list
    Informed = [x for x in Seeds]

    # Removing Informeds from Normal list
    Normal = list(set(Normal) - set(Informed))

    ## SIR Process
    # For each Informed node we try to find the transmissions
    for node in Informed:
        
        ## Finding the Neighbors of the node based which are not informed already
        Neighbors = Neighbors_List[node] - set(Informed)
        # for each uninformed neighbor
        for advicee in Neighbors:   
            
            # it Gets information with probability 'c'
            if  uniform(0,1)<c:
                Normal.remove(advicee)
                Informed.append(advicee)

        
    
    # Returning a dataframe of Seedsize and average cascade size
    return len(Informed)




# Runing simulation for an specific c and number of Seeds
def Simulate_SIR(c=0.3,number_of_seeds=5) -> pd.DataFrame:
    # Simulation config: Monte Carlo
    Number_of_graphs = 20             # Number of different erdos graphs
    Number_of_draw = 10   # Number of different random seeds for random seeding
    Number_of_repeats = 50            # Repeating for each set of seeds in a specific graph
    

    
    # Erdos Random Graph Conifg
    n = 500
    p = 0.01
    
    
    ## Running Code
    
    CascadeRand = []
    CascadeDeg = []
    CascadeEig = []
    
    # Iteration over graphs
    for g in range(Number_of_graphs):
        
        # Creating graph and finding neighbors of each node
        G = nx.erdos_renyi_graph(n,p)
        Neighbors_List = []
        Nodes = list(G.nodes())
        Nodes.sort(reverse=False)
        # Finding Neighbors of each node
        for node in list(Nodes):
            Neighbors_List.append(set(dict(G.adj[node])))
            
        # Generating seeds
        Seeds_Eig = GS.generateEigSeed(number_of_seeds,G)
        Seeds_Deg = GS.generateDegSeed(number_of_seeds,G)
        
        
        # Iteration over draws
        for rpt in range(Number_of_repeats):
            
            
            # Iteration over draws of Seeds for Random Seeding
            for d in range(Number_of_draw):
                
                Seeds_Rand = GS.generateRandSeed(number_of_seeds,G)
                
                # Simulation for Random seeding
                ans = SIR(G,Neighbors_List,c = c, Seeds = Seeds_Rand, Neighbors_List_provided = True)
                CascadeRand.append(ans)
                
            
            # Simulation for Degree Centrality
            ans = SIR(G,Neighbors_List,c = c, Seeds = Seeds_Deg, Neighbors_List_provided = True)   
            CascadeDeg.append(ans)
            
            # Simulation for Eigen-Vector Centrality
            ans = SIR(G,Neighbors_List,c = c, Seeds = Seeds_Eig, Neighbors_List_provided = True)   
            CascadeEig.append(ans)
    
    
    out = {'C':[c],'Seed':[number_of_seeds],
           'Rand_m':[np.round(np.mean(CascadeRand),2)], 'Rand_s':[np.round(np.std(CascadeRand),2)],
           'Deg_m' :[np.round(np.mean(CascadeDeg),2)],   'Deg_s':[np.round(np.std(CascadeDeg),2)],
           'Eig_m' :[np.round(np.mean(CascadeEig),2)],   'Eig_s':[np.round(np.std(CascadeEig),2)]}
    
    return pd.DataFrame(out)
        
        
b = Simulate_SIR(c=0.3,number_of_seeds=10)           


