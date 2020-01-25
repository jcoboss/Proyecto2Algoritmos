from queue import *
from M3DtoGraph import *

def obtenerDiccionarioDijktra(grafo,nodoInicial,nodoDestino,dimension=2):
    #clear node
    dijktra={}
    for punto,adyacentes in grafo.items():
        sub=dijktra.get(punto,{})
        sub["ancestro"]=None
        sub["distancia"]=float('inf')
        sub["visto"]=False
        dijktra[punto]=sub
    #end clear node

    cola=PriorityQueue()
    dijktra[nodoInicial]["distancia"]=0
    cola.put_nowait((0,nodoInicial))
    punto=(-1,-1)#nodo inicial arbitrario
    while not cola.empty() and nodoDestino!=punto:
        tupla=cola.get_nowait()
        distancia=tupla[0]
        punto = tupla[1]
        #print("punto {} sale de la cola".format(punto))
        dijktra[punto]["visto"]=True
        for adyacente in grafo[punto]:
            if not dijktra[adyacente]["visto"]:
                nDistancia=distancia2Puntos3D(adyacente,nodoDestino,dimension)
                if dijktra[adyacente]["distancia"]> nDistancia:
                    dijktra[adyacente]["distancia"]=nDistancia
                    dijktra[adyacente]["ancestro"]=punto
                    cola.put_nowait((nDistancia,adyacente))
    return dijktra

def enrutarDijktra(grafoDijktra, nodoDestino):
    ruta=[]

    ruta.append(nodoDestino)
    ancestro=grafoDijktra[nodoDestino]["ancestro"]
    while ancestro!=None:
        ruta.append(ancestro)
        ancestro=grafoDijktra[ancestro]['ancestro']
    return ruta

def obtenerRutaAStar(grafo,nodoInicial,nodoDestino,dimesion):
    grafoD=obtenerDiccionarioDijktra(grafo,nodoInicial,nodoDestino,dimesion)
    return enrutarDijktra(grafoD,nodoDestino)
