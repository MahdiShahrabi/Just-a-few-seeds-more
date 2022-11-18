#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 18 10:48:06 2022

@author: mahdishahrabi

Running Over Grid of Seeds and Cs
"""
import pandas as pd
import numpy as np
from Simulation_new import Simulate_SIR
from Simulation_new import SIR
import itertools as it
import multiprocessing


# Seeds
NUM_SEED = list(range(1,3))



# Comunicatoin Probabilities
sub_c = list(np.linspace(0,0.15,2))
main_c = list(np.linspace(0.16,0.4,2))
over_c = list(np.linspace(0.41,1,2))

C = sub_c + main_c + over_c




# Output
OUT = pd.DataFrame()

with multiprocessing.Pool() as pool:
    
    items = list(it.product(C,NUM_SEED))
    for result in pool.starmap(Simulate_SIR, items):
        OUT = pd.concat([OUT,result])




# # Iterating over grades
# for c in C:
#     for num_seed in NUM_SEED:
#         # print(f'*C = { c} and *num_seed = {num_seed}', flush=True)
#         # out = Simulate_SIR(c = c,number_of_seeds = num_seed)
        
#         # OUT = pd.concat([OUT,out])
#         pass
        
        
        
        