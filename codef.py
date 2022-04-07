import numpy
def submit(which):
    dom = numpy.loadtxt(which+ '-dom.txt', dtype = int)
    num = numpy.loadtxt(which+ '-num.txt', dtype = int)
    cl = numpy.loadtxt(which+ '-cl.txt', dtype = float) # Les conditions limites sont imposées et ne doivent donc pas être déterminée
    if which == '1':
        dx = 0.5
    else:
        dx = 0.01
    psi = Laplace(dom,num,cl) #Exemple d'appel à la fonction Laplace
    u,v = velocity(dom,psi,dx,dx) #Exemple d'appel à la fonction velocity
    return psi,u,v
    
import numpy as np
from scipy.sparse import csc_matrix
from scipy.sparse.linalg import spsolve

def getCoeff(num_left,num_right,num_down,num_up,num_cent,type_cent,cl_cent):
    if type_cent == 0:
        return 0
    
    if type_cent == 2:
        a = np.array([[1]])
        j = np.array([[num_cent]])
        b = np.array([[cl_cent]])
        return j, a, b
       
    if type_cent == 1:
        a = np.array([[1],[1],[1],[1],[-4]])
        b = np.array([[0]])
        j = np.array([[num_left], [num_right], [num_down], [num_up], [num_cent]])
        return j, a, b
        
    return 0
    
def deriv(f_left, f_c, f_right, type_left, type_c, type_right, h):
    if type_left != 0 and type_right != 0:
        v = (f_right - f_left)/(2*h) 
        return v
    
    if type_left != 0 and type_right == 0:
        v = (f_c - f_left)/(h)
        return v
  
    if type_left == 0 and type_right != 0:
        v = (f_right - f_c)/(h)
        return v
    v = 0
    return v
def velocity(dom, psi, dx, dy):
    
  #  dom = np.rot90(dom)
    dimension = np.shape(dom)
#    if np.shape(psi) != dimension:
 #       print("error")
    u,v = np.zeros(shape = (dimension[0], dimension[1])), np.zeros(shape = (dimension[0], dimension[1]))
    
    for i in range(dimension[0]-1):
        for j in range(dimension[1]-1): 
            if dom[i][j]==0 or j==0 or i==0:
                continue
            v[i][j] =  -deriv(psi[i-1][j],psi[i][j],psi[i+1][j],dom[i-1][j],dom[i][j],dom[i+1][j],dx)
            u[i][j] = deriv(psi[i][j-1],psi[i][j],psi[i][j+1],dom[i][j-1],dom[i][j],dom[i][j+1],dx)
    return u,v
def Laplace(Limite, noeuds , condition):
    
    #noeuds = np.loadtxt(matrix_num, dtype=int)
    #Limite = np.loadtxt(matrix_dom)
    #condition = np.loadtxt(matrix_condition)
    dim = np.shape(noeuds)
    data = np.array([[0]])
    rang = np.array([[0]])
    col = np.array([[0]])
    BB = np.array([[0]])
    rangB = np.array([0])
    
    for x in range(dim[0]-1): # x = i
        for y in range(dim[1]-1): # y = j

            if x==0 or y==0 or getCoeff(noeuds[x-1][y], noeuds[x+1][y], noeuds[x][y+1], noeuds[x][y-1], noeuds[x][y], Limite[x][y], condition[x][y]) == 0:
                continue
            

            j,a,b = getCoeff(noeuds[x-1][y], noeuds[x+1][y], noeuds[x][y+1], noeuds[x][y-1], noeuds[x][y], Limite[x][y], condition[x][y])
            
            data = np.concatenate((data, a))
            col = np.concatenate((col, j-1))
            BB = np.concatenate((BB, b))
            rangB = np.concatenate((rangB, [noeuds[x][y]]))
            """
            data.extend(a)
            col.extend(j-1)
            B.append(b)
            rangB.extend(noeuds[x][y])"""
            
            if Limite[x][y] == 2:
                rang = np.concatenate((rang, np.array([[noeuds[x][y]]]) ))
            if Limite[x][y] == 1:
                rang= np.concatenate((rang, np.array([[noeuds[x][y]],[noeuds[x][y]],[noeuds[x][y]],[noeuds[x][y]],[noeuds[x][y]]])))


#initialiser les vecteur por le sparce matrice (transposer)

    theB = BB[1:].T[0]

    
    datata = data[1:].T[0]
    rangA = (rang[1:]-1).T[0]
    colA  = col[1:].T[0]
    rangB1 = (rangB[1:]-1)

#finding sparce A
    SparceA = csc_matrix((datata, (rangA,colA)))

    SparceB = csc_matrix((theB, (rangB1, np.zeros_like(rangB1))))

    solution_vect = spsolve(SparceA,SparceB)
    
    
    
    matrice = np.zeros((dim[0], dim[1]))
    for x in range(dim[0]-1): # x = i
        for y in range(dim[1]-1): # y = j
            if noeuds[x][y] != 0:
                matrice[x][y] = solution_vect[noeuds[x][y]-1]
         
#    solution_mat = np.rot90(matrice)
    return matrice