from Ambiente import *

#----------AVANCE-----------

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')


matriz=obtenerCampo(100) #matriz de 100x100x100
insertarObstaculosCubos(matriz,ax,100,7) #se insertan 100 cubos con arista 7



ax.set_xlabel('X Label')
ax.set_ylabel('Y Label')
ax.set_zlabel('Z Label')

plt.show()


#-----------------------------