import trimesh as t,numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
fig=plt.figure(figsize=(14,6),facecolor='#f3f5f7')
A=t.load('outputs/A_hex_carrier.stl');B=t.load('outputs/B_arm_5deg_up.stl');scene=t.load('work/assembly.glb')
def draw(ax,meshes,colors,title,lim,elev=35,azim=-55):
 triangles=[];facecolors=[]
 for m,color in zip(meshes,colors):
  normals=m.face_normals; light=np.array([.4,-.4,.8]); shade=np.clip(normals@light,0,1)*.45+.5
  from matplotlib.colors import to_rgb
  rgba=np.c_[np.array(to_rgb(color))[None,:]*shade[:,None],np.ones(len(shade))]
  triangles.extend(m.triangles);facecolors.extend(rgba)
 ax.add_collection3d(Poly3DCollection(triangles,facecolors=facecolors,edgecolor='none'))
 ax.set(xlim=lim[0],ylim=lim[1],zlim=lim[2]);ax.set_box_aspect([b-a for a,b in lim]);ax.view_init(elev,azim);ax.set_axis_off();ax.set_title(title,fontsize=13,pad=8)
draw(fig.add_subplot(131,projection='3d'),[A],['#319aa1'],'A · Original hex connections\nReinforced centre + two wall fixings',[(-110,110),(-100,100),(0,80)])
draw(fig.add_subplot(132,projection='3d'),[B],['#d88b36'],'B · Bolted, ribbed arm\n5° upward · 7.8 mm peg × 19 mm',[(-45,45),(-45,45),(0,85)])
ms=[]
for node in scene.graph.nodes_geometry:
 transform,name=scene.graph[node]; m=scene.geometry[name].copy();m.apply_transform(transform);ms.append(m)
draw(fig.add_subplot(133,projection='3d'),ms,[('#bcc6d1' if max(m.extents[:2])>240 else '#319aa1' if max(m.extents[:2])>100 else '#d88b36') for m in ms],'Assembly · Existing base between A and B\nBase shown with original arm removed',[(-140,140),(-120,155),(0,105)],45,-60)
fig.suptitle('Sovereign wall mount — first printable prototypes',fontsize=20,y=.97)
fig.text(.5,.045,'Peg leans 5° toward the upper wall fixing. Glue fixes the chosen ship orientation. Prototype: not load-tested.',ha='center',fontsize=11,color='#8b442c')
plt.subplots_adjust(left=.01,right=.99,bottom=.1,top=.82,wspace=.03);plt.savefig('outputs/design_preview.png',dpi=170,facecolor=fig.get_facecolor())
