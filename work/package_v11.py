from pathlib import Path
import json,zipfile,trimesh as t
out=Path('outputs/v11')
s=Path('outputs/v10/Assembly_notes.txt').read_text()
s=s.replace('REVISION 10','REVISION 11').replace('Original nail mount, simplified frames, flush plaque clips.','Integrated rounded ship arm; original nail mount, simplified frames, flush plaque clips.')
s=s.replace('hex_ship_original_size.stl uses the same original nail mount, with the structural centre and spokes needed for the ship arm. Its earlier added keyholes and screw-hole fixing spine are removed.','hex_ship_integrated_rounded_arm.stl combines the structural hexagon and B dual-socket arm into one continuous printable solid. It replaces both hex_ship_original_size.stl and B_dual_socket_arm_130mm.stl. No arm-to-frame screws, nuts or assembly are needed. The four old attachment holes are filled. Exposed root, beam and brace edges have 3 mm rounding; the end receiver has 2.5 mm rounding. Functional socket openings and cross-bolt bores retain their dimensions.')
s=s.replace('The open/ship frames are 8 mm thick.','The open frame is 8 mm thick. The integrated ship mount is 166.773 mm deep overall, with an 8 mm outer frame.')
a=s.index('SHIP ARM — UNCHANGED');b=s.index('The top peg axis',a)
s=s[:a]+'INTEGRATED SHIP ARM\nPrint hex_ship_integrated_rounded_arm.stl as one part. The rounded root spans the former frame/flange joint without an attachment interface. The two peg inserts remain removable and still use M3 cross-bolts.\n'+s[b:]
a=s.index('Every delivered STL');b=s.index('These geometry checks',a)
s=s[:a]+'Every delivered STL was reloaded from disk and checked for watertightness, consistent winding, positive volume and a single connected solid. The new integrated arm checks confirm unchanged exterior frame and original nail tab, clearance for both peg inserts, and solid material at the four former attachment holes. The plaque and open-frame designs are unchanged from revision 10. See geometry_checks.json.\n'+s[b:]
s=s.replace('All parts fit within a 250 x 250 mm XY print area.','All parts fit within a 250 x 250 mm XY print area. Integrated mount bounds: 210 x 185.865 x 166.773 mm with the wall face on the bed. This is a geometric orientation, not a validated strength-oriented print profile; layer direction and support access need assessment in the slicer.')
(out/'Assembly_notes.txt').write_text(s)
r=json.loads((out/'geometry_checks.json').read_text())
for p in out.glob('*.stl'):
 m=t.load(p);assert m.is_volume and len(m.split(only_watertight=False))==1,p
 r[p.stem]['export_reload_verified']=True
r['export_cleanup']='Removed two zero-area triangles collapsed by STL vertex merging; geometry and volume unchanged.'
(out/'geometry_checks.json').write_text(json.dumps(r,indent=2))
with zipfile.ZipFile('outputs/Star_Trek_integrated_rounded_mount_v11.zip','w',zipfile.ZIP_DEFLATED) as z:
 for p in sorted(out.iterdir()):z.write(p,'v11/'+p.name)
print('All 12 STL files verified; package ready.')
