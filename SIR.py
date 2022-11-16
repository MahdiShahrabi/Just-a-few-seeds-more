import numpy as np
import networkx as nx
import pandas as pd
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





# Example to rest funciton
G = nx.erdos_renyi_graph(1000,0.006)
Neighbors_List = []
Nodes = list(G.nodes())
Nodes.sort(reverse=False)
# Finding Neighbors of each node
for node in list(Nodes):
    Neighbors_List.append(set(dict(G.adj[node])))

ans = SIR(G,Neighbors_List,c=0.3, Seeds = [1,10,40],Neighbors_List_provided = True)


