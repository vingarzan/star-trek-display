import trimesh as t,numpy as np,json,shutil
from pathlib import Path
out=Path('outputs/v25');out.mkdir(exist_ok=True)
def box(s,c):
 m=t.creation.box(s);m.apply_translation(c);return m
def cyl(r,h,c):
 m=t.creation.cylinder(radius=r,height=h,sections=128);m.apply_translation(c);return m
def union(ms):return t.boolean.union(ms,engine='manifold')
def diff(m,cs):return t.boolean.difference([m]+cs,engine='manifold')
renames={'rim_clip_fit_test':'fit_test_rim_clip','socket_fit_test':'fit_test_socket','nail_cover_fit_test':'fit_test_nail_cover','original_joint_test_top':'fit_test_original_joint_top','original_joint_test_bottom':'fit_test_original_joint_bottom','peg_fit_7.7mm':'fit_test_peg_7.7mm','peg_fit_7.8mm':'fit_test_peg_7.8mm','peg_fit_7.9mm':'fit_test_peg_7.9mm'}
for p in Path('outputs/v24').glob('*.stl'):
 if p.stem in ['peg_insert_1','peg_insert_2']:continue
 shutil.copy2(p,out/(renames.get(p.stem,p.stem)+'.stl'))
body=t.load(out/'hex_ship_integrated_rounded_arm.stl');checks={}
for diam,length in [(8,19),(6,11)]:
 # Collar removed; continuous square stem fills previous collar height.
 stem=box([10,10,14.6],[0,0,7.3]);peg=cyl(diam/2,length+.1,[0,0,14.55+length/2])
 holes=[]
 for axis in [[1,0,0],[0,1,0]]:
  h=cyl(1.7,20,[0,0,0]);h.apply_transform(t.geometry.align_vectors([0,0,1],axis));h.apply_translation([0,0,5.8]);holes.append(h)
 m=diff(union([stem,peg]),holes)
 name=f'peg_insert_{diam}mm';m.export(out/(name+'.stl'))
 up=m.copy();up.apply_transform(t.transformations.rotation_matrix(-np.pi/2,[1,0,0]));up.apply_translation([0,2.4,138])
 front=m.copy();front.apply_translation([0,0,154.4]);front.apply_transform(t.transformations.rotation_matrix(np.deg2rad(-5),[1,0,0],point=[0,0,150]))
 for label,installed in [('upward',up),('outward',front)]:
  v=abs(t.boolean.intersection([installed,body],engine='manifold').volume);assert v<.01,(name,label,v);checks[name+'_'+label+'_overlap_mm3']=v
 coupon=union([box([16,16,3],[0,0,1.5]),cyl(diam/2,length+.1,[0,0,2.95+length/2])]);coupon.export(out/f'fit_test_peg_{diam}.0mm.stl')
r=json.load(open('outputs/v24/geometry_checks.json'))
for old,new in renames.items():
 if old in r:r[new]=r.pop(old)
for key in ['peg_insert_1','peg_insert_2']:r.pop(key,None)
for p in out.glob('*.stl'):
 m=t.load(p);f=m.faces;m.update_faces((f[:,0]!=f[:,1])&(f[:,1]!=f[:,2])&(f[:,0]!=f[:,2]));m.update_faces(m.unique_faces());m.remove_unreferenced_vertices();assert m.is_volume and len(m.split())==1,p;m.export(p);assert t.load(p).is_volume
 r[p.stem]={'dimensions_mm':m.extents.tolist(),'volume_cm3':m.volume/1000,'watertight':True,'components':1,'export_reload_verified':True}
r['new_peg_checks']=checks;r['new_pegs']={'8mm':{'diameter_mm':8,'exposed_length_mm':19},'6mm':{'diameter_mm':6,'exposed_length_mm':11,'intended_hole_depth_mm':12},'stem_mm':[10,10,14.6],'cross_bore_diameter_mm':3.4,'cross_bore_centre_z_mm':5.8,'overhanging_disk':False,'cross_bolt_required_for_depth_retention':True}
(out/'geometry_checks.json').write_text(json.dumps(r,indent=2));print(checks)
