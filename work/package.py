from pathlib import Path
import trimesh as t,numpy as np,json,zipfile
out=Path('outputs');r=json.load(open(out/'geometry_checks.json'))
def box(s,c):
 m=t.creation.box(s);m.apply_translation(c);return m
for width in [10.2,10.3,10.4]:
 stem=box([width,width,11.7],[0,0,6.2]);lead=t.convex.convex_hull(np.array([[x,y,0] for x in [-width/2+.4,width/2-.4] for y in [-width/2+.4,width/2-.4]]+[[x,y,.4] for x in [-width/2,width/2] for y in [-width/2,width/2]]));handle=t.creation.cylinder(radius=4,height=8.1,sections=96);handle.apply_translation([0,0,16.0]);m=t.boolean.union([stem,lead,handle],engine='manifold');holes=[]
 for axis in [[1,0,0],[0,1,0]]:
  h=t.creation.cylinder(radius=1.7,height=20,sections=64);h.apply_transform(t.geometry.align_vectors([0,0,1],axis));h.apply_translation([0,0,6.25]);holes.append(h)
 m=t.boolean.difference([m]+holes,engine='manifold');p=out/f'fit_test_arm_stem_{width:.1f}mm.stl';m.export(p);assert t.load(p).is_volume;r[p.stem]={'stem_width_mm':width,'square_base_height_mm':12.05,'watertight':True}
# Compare the lower 12.05 mm of both inserts and check nominal floor/bolt geometry.
cut=box([20,20,12.05],[0,0,6.025]);bases=[t.boolean.intersection([t.load(out/f'peg_insert_{d}mm.stl'),cut],engine='manifold') for d in [6,8]]
err=sum(abs(t.boolean.difference(pair,engine='manifold').volume) for pair in [bases,bases[::-1]]);assert err<.001;r['identical_square_bases_difference_mm3']=err
arm=t.load(out/'hex_ship_integrated_rounded_arm.stl');R=t.transformations.rotation_matrix(np.deg2rad(-5),[1,0,0],point=[0,0,150]);U=t.transformations.rotation_matrix(-np.pi/2,[1,0,0]);U[:3,3]=[0,1.95,138];F=R@t.transformations.translation_matrix([0,0,153.95]);audit={}
for label,T in [('upward',U),('outward',F)]:
 a=arm.copy();a.apply_transform(np.linalg.inv(T));v=a.section(plane_normal=[1,0,0],plane_origin=[0,0,0]).vertices;floor=v[(abs(v[:,1])<5.3)&(v[:,2]>-1)&(v[:,2]<0)][:,2].max();assert abs(floor+.15)<.001
 h=t.creation.cylinder(radius=1.5,height=60,sections=96);h.apply_transform(t.geometry.align_vectors([0,0,1],[1,0,0]));h.apply_translation([0,0,6.25]);assert abs(t.boolean.intersection([a,h],engine='manifold').volume)<.001
 audit[label]={'bottom_gap_at_bolt_alignment_mm':float(-floor),'M3_bolt_path_clear':True}
 for d in [6,8]:assert abs(t.boolean.intersection([t.load(out/f'peg_insert_{d}mm.stl'),h],engine='manifold').volume)<.001
r['v29_socket_audit']=audit;(out/'geometry_checks.json').write_text(json.dumps(r,indent=2))
for p in out.glob('*.stl'):
 m=t.load(p);assert m.is_volume and len(m.split())==1,p
with zipfile.ZipFile('outputs/Star_Trek_display.zip','w',zipfile.ZIP_DEFLATED) as z:
 for p in sorted(out.iterdir()):
  if p.is_file() and p.suffix!='.zip':z.write(p,p.name)
print(audit)
