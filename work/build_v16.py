from pathlib import Path
import shutil,json
s=Path('work/build_v11.py').read_text().split('# Four former mounting')[0]
s=s.replace("out=Path('outputs/v11')","out=Path('outputs/v16');out.mkdir(exist_ok=True)")
s=s.replace('root=round_convex(box([80,80,16],[0,0,8]),3)', '''# Extend the 60-degree sides until they disappear into the frame ribs.
root=t.convex.convex_hull(np.array([[x,y,z] for x,y in [(0,-9+38*np.sqrt(3)),(38,-9),(0,-9-38*np.sqrt(3)),(-38,-9)] for z in [0,8]]))''')
s=s.replace('box([28,28,138],[0,0,83])','box([28,28,146],[0,0,79])')
s=s.replace('for y,z in [(-35,6),(-12,6),(-12,143)]','for y,z in [(-35,-2),(-12,-2),(-12,143)]')
s=s.replace('body=union([open_hex,spokes,root,beam,brace,front])','''# An added-material tapered collar replaces the inward-rounded root.
# At Z=8 it spreads 6 mm beyond each main beam face; reaches beam at Z=14.
upper=[]
for cx,cy,start in [(11,11,0),(-11,11,90),(-11,-11,180),(11,-11,270)]:
 for ang in np.linspace(start,start+90,17):
  upper.append([cx+3*np.cos(np.deg2rad(ang)),cy+3*np.sin(np.deg2rad(ang)),14])
collar=t.convex.convex_hull(np.array([[x,y,7] for x in [-21,21] for y in [-21,21]]+upper))
brace_collar=t.convex.convex_hull(np.array([[x,y,7] for x in [-14,14] for y in [-41,-5]]+[[x,y,14] for x in [-7,7] for y in [-34,-12]]))
body=union([open_hex,spokes,root,beam,brace,front,collar,brace_collar])''')
exec(s)
assert body.is_volume and len(body.split())==1
for p in Path('outputs/v15').glob('*.stl'):
 if p.name!='hex_ship_integrated_rounded_arm.stl':shutil.copy2(p,out/p.name)
p=out/'hex_ship_integrated_rounded_arm.stl';body.export(p);q=t.load(p);f=q.faces;q.update_faces((f[:,0]!=f[:,1])&(f[:,1]!=f[:,2])&(f[:,0]!=f[:,2]));q.update_faces(q.unique_faces());q.remove_unreferenced_vertices();assert q.is_volume and len(q.split())==1;q.export(p);assert t.load(p).is_volume
r=json.load(open('outputs/v15/geometry_checks.json'));r['hex_ship_integrated_rounded_arm']={'dimensions_mm':q.extents.tolist(),'volume_cm3':q.volume/1000,'watertight':True,'components':1,'export_reload_verified':True};r['geometry_checks']=checks;r['compact_base']={'outline':'extended 60 degree sides blending into horizontal and vertical ribs; no short horizontal base edges','thickness_mm':8,'outer_rounding_mm':0};r['arm_root']={'type':'added material external chamfer collar','height_above_base_mm':6,'main_face_spread_at_base_mm':6,'brace_collar':True};(out/'geometry_checks.json').write_text(json.dumps(r,indent=2));print('Verified single solid; sockets, native perimeter and nail tab unchanged.')
