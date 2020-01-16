import sys
import numpy as np
import vispy
from vispy import color
from vispy import scene
from vispy.scene import visuals
from vispy.color import ColorArray
from Ambiente import *
from time import time


def traduccirDiccionarioVERDADERO(diccionario: dict):

    lista = []
    colorCubos = []

    for clave, valor in diccionario.items():

        x, y, z = valor
        color = np.random.uniform(0.60, 1.00, 3)
        puntosCubitos = [[x[ind], y[ind], z[ind]] for ind in range((len(x)))]
        for ind in range(len(x)):
            colorCubos.append(color)
        lista.extend(puntosCubitos)

    return [np.array(lista), np.array(colorCubos)]

campo=obtenerCampo(100) #matriz de 100x100x100
puntosCubos=obtenerPuntosOrigenCubo(campo,N=120,arista=14)
diccionarioCubos: dict=obtenerDiccionarioCubos(puntosCubos,arista=7)

insertarObstaculosCubosMatrix(campo,diccionarioCubos)

print(len(diccionarioCubos.keys()))

#x, y, z = np.where((campo==1))
puntosCubitos, colorCubos = traduccirDiccionarioVERDADERO(diccionarioCubos)
puntosRuta=calcularRuta(campo,[20,15,0],[98,98,98])


colorRuta = np.array([[0, 0, 0]] * len(puntosRuta))

#colorCubos = np.zeros([[0.85, 1.0, 0.9]] * len(puntosCubitos))

# stack point clouds and colors
pos = np.vstack((np.array(puntosCubitos), np.array(puntosRuta)))
colors = np.vstack((colorCubos, colorRuta))


#
# Make a canvas and add simple view
#

canvas = scene.SceneCanvas(keys='interactive', show=True, bgcolor='white')
"""
arrow keys, or WASD to move forward, backward, left and right
F and C keys move up and down
The camera auto-rotates to make the bottom point down, manual rolling can be performed using Q and E
"""
view = canvas.central_widget.add_view()
flyCam = scene.cameras.FlyCamera(fov=90)
flyCam.scale_factor = 100000
flyCam.center = (99,99,99)


cam1 = scene.cameras.MagnifyCamera()
cam2= scene.cameras.ArcballCamera(fov=90.0, distance=250)

view.camera = flyCam
scatter = visuals.Markers(parent=view.scene)

scatter.antialias = 1

#scatter.set_data(pos=pos, edge_color=(0.7,0.3,0.4,0.8), face_color=(0.7,0.3,0.4,0.8), size=8)

scatter.set_data(pos=pos, face_color=colors, size=8)

#scatter.set_data(pos=puntosRuta, edge_color=(0.0, 0.0, 0.0, 1.0), face_color=(0.9, 0.9, 0.9, 1.0), size=15)
scatter.set_gl_state(depth_test=True, blend=True, blend_func=('src_alpha', 'one_minus_src_alpha'))

# Add axes
axis = visuals.XYZAxis(parent=view.scene)
#print(vispy.color.get_colormap)

r = ColorArray('red')
#map = vispy.color.Colormap(r)
#newAxis = visuals.ColorBar(parent=view.scene, size=10000, cmap=r, orientation='bottom')

if __name__ == '__main__' and sys.flags.interactive == 0:
    canvas.app.run()
