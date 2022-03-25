#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 24 17:24:05 2022

@author: ayoub
"""

from code import getCoeff 
import numpy as np
#
#cd.getCoeff(1,8,2,5,5,5,9)

def Laplace(filename):
    noeuds = np.loadtxt(filename)
    dim = np.shape(noeuds)
    data = []
    rang = []
    col = []
    BB = []
    for x in range(dim[0]): # x = i
        for y in range(dim[1]): # y = j
            j, a, b = getCoeff(noeuds[x][y-1], noeuds[x][y+1], noeuds[x-1][y], noeuds[x+1][y], noeuds[x][y], 2)
            np.append(data, a)
            np.append(col, j)
            np.append(rang, [noeuds[x][y], noeuds[x][y], noeuds[x][y], noeuds[x][y], noeuds[x][y]])
            np.append(BB, b)
            
    return data, rang, col, BB

