import trimesh as t,numpy as np,json
from pathlib import Path
out=Path('outputs'); out.mkdir(exist_ok=True)
def box(size,c):
 m=t.creation.box(size);m.apply_translation(c);return m
def cyl(r,h,c,sections=64):
 m=t.creation.cylinder(radius=r,height=h,sections=sections);m.apply_translation(c);return m
def union(ms):return t.boolean.union(ms,engine='manifold')
def diff(a,bs):return t.boolean.difference([a]+bs,engine='manifold')
def beam(a,b,width=18,h=8):
 a=np.array(a);b=np.array(b);d=b-a;m=box([np.linalg.norm(d),width,h],[0,0,h/2]);m.apply_transform(t.transformations.rotation_matrix(np.arctan2(d[1],d[0]),[0,0,1]));m.apply_translation([*(a+b)/2,0]);return m
src=t.load('source_models/obj_1_Inclined display.stl')
ring=sorted(src.split(),key=lambda m:m.extents[2])[0];ring.apply_translation([-128,-128,0])
a_parts=[ring,box([80,80,8],[0,0,4])]
for end in [[98,0],[-98,0],[0,86],[0,-86]]:a_parts.append(beam([0,0],end))
for y in [-65,65]:a_parts.append(cyl(10,8,[0,y,4]))
a=union(a_parts)
holes=[]
for x in [-28,28]:
 for y in [-28,28]:
  holes += [cyl(2.3,20,[x,y,5]),cyl(4.27,3.4,[x,y,1.65],6)]
for y in [-65,65]:holes += [cyl(2.3,20,[0,y,4]),cyl(4.75,4.2,[0,y,6])]
a=diff(a,holes)
# Peg reproduced from source, including actual tip geometry.
s=t.load('source_models/xxx_-_stand_sovereign_d.stl')
peg=t.boolean.intersection([s,box([40,40,40],[133.9122,101.9995,90.4])],engine='manifold')
peg.apply_translation([-133.9122,-101.9995,-11.4])
# Broad shoulder and four tapered gussets support the replacement arm.
b_parts=[cyl(9,56,[0,0,32]),cyl(3.9,19.2,[0,0,69.4])]
for angle in [0,np.pi/2,np.pi,3*np.pi/2]:
 pts=np.array([[5,-4,4],[31,-4,4],[5,-4,59],[5,4,4],[31,4,4],[5,4,59]])
 rib=t.convex.convex_hull(pts);rib.apply_transform(t.transformations.rotation_matrix(angle,[0,0,1]));b_parts.append(rib)
for part in b_parts: part.apply_transform(t.transformations.rotation_matrix(np.deg2rad(-5),[1,0,0],point=[0,0,8]))
b_parts.append(box([80,80,8],[0,0,4]))
b=diff(union(b_parts),[cyl(2.3,20,[x,y,5]) for x in [-28,28] for y in [-28,28]])
# A drilling template uses the same 56 mm square pattern.
template=diff(box([80,80,2],[0,0,1]),[cyl(1.25,8,[x,y,1]) for x in [-28,28] for y in [-28,28]]+[cyl(3.3,8,[0,0,1])])
for diameter in [7.7,7.8,7.9]:
 coupon=union([box([22,22,3],[0,0,1.5]),cyl(diameter/2,19.2,[0,0,12.4])])
 coupon.export(out/('peg_fit_'+str(diameter)+'mm.stl'))
report={} 
for name,m in [('A_hex_carrier',a),('B_arm_5deg_up',b),('drilling_template',template)]:
 m.export(out/(name+'.stl')); report[name]={'dimensions_mm':m.extents.tolist(),'watertight':bool(m.is_watertight),'positive_volume':bool(m.volume>0),'components':len(m.split()),'volume_cm3':m.volume/1000}
(out/'geometry_checks.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))
# Save an illustrative assembly with the original base digitally trimmed at z=11.4.
base=t.boolean.intersection([s,box([300,300,11.4],[128,122,5.7])],engine='manifold');base.apply_translation([-133.9122,-101.9995,8]);arm=b.copy();arm.apply_translation([0,0,19.4])
t.Scene([a,base,arm]).export('work/assembly.glb')
np.savez('work/assembly_bounds.npz',base_bounds=base.bounds)
