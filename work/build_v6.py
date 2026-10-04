import trimesh as t,numpy as np,json
from pathlib import Path
out=Path('outputs/v6')
def box(sz,c):
 m=t.creation.box(sz);m.apply_translation(c);return m
def cyl(r,h,c,n=64):
 m=t.creation.cylinder(radius=r,height=h,sections=n);m.apply_translation(c);return m
def union(ms):return t.boolean.union(ms,engine='manifold')
def diff(a,bs):return t.boolean.difference([a]+bs,engine='manifold')
def beam(a,b,w=18):
 a=np.array(a);b=np.array(b);d=b-a;m=box([np.linalg.norm(d),w,8],[0,0,4]);m.apply_transform(t.transformations.rotation_matrix(np.arctan2(d[1],d[0]),[0,0,1]));m.apply_translation([*((a+b)/2),0]);return m
source=t.load('source_models/obj_1_Inclined display.stl')
frame=sorted(source.split(),key=lambda m:m.extents[2])[0];frame.apply_translation([-128,-126,0])
# Clip all additions to radius-100 inner hex, leaving the original outside band untouched.
pts=np.array([[100*np.cos(a),100*np.sin(a),z] for a in np.arange(6)*np.pi/3 for z in [-1,9]])
clip=t.convex.convex_hull(pts)
def reinforced(adds):
 interior=t.boolean.intersection([union(adds),clip],engine='manifold');return union([frame,interior])
fixholes=[]
for x,y in [(-15,65),(15,-65)]:
 fixholes.extend([cyl(4,20,[x,y-6,4]),box([3.5,6,20],[x,y-3,4]),cyl(1.75,20,[x,y,4])])
for x,y in [(-15,49),(15,-49)]:fixholes.extend([cyl(2.3,20,[x,y,4]),cyl(4.75,4.2,[x,y,6])])
# Wide spine carries both staggered wall-fixing pairs.
spine=box([52,174,8],[0,0,4])
open_tile=diff(reinforced([spine]),fixholes)
ship=reinforced([spine,box([80,80,8],[0,0,4]),beam([-100,0],[100,0])]);cuts=fixholes.copy()
for x in [-28,28]:
 for y in [-28,28]:cuts.extend([cyl(2.3,20,[x,y,4]),cyl(4.27,3.4,[x,y,1.65],6)])
ship=diff(ship,cuts)
# The formerly lower-right, lone tip becomes the apex. Keep the original two drilling positions.
tip=np.array([254.1015,24.70335]);lower_pair_mid=(np.array([.00315,100.08179])+np.array([86.88031,244.82089]))/2
angle=float(np.pi/2-np.arctan2(*(tip-lower_pair_mid)[::-1]));R=np.array([[np.cos(angle),-np.sin(angle)],[np.sin(angle),np.cos(angle)]])
plaque_offset=np.array([0.,-20.]);positions=[R@np.array([x,20.])+plaque_offset for x in [-40,40]]
adds=[spine,beam([-100,0],[100,0]),beam(positions[0],positions[1],22)]
for p in positions:adds.append(cyl(12,8,[*p,4]))
plaque=reinforced(adds);cuts=fixholes.copy()
for x,y in positions:cuts.extend([cyl(2.3,20,[x,y,4]),cyl(4.27,3.4,[x,y,1.65],6)])
plaque=diff(plaque,cuts)
# Verify plaque nuts do not break into neighbouring wall-fixing cutouts.
for x,y in positions:
 nut=cyl(4.27,3.4,[x,y,1.65],6)
 for hole in fixholes:
  overlap=t.boolean.intersection([nut,hole],engine='manifold');assert abs(overlap.volume)<1e-3
models={'hex_ship_original_size':ship,'hex_plaque_upright_original_size':plaque,'hex_open_original_size':open_tile}
for name in ['B_dual_socket_arm_130mm','peg_insert_1','peg_insert_2','socket_fit_test','peg_fit_7.7mm','peg_fit_7.8mm','peg_fit_7.9mm']:
 models[name]=t.load('outputs/v3/'+name+'.stl')
models['plaque_drilling_template']=t.load('outputs/v4/plaque_drilling_template.stl')
report={}
original_band=diff(frame,[clip])
for name,m in models.items():
 assert m.is_watertight and m.is_winding_consistent and len(m.split())==1 and m.volume>0,name
 m.export(out/(name+'.stl'));report[name]={'dimensions_mm':m.extents.tolist(),'watertight':True,'components':1,'volume_cm3':m.volume/1000}
 if name.startswith('hex_'):
  band=diff(m,[clip]);missing=abs(diff(original_band,[band]).volume);extra=abs(diff(band,[original_band]).volume);assert missing+extra<.01,(name,missing,extra)
  report[name]['protected_original_edge_difference_mm3']=missing+extra
report['original_neighbour_fit']={}
for k,xy in [('above',[0,181.86534]),('upper_right',[157.5,90.93267]),('lower_right',[157.5,-90.93267])]:
 neighbour=frame.copy();neighbour.apply_translation([*xy,0]);volume=abs(t.boolean.intersection([ship,neighbour],engine='manifold').volume);assert volume<.01;report['original_neighbour_fit'][k]={'translation_mm':xy,'intersection_mm3':volume}
report['plaque']={'rotation_counterclockwise_degrees':float(np.degrees(angle)),'offset_in_hex_mm':plaque_offset.tolist(),'M4_mount_centres_xy_mm':[p.tolist() for p in positions],'source_hole_centres_xy_mm':[[93.9122,121.9995],[173.9122,121.9995]]}
report['wall_fixings']={'nail_neck_centres_xy_mm':[[-15,65],[15,-65]],'keyhole_entry_diameter_mm':8,'neck_width_mm':3.5,'slide_mm':6,'screw_centres_xy_mm':[[-15,49],[15,-49]]}
(out/'geometry_checks.json').write_text(json.dumps(report,indent=2))
# Visual-only clipped decorative base; not delivered as a replacement printable STL.
base=t.load('work/decorative_base_trimmed.stl');base.apply_transform(t.transformations.rotation_matrix(angle,[0,0,1]));base.apply_translation([*plaque_offset,8]);base.export('work/v6_upright_plaque.stl')
print(json.dumps(report,indent=2))
