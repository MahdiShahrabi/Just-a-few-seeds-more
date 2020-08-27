import numpy as np
import networkx as nx
import pandas as pd
from random import uniform
import random


## Generating Threshold_dist
def Threshold_dist (lng,dist_type):

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
        
    return(Thresholds)