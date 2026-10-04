import trimesh as t,numpy as np,json,shutil
from pathlib import Path
out=Path('outputs/v28');out.mkdir(exist_ok=True)
def box(s,c):
 m=t.creation.box(s);m.apply_translation(c);return m
def cyl(r,h,c):
 m=t.creation.cylinder(radius=r,height=h,sections=128);m.apply_translation(c);return m
def union(ms):return t.boolean.union(ms,engine='manifold')
def diff(m,cs):return t.boolean.difference([m]+cs,engine='manifold')
for p in Path('outputs/v27').glob('*.stl'):
 if p.stem not in ['peg_insert_8mm','peg_insert_6mm']:shutil.copy2(p,out/p.name)
body=t.load(out/'hex_ship_integrated_rounded_arm.stl');checks={};report=json.load(open('outputs/v27/geometry_checks.json'))
for diam,length,height in [(8,19,3),(6,10,2)]:
 z0=11.6;shaft_start=z0+height;r=diam/2;spread=5-r
 # Quarter-ellipse profile, tangent to horizontal stem shoulder and vertical shaft.
 theta=np.linspace(0,np.pi/2,97)
 curve=np.c_[r+spread*(1-np.sin(theta)),z0+height*(1-np.cos(theta))]
 profile=np.vstack([[0,z0-.1],[5,z0-.1],curve,[0,shaft_start],[0,z0-.1]])
 fillet=t.creation.revolve(profile,sections=192)
 stem=box([10,10,z0],[0,0,z0/2]);shaft=cyl(r,length+.1,[0,0,shaft_start-.05+length/2]);holes=[]
 for axis in [[1,0,0],[0,1,0]]:
  h=cyl(1.7,20,[0,0,0]);h.apply_transform(t.geometry.align_vectors([0,0,1],axis));h.apply_translation([0,0,5.8]);holes.append(h)
 peg=diff(union([stem,fillet,shaft]),holes)
 p=out/f'peg_insert_{diam}mm.stl';peg.export(p);q=t.load(p);f=q.faces;q.update_faces((f[:,0]!=f[:,1])&(f[:,1]!=f[:,2])&(f[:,0]!=f[:,2]));q.update_faces(q.unique_faces());q.remove_unreferenced_vertices();assert q.is_volume and len(q.split())==1;q.export(p)
 up=q.copy();up.apply_transform(t.transformations.rotation_matrix(-np.pi/2,[1,0,0]));up.apply_translation([0,2.4,138])
 front=q.copy();front.apply_translation([0,0,154.4]);front.apply_transform(t.transformations.rotation_matrix(np.deg2rad(-5),[1,0,0],point=[0,0,150]))
 for label,m in [('upward',up),('outward',front)]:checks[f'{diam}mm_{label}_overlap_mm3']=abs(t.boolean.intersection([body,m],engine='manifold').volume)
 report[p.stem]={'dimensions_mm':q.extents.tolist(),'volume_cm3':q.volume/1000,'watertight':True,'components':1,'export_reload_verified':True,'transition_height_mm':height,'transition_profile':'quarter ellipse, revolved','radial_spread_mm':spread}
assert max(checks.values())<.01
coupon=union([box([16,16,3],[0,0,1.5]),cyl(3,10.1,[0,0,7.95])]);coupon.export(out/'fit_test_peg_6.0mm.stl')
for p in out.glob('*.stl'):
 m=t.load(p);assert m.is_volume and len(m.split())==1,p
report.pop('v27_peg_checks',None);report.pop('v27_peg_transitions',None);report['v28_peg_checks']=checks;report['v28_peg_dimensions']={'square_base_both_mm':[10,10,11.6],'6mm_round_length_mm':10,'6mm_transition_height_mm':2,'8mm_round_length_mm':19,'8mm_transition_height_mm':3,'cross_bolt_positions_unchanged':True}
(out/'geometry_checks.json').write_text(json.dumps(report,indent=2));print(checks)
