from pathlib import Path
import shutil,json
s=Path('work/build_v11.py').read_text().split('# Four former mounting')[0]
s=s.replace("out=Path('outputs/v11')","out=Path('outputs/v15');out.mkdir(exist_ok=True)")
s=s.replace('root=round_convex(box([80,80,16],[0,0,8]),3)','root=hex_prism(30,0,8);root.apply_translation([0,-9,0])')
s=s.replace('box([28,28,138],[0,0,83])','box([28,28,146],[0,0,79])')
s=s.replace('for y,z in [(-35,6),(-12,6),(-12,143)]','for y,z in [(-35,-2),(-12,-2),(-12,143)]')
exec(s)
assert body.is_volume and len(body.split())==1
for p in Path('outputs/v14').glob('*.stl'):
 if p.name!='hex_ship_integrated_rounded_arm.stl':shutil.copy2(p,out/p.name)
p=out/'hex_ship_integrated_rounded_arm.stl';body.export(p);q=t.load(p);faces=q.faces;q.update_faces((faces[:,0]!=faces[:,1])&(faces[:,1]!=faces[:,2])&(faces[:,0]!=faces[:,2]));q.update_faces(q.unique_faces());q.remove_unreferenced_vertices();assert q.is_volume and len(q.split())==1;q.export(p);assert t.load(p).is_volume
old=t.load('outputs/v14/hex_ship_integrated_rounded_arm.stl')
r=json.load(open('outputs/v14/geometry_checks.json'))
r['hex_ship_integrated_rounded_arm']={'dimensions_mm':q.extents.tolist(),'volume_cm3':q.volume/1000,'watertight':True,'components':1,'export_reload_verified':True}
r['geometry_checks']=checks;r['external_rounding_radii_mm']={'root':0,'beam':3,'brace':3,'end_receiver':2.5};r['compact_base']={'dimensions_mm':root.extents.tolist(),'outline':'six straight edges parallel to original hexagon','centre_mm':[0,-9,4],'previous_dimensions_mm':[36,54,8],'solid_volume_reduction_cm3':(old.volume-q.volume)/1000,'solid_volume_reduction_percent':100*(old.volume-q.volume)/old.volume}
(out/'geometry_checks.json').write_text(json.dumps(r,indent=2));print(json.dumps(r['compact_base'],indent=2))
