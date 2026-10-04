import trimesh as t,numpy as np,json
from pathlib import Path
out=Path('outputs/v3');out.mkdir(exist_ok=True)
def box(size,c):
 m=t.creation.box(size);m.apply_translation(c);return m
def cyl(r,h,c):
 m=t.creation.cylinder(radius=r,height=h,sections=64);m.apply_translation(c);return m
def union(ms):return t.boolean.union(ms,engine='manifold')
def diff(a,bs):return t.boolean.difference([a]+bs,engine='manifold')
def bore_x(c,r=1.7):
 m=cyl(r,50,[0,0,0]);m.apply_transform(t.geometry.align_vectors([0,0,1],[1,0,0]));m.apply_translation(c);return m
# Coordinates: wall X/Y, +Y upward, +Z into room; flange back at decorative front Z=0.
# Straight upper beam, continuous underside brace, unchanged 56 mm square M4 fixing pattern.
brace=t.convex.convex_hull(np.array([[x,y,z] for x in [-7,7] for y,z in [(-35,6),(-12,6),(-12,143)]]))
parts=[box([80,80,8],[0,0,4]),box([28,28,138],[0,0,75]),brace]
# Level-flight socket faces up, with its centre precisely 130 mm beyond decorative base.
up_void=box([10.4,16,10.4],[0,9.8,130]) # Floor at Y=1.8; exits top Y=14.
up_bolt=bore_x([0,8.2,130])
# Second receiver points out and 5 degrees up. It sits beyond the upward socket.
rot=t.transformations.rotation_matrix(np.deg2rad(-5),[1,0,0],point=[0,0,142])
front=box([24,24,18],[0,0,149]);front.apply_transform(rot);parts.append(front)
front_void=box([10.4,10.4,16],[0,0,153.8]);front_void.apply_transform(rot)
front_bolt=bore_x([0,0,152.2]);front_bolt.apply_transform(rot)
body=diff(union(parts),[up_void,up_bolt,front_void,front_bolt]+[cyl(2.3,20,[x,y,4]) for x in [-28,28] for y in [-28,28]])
peg=t.load('outputs/v2/peg_insert_1.stl')
up=peg.copy();up.apply_transform(t.transformations.rotation_matrix(-np.pi/2,[1,0,0]));up.apply_translation([0,2.4,130])
front_peg=peg.copy();front_peg.apply_translation([0,0,146.4]);front_peg.apply_transform(rot)
models={'B_dual_socket_arm_130mm':body}
for name in ['A_hex_carrier_244mm','peg_insert_1','peg_insert_2','socket_fit_test','drilling_template','peg_fit_7.7mm','peg_fit_7.8mm','peg_fit_7.9mm']:
 models[name]=t.load('outputs/v2/'+name+'.stl')
report={}
for name,m in models.items():
 assert m.is_watertight and m.is_winding_consistent and m.volume>0 and len(m.split())==1
 assert max(m.extents[:2])<=250
 m.export(out/(name+'.stl'));report[name]={'dimensions_mm':m.extents.tolist(),'watertight':True,'components':1,'volume_cm3':m.volume/1000}
checks={}
for name,m in [('level_flight',up),('wall_parallel',front_peg)]:
 volume=float(t.boolean.intersection([body,m],engine='manifold').volume);assert abs(volume)<.001;checks[name]={'intersection_mm3':volume};m.export('work/v3_'+name+'_insert.stl')
report['assembly_checks']=checks
report['level_flight_peg_axis']={'wall_clearance_from_decorative_front_mm':130,'axis':[0,1,0],'peg_shoulder_height_Y_mm':17}
report['static_ship_moment_only_Nm']=.6*9.81*.130
(out/'geometry_checks.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))
