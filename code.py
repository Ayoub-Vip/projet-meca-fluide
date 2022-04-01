"""
Created on Thu Mar 24 16:21:01 2022

@author: USER
"""

import numpy as np


def getCoeff(num_left,num_right,num_down,num_up,num_cent,type_cent,cl_cent):
    if type_cent == 0:
        return 0
    
    if type_cent == 2:
        a = np.array([[1]])
        j = np.array([[num_cent]])
        b = cl_cent
       
    
    if type_cent == 1:
        a = np.array([[1],[1],[1],[1],[-4]])
        b = 0
        j = np.array([[num_left], [num_right], [num_down], [num_up], [num_cent]])
    
    return j,a,b
