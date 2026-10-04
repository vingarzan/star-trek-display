import trimesh, numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
paths=['source_models/obj_1_Inclined display.stl','source_models/obj_2_Inclined display with nail.stl','source_models/xxx_-_stand_sovereign_d.stl']
fig=plt.figure(figsize=(15,12))
for i,p in enumerate(paths):
 m=trimesh.load(p); print(p,m.bounds,m.extents,'watertight',m.is_watertight)
 parts=m.split(only_watertight=False); print('components',[(len(s.faces),s.bounds.tolist()) for s in parts if len(s.faces)>20])
 for j,(e,a) in enumerate([(90,-90),(0,-90),(25,-55)]):
  ax=fig.add_subplot(3,3,i*3+j+1,projection='3d'); ax.add_collection3d(Poly3DCollection(m.triangles,facecolor='#8ebaca',edgecolor='none',alpha=1))
  c=m.bounds.mean(axis=0); r=max(m.extents)/2
  ax.set(xlim=(c[0]-r,c[0]+r),ylim=(c[1]-r,c[1]+r),zlim=(c[2]-r,c[2]+r),xlabel='X',ylabel='Y',zlabel='Z'); ax.view_init(e,a); ax.set_title(['Hex','Nail hex','Sovereign'][i]); ax.set_box_aspect((1,1,1))
plt.tight_layout(); plt.savefig('work/source_views.png',dpi=130)
