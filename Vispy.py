import numpy as np

l = [2,6,5]
ll = np.array(l)
l2 = [5,8,9]
ll2 = np.array(l2)

print(ll-ll2)

c = scene.SceneCanvas(keys='interactive', show=True)
def mostrarCampoGPU(campo3D, colorObtaculo):

    view = c.central_widget.add_view()
    view.camera = 'fly'
    view.camera.depth = 10

    pos = np.array([(0, 0, 0), (2, 1, 1), (1,2,6)])
    s = scene.Markers(pos=pos, parent=view.scene)
    s.interactive = True
    c.app.run()

@c.connect
def on_mouse_press(event):
   vs.view.interactive = False
   print(c.visual_at(event.pos))
   vs.view.interactive = True