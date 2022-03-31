#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 24 17:24:05 2022

@author: ayoub
"""

from code import getCoeff
import numpy as np
#
#cd.getCoeff(1,8,2,5,5,2,9)

def Laplace(matrix_num, matrix_dom, matrix_condition):
    noeuds = np.loadtxt(matrix_num)
    Limite = np.loadtxt(matrix_dom)
    condition = np.loadtxt(matrix_condition)
    dim = np.shape(noeuds)
    data = np.array([])
    rang = np.array([])
    col = np.array([])
    BB = np.array([])
    for x in range(dim[0]): # x = i
        for y in range(dim[1]): # y = j
#            type_cent = 1
            if x==0 or y==0 or x == dim[0]-1 or y == dim[1]-1 or noeuds[x][y] == 0:
                continue
  
#            if noeuds[x][y] != 0:
#                if noeuds[x][y-1] ==0 or  noeuds[x][y+1]== 0 or noeuds[x-1][y]== 0 or noeuds[x+1][y]== 0:
#                    type_cent = 2

            
            j,a,b = getCoeff(noeuds[x][y-1], noeuds[x][y+1], noeuds[x-1][y], noeuds[x+1][y], noeuds[x][y], Limite[x][y], condition[x][y])
            np.concatenate((data, a))
            np.concatenate((col, j))
            np.concatenate((rang, np.array([noeuds[x][y], noeuds[x][y], noeuds[x][y], noeuds[x][y], noeuds[x][y]])))
            np.concatenate((BB, b))
            
    return data, rang, col, BB
Laplace("CL/1-num.txt", "CL/1-dom.txt", "CL/1-cl.txt")
