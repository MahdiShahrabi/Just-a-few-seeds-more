import numpy as np
import networkx as nx
import pandas as pd
from random import uniform
import random
import pickle
import matplotlib.pyplot as plt 
import os

from SIRModel import Simulate_SIR
from ThresholdModel import Simulate_Thr
from Threshold_dist import Threshold_dist


def simulation(network={'type':'Erdos','size':1000,'d':2},method='SIR',c=0.5,dist_type=1,
               plot=['Random','Eigen','Degree'],numSeed=20,Repeat=50,plot_show=True):
    """ A function to run different simulation and plot the results 
        
    ...
    Parameters
    ----------
    Graph: networkx.Graph, default is an Erdos-Renyi graph with n=200 and p=0.01
        A graph to run the simulation on
    
    method: str, default is "SIR"
        The model of cascade.
        Must be one of ['SIR','Threshold']
        
    dist_type: int, default values is 1
        The distribution of nodes thresholds.
        Only necessay when using 'Threshold' method.
        
    c: int, default values is 0.3
        The probabilty of passing information to another node.
        Only necessay when using 'SIR' method.
        
    numSeed: int, default value is 20
        We check seeds size 1,2,....,numSeed.
        "numseed" must be smaller than graph size
        
    Repeat: int, default value is 50
        Number of repeats.
    
    plot: list of str, default value is ['Degree','Random','Eigen']
        The method to generate seeds and run the simulations.
        It must be a subset of the ['Degree','Random','Eigen']
    """
    # GraphType
    if network['type'] is 'Erdos':
        n = network['size']
        d = network['d']
        Graph = nx.erdos_renyi_graph(n,d/n)       
        
    elif network['type'] is 'Facebook':
        os.chdir(r'C:\Users\Mahdi\OneDrive\Just A Few Seeds More\Just-a-few-seeds-more')
        with open('FaceBookGraph', 'rb') as f:
             Graph = pickle.load(f)
                
    elif network['type'] is 'IndianVillage':
        os.chdir(r'C:\Users\Mahdi\OneDrive\Just A Few Seeds More\Just-a-few-seeds-more')
        with open('IndianVillage', 'rb') as f:
             Graph = pickle.load(f)
    
    
    
    # Function dictionary for diffrent models
    switch_method = {'SIR':Simulate_SIR,'Threshold':Simulate_Thr}
    
    # Size of Graph
    lng = Graph.number_of_nodes()
    
    # Average Degree
    if network['type'] is 'Erdos':
        d_bar = network['d']
    else:
        d_bar = np.round(np.mean(list(dict(Graph.degree()).values())),1)
    
    # Checking the validity of inputs
    if numSeed>lng:
        raise ValueError('"numSeed" cannot be larger than Graph size')
        
    if len([x for x in plot if x not in ['Random','Eigen','Degree']])>0:
        raise ValueError('"plot" must be in ["Random","Eigen","Degree"]')
        
    if Repeat<=0:
        raise ValueError('"Repeat" must be larger than 0!')
        
    if not isinstance(Graph,nx.Graph):
        raise ValueError('"Graph" must be a networkx.Graph object!')
        
    if c>1 or c<0:
        raise ValueError('"c" elements must be between 0 and 1!')
        
    if dist_type not in [1,2,3,4,5,6]:
        raise ValueError('"dist_type" must be in [1,2,3,4,5,6]!')
        
    if method not in ['SIR','Threshold']:
        raise ValueError('"method" must be "SIR" or "Threshold"')
    
    
    # Creating Thresholds based on the dist_type
    Thresholds = Threshold_dist(lng,dist_type)
    
    # Choosing the function based on the method
    func = switch_method[method]
    
    
    # "Simulation Sarted" message!
    if method=='SIR':
        print('Simulation on the Model "SIR" with c={} has started (Graph Type={}):'.format(c,network['type']))
    else: 
        print('Simulation on the Model "Threshold" with dist_type={} has started (Graph Type={}):'.format(dist_type,network['type']))
    
    # declaring outputlist
    out = []
    
    # for each element in the plot we run the simulation
    for X in plot:
        if method=='SIR':
            out.append(func(Graph=Graph,c=c, numSeed=numSeed, Repeat=Repeat,how=X))
        elif method=='Threshold': 
            out.append(func(Graph=Graph,Thr=Thresholds, numSeed=numSeed, Repeat=Repeat, how=X))
        print(X,' is done!')
    
    if plot_show:
        ### Ploting the results 
        fig, ax1 = plt.subplots(1,1,figsize=(10,6), dpi= 180)
        colors = {'Random':'black','Degree':'red','Eigen':'blue'}
        for i in range(len(plot)):
            ax1.plot(out[i].SeedSize,out[i].Cascade,color=colors[plot[i]],lw=1,label=plot[i])
            ax1.scatter(out[i].SeedSize,out[i].Cascade,s=[5],marker='o',color=colors[plot[i]])

        ax1.tick_params(axis='x', labelsize=10)
        ax1.set_ylabel('Percentage',color='blue', fontsize=10)
        ax1.tick_params(axis='y', labelcolor='tab:blue',labelsize=10 )
        ax1.set_xticks(out[i].SeedSize[::1])
        ax1.set_xticklabels(out[i].SeedSize[::1])
        ax1.grid(alpha=.4,axis='x')
        ax1.grid(alpha=.4,axis='y')
        plt.suptitle('      Cascade Size vs Number of Seeds '.format(lng,method),fontsize=15,y=0.98)
        if method == 'SIR':
            plt.title('Graph Type: {}, Graph size={},   Average degree={:0.2f},   Model: {},   c={}'.format(network['type'],lng,d_bar,method,c),fontsize=10)
            plot_name = 'SIR_c'+str(c)+'_d'+str(d_bar)+'.png'
        else:
            plt.title('Graph Type: {}, Graph Size={},   Average Degree= {:0.2f},   Model:{},   Threshold Distribution: dist_type{}'.format(network['type'],lng,d_bar,method,dist_type),fontsize=10)
            plot_name = network['type']+'_Threshold_distType'+str(dist_type)+'_d'+str(d_bar)+'.png'
        plt.legend(fontsize=10)
        plt.tight_layout()
        plt.subplots_adjust(top=.9)
        os.chdir(r"C:\Users\Mahdi\OneDrive\Just A Few Seeds More\Photos")
        plt.savefig(plot_name)
        plt.show()
    
    return(out)