from pathlib import Path
import trimesh as t,numpy as np,json,zipfile
out=Path('outputs/v29');r=json.load(open(out/'geometry_checks.json'))
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
s=Path('outputs/v28/Assembly_notes.txt').read_text().replace('REVISION 28','REVISION 29');a=s.index('PEG INSERTS');b=s.index('\n\nORIGINAL FRAME',a)
s=s[:a]+'''PEG INSERTS — REVISION 29
Both inserts have identical 10.3 x 10.3 x 12.05 mm square stems, with a 0.4 mm lead-in chamfer. This changes side clearance from 0.2 mm to 0.05 mm per face in the existing 10.4 mm sockets. The lower stem is extended 0.45 mm, reducing nominal bottom clearance from 0.6 mm to 0.15 mm at the bolt-aligned position.
The cross-bores are retained, 3.4 mm diameter, 6.25 mm from the new bottom. Their installed positions still match the arm. A pin/M3 cross-bolt remains optional hardware for positive retention.
Pin-free retention relies ONLY on physical friction. Nominal CAD clearance cannot guarantee grip across printers/materials. There is no axial stop: without a bolt, an insert can slide the remaining 0.15 mm to the socket floor. Do not claim a fixed 0.15 mm floor gap when fully pushed to the bottom. Bottoming this amount remains within the nominal M3/3.4 mm hole allowance, but verify physically.
Print fit_test_arm_stem_10.2mm, 10.3mm and 10.4mm to choose a fit that can be removed by hand but does not slip under the actual ship load. Production inserts use 10.3 mm. Do not force a tight sample. If the production insert does not hold securely, use the retained cross-bolt until the stem fit is adjusted. Support the ship whenever removing it.
The 8 mm round shaft remains 19 mm long with a 3 mm curved transition. The 6 mm round shaft remains 10 mm long with a 2 mm rounded transition. Their bolt-aligned installed shaft positions are unchanged from v28. Glue only the round shaft into the ship.
''' +s[b:]
s+='\nREVISION 29 VALIDATION\nIdentical lower stems verified by solid comparison. Both socket positions have 0.15 mm nominal floor clearance at bolt alignment and clear M3 bolt paths. The inserted solids clear the arm. Pin-free grip and load capacity have not been physically tested. All other models remain from v28.\n';(out/'Assembly_notes.txt').write_text(s)
for p in out.glob('*.stl'):
 m=t.load(p);assert m.is_volume and len(m.split())==1,p
with zipfile.ZipFile('outputs/Star_Trek_removable_snug_pegs_v29.zip','w',zipfile.ZIP_DEFLATED) as z:
 for p in sorted(out.iterdir()):z.write(p,'v29/'+p.name)
print(audit)
