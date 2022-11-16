#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 15 11:28:53 2022

@author: mahdishahrabi
"""
from numpy.random import uniform

@profile
def check(K=1000000):
    for i in range(10):
        a = uniform(0,1,K)
        
    for i in range(10):
        for j in range(K):
            a = uniform(0, 1)
    return a      
            
check(K=1000000)