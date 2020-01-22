import math as mt
import numpy as np
import random as rd
def distancia2Puntos3D(punto1,punto2):
    return (mt.pow(punto2[1]-punto1[1],2)+mt.pow(punto2[0]-punto1[0],2)+mt.pow(punto2[2]-punto1[2],2))


def obtenerVecinosPunto3D(matriz,punto):
    vecinos=[]
    X,Y,Z=matriz.shape
    x,y,z=punto
    for i in range(-1,2):
        for j in range(-1,2):
            for k in range(-1, 2):
                sX = i + x
                sY = j + y
                sZ = k + z
                if sX!=x or sY!=y or sZ!=z:
                    if 0 <= sX < X and 0 <= sY < Y and 0 <= sZ < Z:
                        if matriz[sX, sY, sZ] == 0:  # me desago del mismo punto como vecino
                            vecinos.append((sX,sY,sZ))
    return vecinos

def crearGrafo(matriz):
    X,Y,Z=matriz.shape
    grafo={}
    for i in range(X):
        for j in range(Y):
            for k in range(Z):
                if matriz[i,j,k]==0:
                    vecinos=obtenerVecinosPunto3D(matriz,(i,j,k))
                    sub=grafo.get((i,j,k),[])
                    sub.extend(vecinos)
                    grafo[(i,j,k)]=sub
    return grafo
"""
def agregarPuntosRutaAMatrix(matriz,ruta):
    for tupla in ruta:
        i,j,z=tupla
        matriz[i,j,z]=1
"""
"""
def agregarObstaculoAMatrix(matriz):
    veces=np.size(matriz)//2
    X,Y,Z =matriz.shape
    while veces>0:
        i=rd.randint(0,X-1)
        j=rd.randint(0,Y-1)
        k=rd.randint(0,Z-1)
        matriz[i,j,k]=1
        veces-=1
"""
