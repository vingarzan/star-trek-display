import trimesh as t,numpy as np,json
from pathlib import Path
out=Path('outputs/v2');out.mkdir(exist_ok=True)
def box(size,c):
 m=t.creation.box(size);m.apply_translation(c);return m
def cyl(r,h,c):
 m=t.creation.cylinder(radius=r,height=h,sections=64);m.apply_translation(c);return m
def union(ms):return t.boolean.union(ms,engine='manifold')
def diff(a,bs):return t.boolean.difference([a]+bs,engine='manifold')
def cross(axis,z,length=32):
 m=cyl(1.7,length,[0,0,0]);m.apply_transform(t.geometry.align_vectors([0,0,1],axis));m.apply_translation([0,0,z]);return m
rot=t.transformations.rotation_matrix(np.deg2rad(-5),[1,0,0],point=[0,0,8])
parts=[cyl(9,56,[0,0,32]),box([20,20,14],[0,0,53])]
for angle in [0,np.pi/2,np.pi,3*np.pi/2]:
 rib=t.convex.convex_hull(np.array([[5,-4,4],[31,-4,4],[5,-4,59],[5,4,4],[31,4,4],[5,4,59]]));rib.apply_transform(t.transformations.rotation_matrix(angle,[0,0,1]));parts.append(rib)
body=diff(union(parts),[box([10.4,10.4,14],[0,0,54.8]),cross([1,0,0],54.2)])
body.apply_transform(rot)
body=diff(union([body,box([80,80,8],[0,0,4])]),[cyl(2.3,20,[x,y,5]) for x in [-28,28] for y in [-28,28]])
# Square stem seats with 0.6 mm bottom clearance; collar rests on socket rim.
peg=union([box([10,10,11.8],[0,0,54.3]),cyl(9,3,[0,0,61.5]),cyl(3.9,19.2,[0,0,72.4])])
peg=diff(peg,[cross([1,0,0],54.2),cross([0,1,0],54.2)])
# exposed peg z63..82, print insert with stem end on z0.
insert=peg.copy();insert.apply_translation([0,0,-48.4])
assembled=peg.copy();assembled.apply_transform(rot)
inter=t.boolean.intersection([body,assembled],engine='manifold')
assert abs(inter.volume)<1e-3,inter.volume
socket_test=diff(box([20,20,15],[0,0,7.5]),[box([10.4,10.4,14],[0,0,9.8]),cross([1,0,0],9.2)])
# Enlarged single-print carrier; central hardware remains unscaled.
source=t.load('source_models/obj_1_Inclined display.stl')
ring=sorted(source.split(),key=lambda m:m.extents[2])[0];ring.apply_translation([-128,-128,0]);ring.apply_scale([244/210,244/210,1])
a_parts=[ring,box([80,80,8],[0,0,4])]
for end in [[114,0],[-114,0],[0,100],[0,-100]]:
 v=np.array(end);beam=box([np.linalg.norm(v),20,8],[0,0,4]);beam.apply_transform(t.transformations.rotation_matrix(np.arctan2(v[1],v[0]),[0,0,1]));beam.apply_translation([*(v/2),0]);a_parts.append(beam)
for y in [-78,78]:a_parts.append(cyl(11,8,[0,y,4]))
holes=[]
for x in [-28,28]:
 for y in [-28,28]:
  nut=t.creation.cylinder(radius=4.27,height=3.4,sections=6);nut.apply_translation([x,y,1.65]);holes.extend([cyl(2.3,20,[x,y,5]),nut])
for y in [-78,78]:holes.extend([cyl(2.3,20,[0,y,4]),cyl(4.75,4.2,[0,y,6])])
carrier=diff(union(a_parts),holes)
models={'A_hex_carrier_244mm':carrier,'socket_fit_test':socket_test,'B_socket_arm_5deg_up':body,'peg_insert_1':insert,'peg_insert_2':insert.copy()}
for name in ['drilling_template','peg_fit_7.7mm','peg_fit_7.8mm','peg_fit_7.9mm']:
 models[name]=t.load('outputs/'+name+'.stl')
report={}
for name,m in models.items():
 assert m.is_watertight and m.is_winding_consistent and m.volume>0 and len(m.split())==1
 m.export(out/(name+'.stl'));report[name]={'dimensions_mm':m.extents.tolist(),'watertight':True,'components':1,'volume_cm3':m.volume/1000}
report['assembled_clearance_check']={'intersection_volume_mm3':inter.volume,'square_socket_mm':10.4,'square_stem_mm':10,'cross_bolt_hole_mm':3.4,'rotation_step_degrees':90}
(out/'geometry_checks.json').write_text(json.dumps(report,indent=2))
# Combined print layout, with two separate inserts and body: three intentional solids.
p1=insert.copy();p1.apply_translation([58,0,0]);p2=insert.copy();p2.apply_translation([82,0,0]);t.util.concatenate([body,p1,p2]).export(out/'B_arm_and_two_inserts_layout.stl')
assembled.export('work/v2_insert_assembled.stl')
print(json.dumps(report,indent=2))
