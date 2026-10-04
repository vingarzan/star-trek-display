from pathlib import Path
import shutil,json
s=Path('work/build_v11.py').read_text().split('# Four former mounting')[0]
s=s.replace("out=Path('outputs/v11')","out=Path('outputs/v17');out.mkdir(exist_ok=True)")
s=s.replace('root=round_convex(box([80,80,16],[0,0,8]),3)', '''# Extend the 60-degree sides until they disappear into the frame ribs.
root=t.convex.convex_hull(np.array([[x,y,z] for x,y in [(0,-9+38*np.sqrt(3)),(38,-9),(0,-9-38*np.sqrt(3)),(-38,-9)] for z in [0,8]]))''')
s=s.replace('box([28,28,138],[0,0,83])','box([28,28,146],[0,0,79])')
s=s.replace('for y,z in [(-35,6),(-12,6),(-12,143)]','for y,z in [(-35,-2),(-12,-2),(-12,143)]')
s=s.replace('body=union([open_hex,spokes,root,beam,brace,front])','''# An added-material tapered collar replaces the inward-rounded root.
# At Z=8 it spreads 6 mm beyond each main beam face; reaches beam at Z=14.
def rounded_root(cx,cy,hx,hy,corner,r=6):
 # Circular concave fillet: horizontal tangent at base, vertical at arm.
 rings=[]
 for theta in np.linspace(0,np.pi/2,49):
  z=8+r*(1-np.cos(theta));d=r*(1-np.sin(theta))
  ring=[]
  for ox,oy,start in [(hx,hy,0),(-hx,hy,90),(-hx,-hy,180),(hx,-hy,270)]:
   for angle in np.linspace(start,start+90,17,endpoint=False):
    a=np.deg2rad(angle);ring.append([cx+ox+(corner+d)*np.cos(a),cy+oy+(corner+d)*np.sin(a),z])
  rings.append(ring)
 # Extend below the frame front for a robust boolean overlap.
 lower=np.array(rings[0]);lower[:,2]=7.5;rings.insert(0,lower.tolist())
 n=len(rings[0]);verts=np.array(rings).reshape(-1,3);faces=[]
 for j in range(len(rings)-1):
  for i in range(n):
   k=(i+1)%n;a=j*n+i;b=j*n+k;c=(j+1)*n+k;d=(j+1)*n+i
   faces.extend([[a,b,c],[a,c,d]])
 for i in range(1,n-1):faces.extend([[0,i+1,i],[(len(rings)-1)*n,(len(rings)-1)*n+i,(len(rings)-1)*n+i+1]])
 m=t.Trimesh(verts,np.array(faces),process=True);m.fix_normals();assert m.is_volume;return m
collar=rounded_root(0,0,11,11,3)
brace_collar=rounded_root(0,-22,4,6,2.8)
body=union([open_hex,spokes,root,beam,brace,front,collar,brace_collar])''')
exec(s)
assert body.is_volume and len(body.split())==1
for p in Path('outputs/v16').glob('*.stl'):
 if p.name!='hex_ship_integrated_rounded_arm.stl':shutil.copy2(p,out/p.name)
p=out/'hex_ship_integrated_rounded_arm.stl';body.export(p);q=t.load(p);f=q.faces;q.update_faces((f[:,0]!=f[:,1])&(f[:,1]!=f[:,2])&(f[:,0]!=f[:,2]));q.update_faces(q.unique_faces());q.remove_unreferenced_vertices();assert q.is_volume and len(q.split())==1;q.export(p);assert t.load(p).is_volume
r=json.load(open('outputs/v16/geometry_checks.json'));r['hex_ship_integrated_rounded_arm']={'dimensions_mm':q.extents.tolist(),'volume_cm3':q.volume/1000,'watertight':True,'components':1,'export_reload_verified':True};r['geometry_checks']=checks;r['compact_base']={'outline':'extended 60 degree sides blending into horizontal and vertical ribs; no short horizontal base edges','thickness_mm':8,'outer_rounding_mm':0};r['arm_root']={'type':'added material rounded fillet collar','fillet_radius_mm':6,'height_above_base_mm':6,'main_face_spread_at_base_mm':6,'brace_collar':True};(out/'geometry_checks.json').write_text(json.dumps(r,indent=2));print('Verified single solid; sockets, native perimeter and nail tab unchanged.')
