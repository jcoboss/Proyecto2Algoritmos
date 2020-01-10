from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np
import random as rd

resolucion=100

def obtenerCampo():
    return np.zeros((resolucion,resolucion,resolucion),dtype=int)

def mostrarCampo(campo3D,colorObstaculos):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    puntos=np.where((campo3D==1))
    x = puntos[0]
    y = puntos[1]
    z = puntos[2]

    ax.scatter(x, y, z, c=colorObstaculos, marker='o')

    ax.set_xlabel('X Label')
    ax.set_ylabel('Y Label')
    ax.set_zlabel('Z Label')

    plt.show()

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
        factor=100

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
                excesoY = 0 <= x < limitX
                excesoZ = 0 <= z < limitZ
                noIgual = posX != punto[0] and posY != punto[1] and posZ != punto[2]
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

def insertarObstaculosCubos(array3d,cantidad="MEDIO"):
    x,y,z=array3d.shape
    factor=12
    if cantidad == "SATURADO":
        factor=25
    elif cantidad == "SOBRESATURADO":
        factor=50

    for i in range(factor):
        a = rd.randint(0, x - 1)
        b = rd.randint(0, y - 1)
        c = rd.randint(0, z - 1)
        crearCubo(array3d,a,b,c)

def crearCubo(array3d,x,y,z):
    factor = rd.randint(5, 15)
    crecerCubo(array3d,x,y,z,factor)

def crecerCubo(array3d,x,y,z,valorCrecer):

    X,Y,Z=array3d.shape
    if x+valorCrecer<X and y+valorCrecer<Y and z+valorCrecer<Z :
        for i in range(x,x+valorCrecer):
            for j in range(y,y+valorCrecer):
                array3d[i][j][z] = 1
                array3d[i][j][z+valorCrecer] = 1

        for i in range(x,x+valorCrecer):
            for k in range(z,z+valorCrecer):
                array3d[i][y][k] = 1
                array3d[i][y+valorCrecer][k] = 1

        for j in range(y,y+valorCrecer):
            for k in range(z,z+valorCrecer):
                array3d[x][j][k] = 1
                array3d[x+valorCrecer][j][k] = 1

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
    while puntoActual != puntoFin:

        ruta.append(puntoActual)
        puntosVecinos: list = buscarVecinos2(campo3D, puntoActual)

        listaPuntos = list()
        print("Ruta pracial -> " +str(ruta))
        print("Vecinos", str(puntosVecinos))

        for puntoPrueba in puntosVecinos:

            if puntoPrueba != puntoFin:
                vectores: list = vectorizar(puntoAnt, puntoActual, puntoPrueba)
                pUno: list = vectores[0]
                pDos: list = vectores[1]
                avance: bool = productoPunto(pUno, pDos) >= 0
                disponble: bool = campo3D[puntoPrueba[0], puntoPrueba[1], puntoPrueba[2]] == 0
                if avance and disponble:
                    print("Agregue -> " + str(puntoPrueba))
                    distancia = calcularDistancia(puntoPrueba, puntoFin)
                    tupla: tuple = (distancia, puntoPrueba)
                    if tupla not in listaPuntos: listaPuntos.append(tupla)
            else:
                listaPuntos.append(tuple(0,puntoFin))

        listaPuntos.sort(key=lambda tup: tup[0], reverse=True)
        print("Tuplas -> " + str(listaPuntos))
        print("Ordene")
        puntoMasCercano: list = list(listaPuntos.pop()[1])

        if puntoMasCercano == puntoFin:
            ruta.append(puntoFin)
            break
        else:
            puntoAnt = puntoActual
            puntoActual = puntoMasCercano

    return ruta


campo=obtenerCampo()
#insertarObstaculos(campo,"SATURADO")
#mostrarCampo(campo,"r")
#campo=obtenerCampo()
#insertarObstaculosCumulos(campo,"SATURADO")
#mostrarCampo(campo,"g")
#campo=obtenerCampo()
insertarObstaculosCubos(campo,"SATURADO")
mostrarCampo(campo,"b")

#ruta = calcularRuta(campo, [1,1,1], [5,5,4])
#print(ruta)



