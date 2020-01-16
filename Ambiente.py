from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np
import random as rd

#import numba

#from timeit import default_timer as timer
#from numba import jit, cuda


def obtenerCampo(resolucion=100):
    return np.zeros((resolucion,resolucion,resolucion),dtype=int)



def insertarObstaculos(array3d,cantidad="MEDIO"):
    x,y,z=array3d.shape
    factor=10000
    if cantidad == "SATURADO":
        factor=1000
    elif cantidad == "SOBRESATURADO":
        factor=500

    nElementos=array3d.size//factor

    for i in range(nElementos):
        a=rd.randint(0,x-1)
        b=rd.randint(0,y-1)
        c=rd.randint(0,z-1)
        array3d[a][b][c]=1

def insertarObstaculosCumulos(array3d,cantidad="MEDIO"):
    x,y,z=array3d.shape
    factor=25
    if cantidad == "SATURADO":
        factor=50
    elif cantidad == "SOBRESATURADO":
        factor=750

    for i in range(factor):
        a = rd.randint(0, x - 1)
        b = rd.randint(0, y - 1)
        c = rd.randint(0, z - 1)
        crearCumulo(array3d,a,b,c)

def crearCumulo(array3d,x,y,z):
    factor=rd.randint(3,9)
    crecer(array3d,x,y,z,factor)

def crecer(array3d,x,y,z,valorCrecer):
    array3d[x][y][z]=1
    if valorCrecer>0:
        listaVecinos=buscarVecinos(array3d,[x,y,z])
        rd.shuffle(listaVecinos)
        for vecino in listaVecinos:
            valorCrecer = valorCrecer - 1
            crecer(array3d,vecino[0],vecino[1],vecino[2],valorCrecer)

def buscarVecinos2(campo3D, punto):

    limitX, limitY, limitZ = campo3D.shape
    lista = []

    posZ = punto[2] -1
    for z in range(3):

        posX = punto[0] - 1
        for x in range(3):

            posY = punto[1] - 1
            for y in range(3):

                excesoX = 0 <= x < limitX
                excesoY = 0 <= y < limitY
                excesoZ = 0 <= z < limitZ
                noIgual = posX != punto[0] or posY != punto[1] or posZ != punto[2]
                if excesoX and excesoY and excesoZ and noIgual:
                    puntoNuevo = [posX, posY, posZ]
                    lista.append(puntoNuevo)
                posY += 1
            posX += 1
        posZ += 1
    return lista

def buscarVecinos(array3D,punto):
    vecinos=[]
    X,Y,Z=array3D.shape

    for i in range(len(punto)):
        puntoMas=punto.copy()
        puntoMenos =punto.copy()
        puntoMas[i]=punto[i]+1
        puntoMenos[i]=punto[i]-1

        x, y, z = puntoMas
        x1, y1, z1 = puntoMenos
        if 0<x < X and 0<y<Y and 0<z <Z:
            vecinos.append(tuple(puntoMas))
        if 0 < x1 < X and 0 < y1 < Y and 0 < z1 < Z:
            vecinos.append(tuple(puntoMenos))
    return vecinos




def agregarCuboAMatriz(array3d,puntosCubo):
    xs,ys,zs=puntosCubo
    longitudPuntos=len(puntosCubo[0])
    for i in range(longitudPuntos):
        array3d[xs[i],ys[i],zs[i]]=1

def agregarPuntosAPlot(puntosCubo,subplot):#puntos debe ser [[xq,x2,x3...],[y1,y2,y3,...],[z1,z2,z3....]]
    xs,ys,zs=puntosCubo
    subplot.scatter(xs, ys, zs, marker='o')




def insertarObstaculosCubosMatrix(array3d,diccionarioCubos):
    for tuplaPunto,puntosCubo in diccionarioCubos.items():
        agregarCuboAMatriz(array3d,puntosCubo)

def insertarObstaculosCubosPlot(diccionarioCubos,subplot):
    for tuplaPunto,puntosCubo in diccionarioCubos.items():
        agregarPuntosAPlot(puntosCubo,subplot)


def obtenerDiccionarioCubos(puntosCubos,arista=7):#{(xo1,yo1,zo1):[xs,ys,zs]}
    dicCubos={}#{(xo1,yo1,zo1):[[x1,y2,z3]...],(xo2,yo2,zo2):[[x]]}
    for tuplaPunto in puntosCubos:
        a,b,c=tuplaPunto
        puntosCubo=obtenerPuntosSuperficieCubo(a,b,c,arista)
        dicCubos[tuplaPunto]=puntosCubo
    return dicCubos


#######metodo de generacion de puntos origen#####

def obtenerPuntosOrigenCubo(array3d, N, arista):
    X, Y, Z = array3d.shape

    puntosOrigen = []
    array3dCopy=np.copy(array3d)
    while (N > 0):

        x=rd.randint(0, X-arista-1)
        y=rd.randint(0, Y-arista-1)
        z=rd.randint(0, Z-arista-1)

        """validos = np.where((array3dCopy != 1))
        i = rd.randint(0, len(validos[0]))

        x = validos[0][i]
        y = validos[1][i]
        z = validos[2][i]"""

        if dentroDeRango(array3dCopy,x,y,z,arista) and sinIntercepciones(array3dCopy,x,y,z,arista):
            puntosOrigen.append((x,y,z))
            puntosCubo = obtenerPuntosSolidoCubo(x, y, z, arista)
            agregarCuboAMatriz(array3dCopy, puntosCubo)
            N-=1

    return puntosOrigen#[(a,b,c),(a,b,c)....]


####fin metodo de generacion de puntos origen###

#############metodos de generacion de puntos#####

def obtenerPuntosSuperficieCubo(x,y,z,arista):
    xs=[]
    ys=[]
    zs=[]

    for i in range(x, x + arista):
        for j in range(y, y + arista):
            xs.append(i)
            ys.append(j)
            zs.append(z)
            xs.append(i)
            ys.append(j)
            zs.append(z+arista)

    for i in range(x, x + arista):
        for k in range(z, z + arista):
            xs.append(i)
            ys.append(y)
            zs.append(k)
            xs.append(i)
            ys.append(y+arista)
            zs.append(k)

    for j in range(y, y + arista):
        for k in range(z, z + arista):
            xs.append(x)
            ys.append(j)
            zs.append(k)
            xs.append(x+arista)
            ys.append(j)
            zs.append(k)
    return [xs,ys,zs]

def obtenerPuntosSolidoCubo(x,y,z,arista):
    xs=[]
    ys=[]
    zs=[]
    for i in range(x, x + arista):
        for j in range(y, y + arista):
            for k in range(z, z + arista):
                xs.append(i)
                ys.append(j)
                zs.append(k)
    return [xs,ys,zs]

#############fin metodos de creacion#########


#############metodos de validacion##########
def sinIntercepciones(array3d,x,y,z,arista):

    return array3d[x,y,z]!=1 and  array3d[x+arista,y+arista,z+arista]!=1 \
           and array3d[x + arista, y + arista, z ] != 1 and array3d[x+arista,y,z+arista]!=1 \
           and array3d[x,y+arista,z+arista]!=1 and array3d[x,y,z+arista]!=1 \
           and array3d[x,y+arista,z]!=1 and array3d[x+arista,y,z]!=1

def dentroDeRango(array3d,x,y,z,arista):
    X, Y, Z = array3d.shape
    return 0<x + arista < X and 0<y + arista < Y and 0<z + arista < Z

#############fin metodos de validacion#######



def productoPunto(pI, pD):

    result = 0
    ind = 0
    while ind < 3:
        result += pI[ind]*pD[ind]
        ind+=1

    return result

def vectorizar(puntoAnterio, puntoActual, puntoPrueba):

    arrAnt = np.array(puntoAnterio)
    arrAct = np.array(puntoActual)
    arrPrue = np.array(puntoPrueba)

    return [arrAct-arrAnt, arrPrue-arrAct]

def calcularDistancia(puntoInicio:list, puntoDestino:list):

    result:float = 0.0
    for ind in range(3):
        result += (puntoInicio[ind]-puntoDestino[ind])**2

    return result

def calcularRuta(campo3D, puntoInicio:list, puntoFin:list):

    puntoAnt:list = puntoInicio
    puntoActual:list = puntoInicio

    ruta:list = []
    veces = 0
    while puntoActual != puntoFin:

        ruta.append(puntoActual)
        puntosVecinos: list = buscarVecinos2(campo3D, puntoActual)

        listaPuntos = list()

        for puntoPrueba in puntosVecinos:

            vectores: list = vectorizar(puntoAnt, puntoActual, puntoPrueba)
            pUno: list = vectores[0]
            pDos: list = vectores[1]
            avance: bool = productoPunto(pUno, pDos) >= 0
            disponble: bool = campo3D[puntoPrueba[0], puntoPrueba[1], puntoPrueba[2]] == 0
            if avance and disponble:

                    distancia = calcularDistancia(puntoPrueba, puntoFin)
                    tupla: tuple = (distancia, puntoPrueba)
                    if tupla not in listaPuntos: listaPuntos.append(tupla)

        listaPuntos.sort(reverse=True)
        puntoMasCercano: list = list(listaPuntos.pop()[1])

        puntoAnt = puntoActual
        puntoActual = puntoMasCercano
        veces+=1
    ruta.append(tuple(puntoFin))
    return ruta



