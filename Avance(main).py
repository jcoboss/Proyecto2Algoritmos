from Ambiente import *
from time import time
#----------AVANCE-----------

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')


campo=obtenerCampo(100) #matriz de 100x100x100
puntosCubos=obtenerPuntosOrigenCubo(campo,N=100,arista=7)
diccionarioCubos=obtenerDiccionarioCubos(puntosCubos,arista=7)

insertarObstaculosCubosMatrix(campo,diccionarioCubos)
insertarObstaculosCubosPlot(diccionarioCubos,ax) #se insertan 100 cubos con arista 7


ax.set_xlabel('X Label')
ax.set_ylabel('Y Label')
ax.set_zlabel('Z Label')

plt.show()


#-----------------------------