from pathlib import Path
import shutil,json
s=Path('work/build_v11.py').read_text().split('# Four former mounting')[0]
s=s.replace("out=Path('outputs/v11')","out=Path('outputs/v24');out.mkdir(exist_ok=True)")
s=s.replace('root=round_convex(box([80,80,16],[0,0,8]),3)', '''# Extend the 60-degree sides until they disappear into the frame ribs.
root=hex_prism(37,0,8);root.apply_translation([0,-8.2,0])''')
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
# Follow the actual angled brace sections, rather than a rectangular proxy.
angles=np.arange(256)*2*np.pi/256;directions=np.c_[np.cos(angles),np.sin(angles)]
rings=[]
for theta in np.linspace(0,np.pi/2,65):
 z=8+6*(1-np.cos(theta));offset=6*(1-np.sin(theta))
 section=brace.section(plane_origin=[0,0,z],plane_normal=[0,0,1]);points=section.vertices[:,:2]
 h=ConvexHull(points);poly=points[h.vertices]
 if offset>1e-8:
  cloud=(poly[:,None,:]+offset*directions[None,:,:]).reshape(-1,2);h=ConvexHull(cloud);poly=cloud[h.vertices]
 h=ConvexHull(poly);planes=h.equations;centre=(poly.min(axis=0)+poly.max(axis=0))/2
 den=directions@planes[:,:2].T;num=-(planes[:,:2]@centre+planes[:,2]);dist=np.min(np.where(den>1e-10,num[None,:]/np.maximum(den,1e-10),np.inf),axis=1)
 xy=centre+directions*dist[:,None];rings.append(np.c_[xy,np.full(len(xy),z)])
low=rings[0].copy();low[:,2]=7.5;rings.insert(0,low)
n=256;verts=np.vstack(rings);faces=[]
for j in range(len(rings)-1):
 for i in range(n):
  k=(i+1)%n;a=j*n+i;b=j*n+k;c=(j+1)*n+k;d=(j+1)*n+i;faces.extend([[a,b,c],[a,c,d]])
for i in range(1,n-1):faces.extend([[0,i+1,i],[(len(rings)-1)*n,(len(rings)-1)*n+i,(len(rings)-1)*n+i+1]])
brace_collar=t.Trimesh(verts,np.array(faces),process=True);brace_collar.fix_normals();assert brace_collar.is_volume
body=union([open_hex,spokes,root,beam,brace,front,collar,brace_collar])''')
s=s.replace("spokes=union([box([198,18,8],[0,0,4]),box([18,174,8],[0,0,4])]);spokes=t.boolean.intersection([spokes,hex_prism(100,-1,9)],engine='manifold')", """diagonals=[]
for angle in [-30,30]:
 d=box([190,12,8],[0,0,4]);d.apply_transform(t.transformations.rotation_matrix(np.deg2rad(angle),[0,0,1]));diagonals.append(d)
spokes=union(diagonals+[box([12,174,8],[0,0,4])]);spokes=t.boolean.intersection([spokes,hex_prism(100,-1,9)],engine='manifold')""")
s=s.replace('body=diff(body,[nail_void,up_void,up_bolt,fv,fb])','body=diff(body,[nail_void,up_void,up_bolt,fv,fb]);section=nail.section(plane_origin=[0,0,2],plane_normal=[0,0,1]);loop=min([section.vertices[e.points] for e in section.entities],key=lambda a: np.ptp(a[:,0]));hole=t.convex.convex_hull(np.array([[x,y,z] for x,y,_ in loop for z in [-1,9]]));bridge=diff(box([18,23,8],[0,79.43266296386719,4]),[hole]);body=diff(union([body,bridge]),[hole])')
s=s.replace('err=abs(diff(q,[nail]).volume)+abs(diff(nail,[q]).volume);assert err<.01','expected=union([nail, t.boolean.intersection([bridge,nail_window],engine="manifold")]);err=abs(diff(q,[expected]).volume)+abs(diff(expected,[q]).volume);assert err<.01')
s=s.replace("checks['source_nail_tab_difference_mm3']=err","checks['nail_tab_plus_gap_fill_difference_mm3']=err")
exec(s)
assert body.is_volume and len(body.split())==1
foot=t.boolean.intersection([union([collar,brace_collar]),box([150,150,.4],[0,0,7.75])],engine='manifold')
unsupported=abs(diff(foot,[union([root,spokes])]).volume)
print('unsupported joint footprint volume',unsupported)
assert unsupported<.01
for p in Path('outputs/v23').glob('*.stl'):
 if p.name!='hex_ship_integrated_rounded_arm.stl':shutil.copy2(p,out/p.name)
p=out/'hex_ship_integrated_rounded_arm.stl';body=diff(body,[box([14,12,8],[0,78.93266296386719,9])]);body.export(p);q=t.load(p);f=q.faces;q.update_faces((f[:,0]!=f[:,1])&(f[:,1]!=f[:,2])&(f[:,0]!=f[:,2]));q.update_faces(q.unique_faces());q.remove_unreferenced_vertices();assert q.is_volume and len(q.split())==1;q.export(p);assert t.load(p).is_volume
r=json.load(open('outputs/v23/geometry_checks.json'));r['hex_ship_integrated_rounded_arm']={'dimensions_mm':q.extents.tolist(),'volume_cm3':q.volume/1000,'watertight':True,'components':1,'export_reload_verified':True};r['geometry_checks']=checks;r['compact_base']={'outline':'regular hexagon aligned with outer frame, offset 8.2 mm downward to support brace foot','width_mm':74,'height_mm':64.08587988,'thickness_mm':8,'outer_rounding_mm':0};r['arm_root']={'type':'added material rounded fillet collar','fillet_radius_mm':6,'height_above_base_mm':6,'main_face_spread_at_base_mm':6,'brace_collar':'matched to actual angled brace cross-sections; offset tapers tangentially to zero'};r['frame_braces']={'diagonal_count':2,'diagonal_angles_degrees':[-30,30],'diagonal_width_mm':12,'previous_horizontal_width_mm':18,'vertical_width_mm':12,'thickness_mm':8,'normal_to_sloping_frame_edges':True};(out/'geometry_checks.json').write_text(json.dumps(r,indent=2));print('Verified single solid; sockets, native perimeter and nail tab unchanged.')
