import trimesh as t,numpy as np,json,shutil
from pathlib import Path
out=Path('outputs/v23');out.mkdir(exist_ok=True)
def box(s,c):
 m=t.creation.box(s);m.apply_translation(c);return m
def union(ms):return t.boolean.union(ms,engine='manifold')
def diff(m,cs):return t.boolean.difference([m]+cs,engine='manifold')
y=78.93266296386719
old=t.load('outputs/v22/hex_ship_integrated_rounded_arm.stl')
pocket=box([14,12,8],[0,y,9]);body=diff(old,[pocket]) # floor Z=5
# Hollow cover, 0.2 mm side clearance, 1.2 mm roof.
roof=box([13.6,11.6,1.2],[0,y,9.8])
skirt=diff(box([13.6,11.6,4],[0,y,7.2]),[box([11.8,9.8,5],[0,y,7.2])])
slots=[box([2,.6,3.4],[x,y+v,6.9]) for x in [-6.35,6.35] for v in [-3.4,3.4]]
skirt=diff(skirt,slots)
nubs=[]
for sign in [-1,1]:
 pts=np.array([[sign*x,y+v,z] for x,z in [(6.7,6.2),(7.05,6.7),(6.7,7.2)] for v in [-1.5,1.5]])
 nubs.append(t.convex.convex_hull(pts))
cap=union([roof,skirt]+nubs)
# Fingernail/tool recess at one roof end.
cap=diff(cap,[box([4,1.3,.6],[0,y-5.55,9.4])])
# Nominal cap clears holder apart from intentional 0.05 mm grip nibs.
nominal=diff(cap,nubs);overlap=abs(t.boolean.intersection([nominal,body],engine='manifold').volume);assert overlap<.01
# Verify centred 9 mm diameter, 4 mm high hardware head envelope.
head=t.creation.cylinder(radius=4.5,height=4,sections=96);head.apply_translation([0,y,7]);assert abs(t.boolean.intersection([cap,head],engine='manifold').volume)<.01
coupon=diff(box([18,16,8],[0,y,4]),[pocket]);hole=t.creation.cylinder(radius=2.6,height=12,sections=64);hole.apply_translation([0,y,4]);coupon=diff(coupon,[hole]);coupon.apply_translation([0,-y,0])
cap.export('work/v23_cap_installed.stl')
# Print on flat roof: hollow side faces upward, no internal roof supports.
printcap=cap.copy();printcap.apply_translation([0,-y,0]);printcap.apply_transform(t.transformations.rotation_matrix(np.pi,[1,0,0]));printcap.apply_translation([0,0,10.4])
for p in Path('outputs/v22').glob('*.stl'):
 if p.name!='hex_ship_integrated_rounded_arm.stl':shutil.copy2(p,out/p.name)
for name,m in [('hex_ship_integrated_rounded_arm',body),('nail_cover_cap',printcap),('nail_cover_fit_test',coupon)]:
 m.export(out/(name+'.stl'));q=t.load(out/(name+'.stl'));f=q.faces;q.update_faces((f[:,0]!=f[:,1])&(f[:,1]!=f[:,2])&(f[:,0]!=f[:,2]));q.update_faces(q.unique_faces());q.remove_unreferenced_vertices();assert q.is_volume and len(q.split())==1;q.export(out/(name+'.stl'));assert t.load(out/(name+'.stl')).is_volume
r=json.load(open('outputs/v22/geometry_checks.json'))
for name in ['hex_ship_integrated_rounded_arm','nail_cover_cap','nail_cover_fit_test']:
 m=t.load(out/(name+'.stl'));r[name]={'dimensions_mm':m.extents.tolist(),'volume_cm3':m.volume/1000,'watertight':True,'export_reload_verified':True,'components':1}
r['nail_adapter']={'seat_height_from_wall_mm':5,'recess_depth_mm':3,'pocket_xy_mm':[14,12],'cap_proud_of_frame_mm':2.4,'head_envelope_diameter_mm':9,'head_envelope_height_mm':4,'cap_side_clearance_mm':.2,'grip_nib_interference_each_side_mm':.05,'nominal_cap_overlap_mm3':overlap,'retention':'two flexible friction fingers; physical fit untested'}
(out/'geometry_checks.json').write_text(json.dumps(r,indent=2));print('Verified models and head clearance.')
