import numpy as np
import networkx as nx
import pandas as pd
from random import uniform
import random

from GenerateSeed import generateRandSeed
from GenerateSeed import generateEigSeed
from GenerateSeed import generateDegSeed

## Threshold Simulation
def Simulate_Thr (Graph,Thr=[uniform(0,1) for x in range(100)], numSeed = 20, Repeat=50 ,how='Degree'):
    """ A function to run "Threshold" model simulation on a Graph 
    
    ...
    Parameters
    ----------
    Graph: networkx.Graph,
        A graph to run the simulation on
        
    Thr: list, default values in uniformly random numbers between 0 and 1
        A list of nodes thresholds
        
    numSeed: int, default value is 20
        We check seeds size 1,2,....,numSeed.
        "numseed" must be smaller than graph size
        
    Repeat: int, default value is 50
        Number of repeats.
    
    how: str, default value is "Degree"
        The method to generate seeds.
        It must be one of the ['Degree','Random','Eigen']
    """
    
    # Dictionary for seed generation
    switch_seed_method = {'Random':generateRandSeed,'Eigen':generateEigSeed,'Degree':generateDegSeed}    
    
    # Size of Graph
    lng = Graph.number_of_nodes()
    
    # Declaring the list of cascade size for each seedsize
    Cascade_size =[]
        
    # Creating Neighbor List
    Neighbors_List = []
    Nodes = list(Graph.nodes())
    Nodes.sort(reverse=False)
    # Finding Neighbors of each node
    for node in list(Nodes):
        Neighbors_List.append(list(dict(Graph.adj[node])))
        
    # If the seeding method is either Degree or Eigen, we only need...
    #... find all the numSeed central nodes, and then pick sizeS first of it    
    if how=='Degree' or how=='Eigen':
        SPSeeds = switch_seed_method[how](numSeed,Graph)

    # for each seed size
    for sizeS in list(np.arange(1,numSeed+1,1)):
        
        # Cascade size in each repeat
        Cascade_size_rpt =[]
        
        # Repeating the procee
        for rpt in range(Repeat):
            
            # Shuffling the Thresholds (Node have different thresholds in diffrent repeatitions)
            random.shuffle(Thr)
           
            # Generating Seeds
            if how=='Random':
                Seeds = switch_seed_method[how](sizeS,Graph)
            else:
                Seeds = SPSeeds[:sizeS]

            # Initializing the Status Lists of Normal and Informed Nodes  
            Normal = list(range(lng))
            Informed = list()
            New_Informed = []

            # Adding initial seeds to Informed list
            Informed = [x for x in Seeds]

            # Removing Informeds from Normal list
            Normal = [x for x in Normal if x not in Informed]
            
            # We iterate through nodes and find the nodes that fraction of their informed neighbors...
            # ... exceed their threshold. When we converge to the fixed point (size of informed stays constant),...
            # ... we break the loop.
            while True:
                
                # We set the Informed_last_size before starting to find new informeds
                Informed_last_size = len(Informed)
                
                # For nomal nodes
                for node in Normal:

                    # Finding informed Neighbors of the node
                    Informed_Neighbors = [k for k in Neighbors_List[node] if k in Informed]
 
                    # Calculating the fraction of neighbors which are informed
                    try:
                        thr = len(Informed_Neighbors)/len(Neighbors_List[node])
                    except:
                        thr = 0

                    if  thr>Thr[node]:
                        Informed.append(node)
                
                # Removind nodes that are informed from the Normal set
                Normal = [x for x in Normal if x not in Informed]
                
                # If there is no new Informed or all nodes are informed, we break the loop.
                if len(Informed)==Informed_last_size or len(Informed)==lng:
                    break
            
            # At the end each repeat (when all informed nodes have a chance to talk to their neighbors),...
            # ... we store the cascade size        
            Cascade_size_rpt.append(len(Informed))

        # Calculating average over all repeats, and deviding by size of graph to calculate the percentage
        Cascade_size.append(np.mean(Cascade_size_rpt)/lng)  
    
    # Returning a dataframe of Seedsize and average cascade size
    return(pd.DataFrame(data={'SeedSize':list(np.arange(1,numSeed+1,1)),'Cascade':Cascade_size}))