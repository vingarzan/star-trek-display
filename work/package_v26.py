from pathlib import Path
import json,zipfile
out=Path('outputs/v26')
s=Path('outputs/v25/Assembly_notes.txt').read_text().replace('REVISION 25','REVISION 26')
s=s.replace('The square stem continues to the round peg shoulder, preserving the round peg\'s installed position. Print stem-down as supplied.','A circular cone with a 10 mm base diameter now transitions from the square stem into the round shaft: a 3 mm transition on the 8 mm insert and a 5 mm transition on the 6 mm insert. The round shaft positions, engagement lengths and cross-bolt positions are unchanged. There is no projecting disk. The tapered shape is intended to reduce the abrupt shoulder; it has not been physically strength-tested. Print orientation and layer adhesion still affect breakage.')
a=s.index('PLAQUE POSITION');b=s.index('PRINTING AND CHECKS',a)
s=s[:a]+'''SNUG PLAQUE HOLDERS — CHOOSE MATCHING THICKNESS
5.7 mm plate: hex_plaque_snug_5.7mm.stl + plaque_latch_snug_5.7mm.stl.
4.7 mm plate: hex_plaque_snug_4.7mm.stl + plaque_latch_snug_4.7mm.stl.
Each pair has 0.2 mm nominal front clearance: 5.9 mm and 4.9 mm gaps respectively, measured from the frame face to the retaining lip/latch underside. The former clips had 0.6 mm clearance and latch about 0.9 mm. The two sets share the same XY outline, clip positions and latch attachment.
The 4.7 mm set assumes the same plaque rim shape and ornament clearance as the original plate, differing in thickness only. Its model check uses a thickness-scaled proxy, not a scan of the real 4.7 mm plate.
Print fit_test_plate_gap_5.7mm.stl or fit_test_plate_gap_4.7mm.stl and check the actual plate before printing its frame. These check the gap, not the full emblem outline. Nominal clearance is not a guarantee of a snug print on every material/printer.
The plaque stays flush against the frame. Its single emblem point faces up. Keep the selected latch removed while lowering the plaque into both lower clips, then fit the matching latch. It lifts off after removing its M3 screw; do not force the plaque past a closed latch.
Use an M3 x 14 screw, or an M3 x 16 with about 2 mm washer thickness, for the shorter latches. Verify actual engagement and that the screw does not bottom out in the printed pilot hole. Tighten lightly. No plaque drilling is needed.

''' +s[b:]
s+='\nREVISION 26 VALIDATION\nBoth tapered inserts clear both sockets. Both holder/latch sets clear the seated reference or thickness proxy and the sampled removal paths. New clip and latch geometry stays inside the original hex outline. Exported meshes are watertight single solids. The ship frame and nail cap are unchanged. Physical fit and strength testing remain required, particularly given the reported peg breakage.\n'
(out/'Assembly_notes.txt').write_text(s)
r=json.load(open(out/'geometry_checks.json'))
for key in ['plaque_latch','plaque_corner_clips','new_pegs','new_peg_checks']:r.pop(key,None)
(out/'geometry_checks.json').write_text(json.dumps(r,indent=2))
with zipfile.ZipFile('outputs/Star_Trek_tapered_pegs_snug_plates_v26.zip','w',zipfile.ZIP_DEFLATED) as z:
 for p in sorted(out.iterdir()):z.write(p,'v26/'+p.name)
print('Package ready.')
