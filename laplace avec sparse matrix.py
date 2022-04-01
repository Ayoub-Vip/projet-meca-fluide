#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 24 17:24:05 2022

@author: ayoub
"""

import numpy as np
from scipy.sparse import csc_matrix
from scipy.sparse.linalg import spsolve


#cd.getCoeff(1,8,2,5,5,2,9)
def getCoeff(num_left,num_right,num_down,num_up,num_cent,type_cent,cl_cent):
    if type_cent == 0:
        return 0
    
    if type_cent == 2:
        a = np.array([[1]])
        j = np.array([[num_cent]])
        b = np.array([[cl_cent]])
       
    
    if type_cent == 1:
        a = np.array([[1],[1],[1],[1],[-4]])
        b = np.array([[0]])
        j = np.array([[num_left], [num_right], [num_down], [num_up], [num_cent]])
    
    return j,a,b

def Laplace(matrix_num, matrix_dom, matrix_condition):
    
    noeuds = np.loadtxt(matrix_num, dtype=int)
    Limite = np.loadtxt(matrix_dom)
    condition = np.loadtxt(matrix_condition)
    dim = np.shape(noeuds)
    data = np.array([[0]])
    rang = np.array([[0]])
    col = np.array([[0]])
    BB = np.array([[0]])
    rangB = np.array([0])
    
    for x in range(dim[0]-1): # x = i
        for y in range(dim[1]-1): # y = j

            if x==0 or y==0:
                continue

            j,a,b = getCoeff(noeuds[x][y-1], noeuds[x][y+1], noeuds[x-1][y], noeuds[x+1][y],
                             noeuds[x][y], Limite[x][y], condition[x][y])

            data= np.concatenate((data, a))
            col = np.concatenate((col, j-1))
            BB = np.concatenate((BB, b))
            rangB = np.concatenate((rangB, [noeuds[x][y]]))
            
            if Limite[x][y] == 2:
                rang = np.concatenate((rang, np.array([[noeuds[x][y]]]) ))
            if Limite[x][y] == 1:
                rang= np.concatenate((rang, np.array([[noeuds[x][y]],[noeuds[x][y]],[noeuds[x][y]],[noeuds[x][y]],[noeuds[x][y]]])))
            
    return data[1:], rang[1:]-1, col[1:], BB[1:], rangB[1:]-1


data, rang, col, BB, rangB = Laplace("CL/1-num.txt", "CL/1-dom.txt", "CL/1-cl.txt")

#print("data", data,"rang", rang, "\n column is ", col,"\n BB is ",  BB)

#initialiser les vecteur por le sparce matrice (transposer)
theB = BB.T[0]
datata =data.T[0]
rangA = rang.T[0]
colA  = col.T[0]

#finding sparce A
SparceA = csc_matrix((datata, (rangA,colA)))
SparceB = csc_matrix((theB, (rangB, np.zeros_like(rangB))))

solution_fi = spsolve(SparceA, SparceB)
