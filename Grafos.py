import numpy as np
import itertools as it
import math as mt
from time import time
from queue import PriorityQueue

import random as rd

def crearGrafo(matriz):
    X,Y=matriz.shape
    grafo={}
    for i in range(X):
        for j in range(Y):
            if matriz[i,j]==0:
                vecinos=obtenerVecinosPunto2D(matriz,(i,j))
                sub=grafo.get((i,j),[])
                sub.extend(vecinos)
                grafo[(i,j)]=sub
    return grafo

def distancia2Puntos2D(punto1,punto2):
    return (mt.pow(punto2[1]-punto1[1],2)+mt.pow(punto2[0]-punto1[0],2))

def obtenerVecinosPunto2D(matriz,punto):
    vecinos=[]
    X,Y=matriz.shape
    x,y=punto
    for i in range(-1,2):
        for j in range(-1,2):
            sX = i + x
            sY = j + y
            if sX!=x or sY!=y:
                if 0 <= sX < X and 0 <= sY < Y:
                    if matriz[sX, sY] == 0:  # me desago del mismo punto como vecino
                        vecinos.append((sX,sY))
                        #matriz[sX, sY] = 2
                        #print(i, j)
    return vecinos

def encontrarRutaMasCorta(punto1,punto2,grafo):
    ruta=[]
    ruta.append(punto1)
    operaciones={}
    i=1
    while punto1!=punto2:

        adyacentes = grafo[punto1]
        minVal = 10000000000#la longitud del grafo siempre va a ser mas grande que cualquier distancia
        minPunto = adyacentes[0]
        for adyacente in adyacentes:
            #print("Nueva operacion # {}".format(i))
            i += 1
            distancia = distancia2Puntos2D(adyacente, punto2)
            if distancia < minVal:
                minPunto = adyacente
                minVal = distancia
        ruta.append(minPunto)
        punto1=minPunto
    return ruta


def agregarPuntosRutaAMatrix(matriz,ruta):
    for tupla in ruta:
        i,j=tupla
        matriz[i,j]=1

def agregarObstaculoAMatrix(matriz):
    veces=np.size(matriz)//2
    X,Y =matriz.shape
    while veces>0:
        i=rd.randint(0,X-1)
        j=rd.randint(0,Y-1)
        matriz[i,j]=2
        veces-=1

