"""Lighter corner-braced alternative retaining only the upward socket."""
from pathlib import Path
import json,numpy as np,trimesh as t
from scipy.spatial import ConvexHull,HalfspaceIntersection
from scipy.optimize import linprog
from render import draw,plt
R=Path(__file__).resolve().parents[1];out=R/'outputs'
def box(s,c):
 m=t.creation.box(s);m.apply_translation(c);return m
def hexagon(r,z0,z1):return t.convex.convex_hull(np.array([[r*np.cos(a),r*np.sin(a),z] for a in np.arange(6)*np.pi/3 for z in [z0,z1]]))
def union(ms):return t.boolean.union(ms,engine='manifold')
def inter(a,b):return t.boolean.intersection([a,b],engine='manifold')
def diff(a,b):return t.boolean.difference([a,b],engine='manifold')
def rounded(mesh,r):
 planes=np.unique(np.round(ConvexHull(mesh.vertices).equations,10),axis=0);planes[:,-1]+=r
 sol=linprog([0,0,0,-1],A_ub=np.c_[planes[:,:3],np.linalg.norm(planes[:,:3],axis=1)],b_ub=-planes[:,3],bounds=[(None,None)]*4,method='highs')
 core=HalfspaceIntersection(planes,sol.x[:3]).intersections;sphere=t.creation.icosphere(subdivisions=3,radius=r).vertices
 return t.convex.convex_hull((core[:,None,:]+sphere[None,:,:]).reshape(-1,3))
old=t.load(out/'hex_ship_corner_braced_arm.stl')
frame=t.load(out/'hex_open_original_size.stl')
# Extract only the arm and a 0.01 mm overlap; exclude old base/braces below it later.
arm=inter(old,box([100,110,139.01],[0,0,77.495])) # Z=7.99..147
# Split at the socket region so all socket geometry remains exactly positioned.
low=inter(arm,box([100,110,118.01],[0,0,66.995])) # Z=7.99..126
high=inter(arm,box([100,110,21],[0,0,136.5]))
v=low.vertices.copy();f=np.clip((v[:,2]-8)/118,0,1);v[:,0]*=.8+.2*f
v[:,1]=np.where(v[:,1]<0,v[:,1]*(.78+.22*f),v[:,1]);low.vertices=v
arm=union([low,high])
# Round the new tip without changing the socket walls below Z=144.
cap=rounded(box([28,28,10],[0,0,142]),3)
arm=union([inter(arm,box([120,120,136.01],[0,0,75.995])),inter(arm,cap)])
# Narrow only material outside the 10.4 mm socket envelope. Its internal
# walls and the pin bore's Y-Z profile remain unchanged.
v=arm.vertices.copy();x=v[:,0];v[:,0]=np.sign(x)*np.where(np.abs(x)<=5.2,np.abs(x),5.2+(np.abs(x)-5.2)*(4.8/8.8));arm.vertices=v
root=hexagon(38,0,8)
arm=diff(arm,diff(box([120,120,8],[0,0,4]),root))
ribs=[]
for angle in [0,60,120]:
 m=box([220,12,8],[0,0,4]);m.apply_transform(t.transformations.rotation_matrix(np.deg2rad(angle),[0,0,1]));ribs.append(m)
ribs=inter(union(ribs),hexagon(100,0,8));model=union([frame,root,ribs,arm])
p=out/'hex_ship_corner_braced_light_arm.stl';model.export(p);model=t.load(p)
f=model.faces;model.update_faces((f[:,0]!=f[:,1])&(f[:,1]!=f[:,2])&(f[:,0]!=f[:,2]));model.update_faces(model.unique_faces());model.remove_unreferenced_vertices();model.export(p);model=t.load(p)
assert model.is_volume and len(model.split())==1
foot=inter(arm,box([100,100,.01],[0,0,8.005]));unsupported=abs(diff(foot,hexagon(38,7.9,8.1)).volume);assert unsupported<.01
checks={}
for diameter in [6,8]:
 peg=t.load(out/f'peg_insert_{diameter}mm.stl');peg.apply_transform(t.transformations.rotation_matrix(-np.pi/2,[1,0,0]));peg.apply_translation([0,1.95,138])
 for lift in [0,.15,1,4,8,13]:
  q=peg.copy();q.apply_translation([0,lift,0]);v=float(abs(inter(model,q).volume));checks[f'peg_{diameter}mm_lift_{lift}_overlap_mm3']=v;assert v<.01
socket_region=box([10.4,12.2,10.4],[0,7.9,138]) # Exact cavity from its floor at Y=1.8 to mouth at Y=14.
a=inter(model,socket_region);b=inter(old,socket_region)
err=float(abs(a.volume)+abs(b.volume));assert err<.01
checks['socket_cavity_obstruction_mm3']=err
checks['unsupported_footprint_mm3']=float(unsupported)
# Optional retaining pin remains a clear 3.4 mm bore through the narrower housing.
pin=t.creation.cylinder(radius=1.695,height=30,sections=96);pin.apply_transform(t.geometry.align_vectors([0,0,1],[1,0,0]));pin.apply_translation([0,8.2,138])
checks['pin_bore_obstruction_mm3']=float(abs(inter(model,pin).volume));assert checks['pin_bore_obstruction_mm3']<.01
report=json.loads((out/'geometry_checks.json').read_text());report['hex_ship_corner_braced_light_arm']=dict(dimensions_mm=model.extents.tolist(),volume_cm3=float(model.volume/1000),watertight=True,components=1,export_reload_verified=True,central_hex_width_mm=76,central_hex_height_mm=float(76*np.cos(np.pi/6)),arm_width_at_base_mm=float(2*(5.2+(11.2-5.2)*(4.8/8.8))),socket_housing_width_mm=20,tip_height_from_wall_mm=147,upward_socket_axis_from_wall_mm=138,outward_socket=False,volume_reduction_percent=float(100*(1-model.volume/old.volume)),checks=checks)
(out/'geometry_checks.json').write_text(json.dumps(report,indent=2)+'\n')
fig=plt.figure(figsize=(14,7),facecolor='#f3f5f7')
draw(fig.add_subplot(121,projection='3d'),[model],['#688ca5'],'Lighter corner-braced arm — front',[(-112,112),(-100,100),(0,170)],90,-90)
draw(fig.add_subplot(122,projection='3d'),[model],['#688ca5'],'Single upward socket · smaller centred base',[(-112,112),(-100,100),(0,170)],30,55)
fig.tight_layout();fig.savefig(out/'light_arm_preview.png',dpi=150,bbox_inches='tight')
print(json.dumps(report['hex_ship_corner_braced_light_arm'],indent=2))
