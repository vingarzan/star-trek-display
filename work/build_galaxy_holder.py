"""Galaxy-specific plaque holder. The measured physical thickness is 4.7 mm."""
from pathlib import Path
import numpy as np,json
import trimesh as t
from render import draw,plt
R=Path(__file__).resolve().parents[1];out=R/'outputs'
def box(s,c):
 m=t.creation.box(s);m.apply_translation(c);return m
def cyl(r,h,c):
 m=t.creation.cylinder(radius=r,height=h,sections=96);m.apply_translation(c);return m
def union(ms):return t.boolean.union(ms,engine='manifold')
def diff(a,b):return t.boolean.difference([a,b],engine='manifold')
def inter(a,b):return t.boolean.intersection([a,b],engine='manifold')
def local(m,angle):
 m.apply_transform(t.transformations.rotation_matrix(np.deg2rad(angle),[0,0,1]));return m
source=t.load(R/'source_models/xxx_-_stand_galaxy_d.stl')
# Use the source base outline below the stand arm; map source X-Z into wall X-Y.
plaque=inter(source,box([300,4,250],[0,2,0]));plaque.vertices=plaque.vertices[:,[2,0,1]]
plaque.vertices[:,2]=8+plaque.vertices[:,2]*4.7/4
frame=t.load(out/'hex_open_original_size.stl')
outline=t.convex.convex_hull(np.array([[105*np.cos(a),105*np.sin(a),z] for a in np.arange(6)*np.pi/3 for z in [-1,25]]))
parts=[frame];seats=[]
for angle in [-90,-150,-30]:
 a=np.deg2rad(angle);n=np.array([np.cos(a),np.sin(a)]);tan=np.array([-n[1],n[0]])
 v=plaque.vertices[:,:2];near=v[np.abs(v@tan)<4.1];edge=float((near@n).max());seat=edge+.15
 # X is the local outward radius and Y the tangential width.
 floor=box([90.5-seat,8,8.9],[ (90.5+seat)/2,0,10.45])
 lip=box([90.5-(edge-2),8,2.4],[(90.5+edge-2)/2,0,14.1])
 clip=inter(local(union([floor,lip]),angle),outline)
 parts.append(clip);seats.append(dict(angle_degrees=angle,plaque_edge_radius_mm=edge,seat_radius_mm=seat))
# M3 keeper shifted along the upper-right border to clear the disc with a 5 mm boss.
angle=30;radius=88.3;a=np.deg2rad(angle);screw=np.array([radius*np.cos(a)-16*np.sin(a),radius*np.sin(a)+16*np.cos(a)])
pilot=cyl(1.3,7,[*screw,4.5])
holder=diff(union(parts),pilot)
keeper_local=union([cyl(2.5,4.9,[radius,0,10.45]),cyl(2.5,2.4,[radius,0,14.1]),box([8,5,2.4],[radius-4,0,14.1]),cyl(2.5,2.4,[radius-8,0,14.1])])
keeper_local=diff(keeper_local,cyl(1.7,12,[radius,0,11]));keeper_local.apply_translation([0,16,0]);keeper=local(keeper_local,angle)
checks={}
for name,m in [('holder',holder),('keeper',keeper)]:
 checks[name+'_plaque_overlap_mm3']=float(abs(inter(m,plaque).volume));assert checks[name+'_plaque_overlap_mm3']<.01
for dy in np.linspace(0,10,21):
 p=plaque.copy();p.apply_translation([0,dy,0]);overlap=float(abs(inter(holder,p).volume));checks['lift_'+str(dy)+'mm_overlap_mm3']=overlap;assert overlap<.01
for dz in [0,1,4,10,20]:
 p=plaque.copy();p.apply_translation([0,10,dz]);overlap=float(abs(inter(holder,p).volume));checks['approach_'+str(dz)+'mm_overlap_mm3']=overlap;assert overlap<.01
added=diff(holder,frame);assert abs(diff(added,outline).volume)<.01
assert abs(diff(keeper,outline).volume)<.01
models={'hex_plaque_galaxy_4.7mm':holder}
kp=keeper.copy();kp.apply_translation([-screw[0],-screw[1],-8]);# Print on the flat cap, with its pillar facing up.
kp.apply_transform(t.transformations.rotation_matrix(np.pi,[1,0,0]));kp.apply_translation([0,0,-kp.bounds[0,2]])
models['plaque_retainer_galaxy_4.7mm']=kp
for name,m in models.items():
 p=out/(name+'.stl');m.export(p);m=t.load(p);f=m.faces;m.update_faces((f[:,0]!=f[:,1])&(f[:,1]!=f[:,2])&(f[:,0]!=f[:,2]));m.update_faces(m.unique_faces());m.remove_unreferenced_vertices();m.export(p);m=t.load(p);assert m.is_volume and len(m.split())==1
 checks[name]=dict(dimensions_mm=m.extents.tolist(),watertight=True,components=1,export_reload_verified=True)
report=json.loads((out/'geometry_checks.json').read_text());report['galaxy_holder']=dict(plate_thickness_mm=4.7,clip_gap_mm=4.9,source_base_outline_thickness_mm=4,source_disc_diameter_mm=173.2112198,clips=seats,retainer_screw='M3 x 12 mm, 2.6 mm printed pilot and 3.4 mm retainer clearance',holder_pilot_diameter_mm=2.6,retainer_hole_diameter_mm=3.4,checks=checks)
(out/'geometry_checks.json').write_text(json.dumps(report,indent=2)+'\n')
fig=plt.figure(figsize=(16,7),facecolor='#f3f5f7')
draw(fig.add_subplot(131,projection='3d'),[holder,keeper],['#688ca5','#d49b48'],'Galaxy holder and retainer',[(-110,110),(-120,130),(0,18)],90,-90)
draw(fig.add_subplot(132,projection='3d'),[holder,plaque,keeper],['#688ca5','#c2c6c9','#d49b48'],'Plaque seated — single point up',[(-110,110),(-120,130),(0,18)],90,-90)
draw(fig.add_subplot(133,projection='3d'),[holder,keeper],['#688ca5','#d49b48'],'Three lower clips · upper-right keeper',[(-110,110),(-105,105),(0,30)],40,-60)
fig.tight_layout();fig.savefig(out/'galaxy_holder_preview.png',dpi=150,bbox_inches='tight')
print(json.dumps(report['galaxy_holder'],indent=2))
