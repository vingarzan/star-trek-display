import trimesh as t,numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
fig=plt.figure(figsize=(14,6),facecolor='#f3f5f7')
def draw(ax,meshes,colors,title,lim,elev=35,azim=-55):
 triangles=[];facecolors=[]
 for m,color in zip(meshes,colors):
  normals=m.face_normals; light=np.array([.4,-.4,.8]); shade=np.clip(normals@light,0,1)*.45+.5
  from matplotlib.colors import to_rgb
  rgba=np.c_[np.array(to_rgb(color))[None,:]*shade[:,None],np.ones(len(shade))]
  triangles.extend(m.triangles);facecolors.extend(rgba)
 ax.add_collection3d(Poly3DCollection(triangles,facecolors=facecolors,edgecolor='none'))
 ax.set(xlim=lim[0],ylim=lim[1],zlim=lim[2]);ax.set_box_aspect([b-a for a,b in lim]);ax.view_init(elev,azim);ax.set_axis_off();ax.set_title(title,fontsize=13,pad=8)
