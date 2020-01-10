import sys
import numpy as np
from vispy import scene
from vispy.scene import visuals
import vispy
import Ambiente as ab

# create data cloud
campo = ab.obtenerCampo()
ab.insertarObstaculosCubos(campo)


pos = np.zeros((100, 3), dtype=int)
print(pos)
x, y, z = np.where((campo==1))


lista = [[x[ind], y[ind], z[ind]] for ind in range((len(x)))]

pos = np.array(lista)

print(pos)

#
# Make a canvas and add simple view
#

canvas = scene.SceneCanvas(keys='interactive', show=True, bgcolor='w')
"""
arrow keys, or WASD to move forward, backward, left and right
F and C keys move up and down
The camera auto-rotates to make the bottom point down, manual rolling can be performed using Q and E
"""
view = canvas.central_widget.add_view()
flyCam = scene.cameras.FlyCamera(fov=90)
flyCam.scale_factor = 1000000
view.camera = flyCam

scatter = visuals.Markers(parent=view.scene)

scatter.antialias = 1
scatter.set_data(pos=pos, edge_color=(0.0, 0.0, 0.0, 1.0), face_color=(0.6, 0.5, 0.4, 1.0), size=15)
scatter.set_gl_state(depth_test=True, blend=True, blend_func=('src_alpha', 'one_minus_src_alpha'))

# Add axes
axis = visuals.XYZAxis(parent=view.scene)

if __name__ == '__main__' and sys.flags.interactive == 0:
    canvas.app.run()