import trimesh as t,numpy as np,json,shutil
from pathlib import Path
out=Path('outputs/v26');out.mkdir(exist_ok=True)
def box(s,c):
 m=t.creation.box(s);m.apply_translation(c);return m
def cyl(r,h,c):
 m=t.creation.cylinder(radius=r,height=h,sections=128);m.apply_translation(c);return m
def union(ms):return t.boolean.union(ms,engine='manifold')
def diff(m,cs):return t.boolean.difference([m]+cs,engine='manifold')
oldnames={'hex_plaque_flush_clips','plaque_upper_right_latch','fit_test_rim_clip','peg_insert_8mm','peg_insert_6mm'}
for p in Path('outputs/v25').glob('*.stl'):
 if p.stem not in oldnames:shutil.copy2(p,out/p.name)
report=json.load(open('outputs/v25/geometry_checks.json'))
for name in oldnames:report.pop(name,None)
checks={};body=t.load(out/'hex_ship_integrated_rounded_arm.stl')
for diam,length,taper_height in [(8,19,3),(6,11,5)]:
 z0=14.6-taper_height
 stem=box([10,10,z0+.1],[0,0,(z0+.1)/2])
 pts=[[5*np.cos(a),5*np.sin(a),z0] for a in np.arange(128)*2*np.pi/128]+[[diam/2*np.cos(a),diam/2*np.sin(a),14.6] for a in np.arange(128)*2*np.pi/128]
 taper=t.convex.convex_hull(np.array(pts));shaft=cyl(diam/2,length+.1,[0,0,14.55+length/2]);holes=[]
 for axis in [[1,0,0],[0,1,0]]:
  h=cyl(1.7,20,[0,0,0]);h.apply_transform(t.geometry.align_vectors([0,0,1],axis));h.apply_translation([0,0,5.8]);holes.append(h)
 peg=diff(union([stem,taper,shaft]),holes);peg.export(out/f'peg_insert_{diam}mm.stl')
 up=peg.copy();up.apply_transform(t.transformations.rotation_matrix(-np.pi/2,[1,0,0]));up.apply_translation([0,2.4,138])
 front=peg.copy();front.apply_translation([0,0,154.4]);front.apply_transform(t.transformations.rotation_matrix(np.deg2rad(-5),[1,0,0],point=[0,0,150]))
 for label,m in [('upward',up),('outward',front)]:checks[f'{diam}mm_{label}_overlap_mm3']=abs(t.boolean.intersection([body,m],engine='manifold').volume)
open_hex=t.load(out/'hex_open_original_size.stl')
outline=t.convex.convex_hull(np.array([[105*np.cos(a),105*np.sin(a),z] for a in np.arange(6)*np.pi/3 for z in [-1,30]]))
# Use saved positioned plaque for fit checks; 4.7 mm uses same-outline thickness proxy.
original=t.load('work/v13_plaque.ply');f=original.faces;original.update_faces((f[:,0]!=f[:,1])&(f[:,1]!=f[:,2])&(f[:,0]!=f[:,2]));original.update_faces(original.unique_faces());px,py=51,88.3
for thickness in [5.7,4.7]:
 gap=thickness+.2;front=8+gap;parts=[open_hex]
 for x in [-48,48]:
  seat=-87.43;root=box([6,5.5,2],[x,-87.55,7]);floor=box([6,3,front+3-6],[x,seat-1.5,(6+front+3)/2]);lip=box([4.2,6,3],[np.sign(x)*47.1,seat,front+1.5]);parts.append(t.boolean.intersection([union([root,floor,lip]),outline],engine='manifold'))
 holder=diff(union(parts),[cyl(1.3,7,[px,py,4.5])])
 boss=cyl(2.5,gap+.1,[px,py,8+(gap+.1)/2]);keeper=union([boss,cyl(2.5,3,[px,py,front+1.5]),box([5,10,3],[px,py-5,front+1.5]),cyl(2.5,3,[px,py-10,front+1.5])]);keeper=diff(keeper,[cyl(1.7,24,[px,py,12])])
 plaque=original.copy();plaque.vertices[:,2]=8+(plaque.vertices[:,2]-8)*thickness/5.7
 for label,m in [('holder',holder),('latch',keeper)]:checks[f'{thickness}mm_{label}_seated_overlap_mm3']=abs(t.boolean.intersection([m,plaque],engine='manifold').volume)
 for dy in [0,2,5,10]:
  p=plaque.copy();p.apply_translation([0,dy,0]);checks[f'{thickness}mm_lift_{dy}_overlap_mm3']=abs(t.boolean.intersection([holder,p],engine='manifold').volume)
 for dz in [0,2,5,10]:
  k=keeper.copy();k.apply_translation([0,0,dz]);checks[f'{thickness}mm_unlatch_{dz}_overlap_mm3']=abs(t.boolean.intersection([k,plaque],engine='manifold').volume)
 assert abs(diff(diff(holder,[open_hex]),[outline]).volume)<.01
 assert abs(diff(keeper,[outline]).volume)<.01
 holder.export(out/f'hex_plaque_snug_{thickness}mm.stl');keeper.export(f'work/v26_latch_{thickness}mm.stl');kp=keeper.copy();kp.apply_translation([-px,-py,-8]);kp.export(out/f'plaque_latch_snug_{thickness}mm.stl')
 # U-shaped thickness gauge: same gap as both clips and latch.
 gauge=union([box([12,10,2],[0,0,1]),box([12,2,gap+4],[0,-4,(gap+4)/2]),box([12,6,2],[0,-2,3+gap])]);gauge.export(out/f'fit_test_plate_gap_{thickness}mm.stl')
assert max(checks.values())<.01,checks
for p in out.glob('*.stl'):
 m=t.load(p);f=m.faces;m.update_faces((f[:,0]!=f[:,1])&(f[:,1]!=f[:,2])&(f[:,0]!=f[:,2]));m.update_faces(m.unique_faces());m.remove_unreferenced_vertices();assert m.is_volume and len(m.split())==1,p;m.export(p);assert t.load(p).is_volume
 report[p.stem]={'dimensions_mm':m.extents.tolist(),'watertight':True,'components':1,'export_reload_verified':True,'volume_cm3':m.volume/1000}
report['v26_checks']=checks;report['v26_plate_gaps_mm']={'5.7mm_plate':5.9,'4.7mm_plate':4.9};report['v26_pegs']={'8mm_taper_height_mm':3,'6mm_taper_height_mm':5,'round_shaft_positions_and_lengths_unchanged':True,'taper_shape':'circular cone, 10 mm base diameter'};report['4.7mm_geometry_assumption']='same plaque outline; reference plaque Z thickness scaled for interference checks, not verified against actual 4.7mm plate'
(out/'geometry_checks.json').write_text(json.dumps(report,indent=2));print(checks)
