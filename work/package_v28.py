from pathlib import Path
import json,zipfile,trimesh as t
out=Path('outputs/v28');r=json.load(open(out/'geometry_checks.json'))
cut=t.creation.box([20,20,11.6]);cut.apply_translation([0,0,5.8]);bases=[]
for d in [6,8]:bases.append(t.boolean.intersection([t.load(out/f'peg_insert_{d}mm.stl'),cut],engine='manifold'))
err=abs(t.boolean.difference(bases,engine='manifold').volume)+abs(t.boolean.difference(bases[::-1],engine='manifold').volume);assert err<.001
r['identical_square_bases_difference_mm3']=err
m=t.load(out/'fit_test_peg_6.0mm.stl');r['fit_test_peg_6.0mm']['dimensions_mm']=m.extents.tolist();r['fit_test_peg_6.0mm']['volume_cm3']=m.volume/1000
(out/'geometry_checks.json').write_text(json.dumps(r,indent=2))
s=Path('outputs/v27/Assembly_notes.txt').read_text();s=s.replace('REVISION 27','REVISION 28')
a=s.index('PEG INSERTS');b=s.index('\n\nORIGINAL FRAME',a)
s=s[:a]+'''PEG INSERTS — REVISION 28
Both inserts now have the SAME 10 x 10 x 11.6 mm square base and perpendicular 3.4 mm cross-bores centred 5.8 mm from the bottom. Their rounded transitions begin at the socket rim in the bolt-aligned position. Keep the M3 retaining bolt installed; the insert is not intended to be pushed to the bottom of the socket (0.6 mm bottom clearance).
peg_insert_8mm.stl: unchanged 8 mm diameter shaft, 19 mm usable length, 3 mm-high curved transition; total height 33.6 mm.
peg_insert_6mm.stl: 6 mm diameter shaft shortened from 11 to 10 mm; 2 mm radius rounded transition; total height 23.6 mm. The square base is shortened from 12.6 to 11.6 mm, matching the other insert. The round shaft starts at Z=13.6 mm rather than 14.6 mm. A nominal 12 mm-deep ship hole therefore has 2 mm axial clearance before reaching the rounded transition; actual contact depends on the entrance shape and print tolerances.
The disk remains omitted. Glue only the round shaft into the ship and keep the square stem removable. Support the ship while removing its cross-bolt. The updated fit_test_peg_6.0mm.stl has the same 10 mm usable test shaft; it checks bore fit and depth but does not reproduce the rounded shoulder. Test the full insert before gluing.
''' +s[b:]
s+='\nREVISION 28 VALIDATION\nBoth square base solids were compared and are identical. Both insert meshes clear both arm sockets in the bolt-aligned positions. Exported meshes remain single watertight solids. The 8 mm insert, arm, snug plaque sets and nail cap are otherwise unchanged. Physical fit and strength still require testing.\n';(out/'Assembly_notes.txt').write_text(s)
with zipfile.ZipFile('outputs/Star_Trek_matching_peg_bases_v28.zip','w',zipfile.ZIP_DEFLATED) as z:
 for p in sorted(out.iterdir()):z.write(p,'v28/'+p.name)
print('Identical square bases verified; package ready.')
