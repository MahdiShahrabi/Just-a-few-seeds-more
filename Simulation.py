import numpy as np
import networkx as nx
import pandas as pd
from random import uniform
import random
import matplotlib.pyplot as plt 
import os

from SIRModel import Simulate_SIR
from ThresholdModel import Simulate_Thr


def simulation(Graph=nx.erdos_renyi_graph(200,0.01),method='SIR',c=0.5,dist_type=1,
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
    # Function dictionary for diffrent models
    switch_method = {'SIR':Simulate_SIR,'Threshold':Simulate_Thr}
    
    # Size of Graph
    lng = Graph.number_of_nodes()
    
    # Average Degree
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
    
    
    # Choosing the function based on the method
    func = switch_method[method]
    
    
    # Creating Thresholds based on the dist_type
    if dist_type==1:
        Thresholds = np.random.uniform(0,1,lng)        
        
    elif dist_type==2:
        l = np.random.normal(0.5,0.2,lng)
        Thresholds = [x if x>=0 and x<=1 else uniform(0.45,0.55) for x in l]
        
    elif dist_type==3:
        Thresholds = []
        dist = [(0,0.2),(0.2,0.8),(0.8,1)]
        weight = [45,10,45]
        weight_size = [np.round(x*lng/100) for x in weight]
        weight_size[-1] = weight_size[-1]+lng-sum(weight_size)
        for i in range(3):
            Thresholds = Thresholds + list(np.random.uniform(dist[i][0],dist[i][1],int(weight_size[i])))
        random.shuffle(Thresholds)
    
    elif dist_type==4:
        Thresholds = []
        dist = [(0,0.2),(0.2,0.8),(0.8,1)]
        weight = [20,10,70]
        weight_size = [np.round(x*lng/100) for x in weight]
        weight_size[-1] = weight_size[-1]+lng-sum(weight_size)
        for i in range(3):
            Thresholds = Thresholds + list(np.random.uniform(dist[i][0],dist[i][1],int(weight_size[i])))
        random.shuffle(Thresholds)
        
    elif dist_type==5:
        Thresholds = []
        dist = [(0,0.2),(0.2,0.8),(0.8,1)]
        weight = [70,10,20]
        weight_size = [np.round(x*lng/100) for x in weight]
        weight_size[-1] = weight_size[-1]+lng-sum(weight_size)
        for i in range(3):
            Thresholds = Thresholds + list(np.random.uniform(dist[i][0],dist[i][1],int(weight_size[i])))
        random.shuffle(Thresholds)
        
    elif dist_type==6:
        Thresholds = []
        dist = [(0,0.2),(0.2,0.8),(0.8,1)]
        weight = [10,80,10]
        weight_size = [np.round(x*lng/100) for x in weight]
        weight_size[-1] = weight_size[-1]+lng-sum(weight_size)
        for i in range(3):
            Thresholds = Thresholds + list(np.random.uniform(dist[i][0],dist[i][1],int(weight_size[i])))
        random.shuffle(Thresholds)
    
    # "Simulation Sarted" message!
    if method=='SIR':
        print('Simulation on the Model "SIR" with c={} has started:'.format(c))
    else: 
        print('Simulation on the Model "Threshold" with dist_type={} has started:'.format(dist_type))
    
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
            plt.title('Graph size: {},   Average degree: {:0.2f},   Model: {},   c: {}'.format(lng,d_bar,method,c),fontsize=10)
            plot_name = 'SIR_c'+str(c)+'_d'+str(d_bar)+'.png'
        else:
            plt.title('Graph size:{},   Average degree: {:0.2f},   Model:{},   Threshold distribution: dist_type{}'.format(
                lng,d_bar,method,dist_type),fontsize=10)
            plot_name = 'Threshold_distType'+str(dist_type)+'_d'+str(d_bar)+'.png'
        plt.legend(fontsize=10)
        plt.tight_layout()
        plt.subplots_adjust(top=.9)
        os.chdir(r"C:\Users\Mahdi\OneDrive\Just A Few Seeds More\Photos")
        plt.savefig(plot_name)
        plt.show()
    
    return(out)