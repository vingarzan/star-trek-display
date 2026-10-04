# Original with-nail perimeter, with the fighter-plane arm removed.
exec(open('work/build_v9.py').read().split('# Raised plaque')[0])
out=Path('outputs/v11')
from scipy.spatial import ConvexHull,HalfspaceIntersection
from scipy.optimize import linprog

def round_convex(mesh,r):
 # Erode a convex solid by r, then add a faceted sphere: round every exterior edge
 # while keeping the original envelope and broad functional flat faces.
 planes=np.unique(np.round(ConvexHull(mesh.vertices).equations,10),axis=0);planes[:,-1]+=r
 A=np.c_[planes[:,:3],np.linalg.norm(planes[:,:3],axis=1)]
 sol=linprog([0,0,0,-1],A_ub=A,b_ub=-planes[:,3],bounds=[(None,None)]*4,method='highs');assert sol.success and sol.x[3]>0
 core=HalfspaceIntersection(planes,sol.x[:3]).intersections
 sphere=t.creation.icosphere(subdivisions=3,radius=r).vertices
 return t.convex.convex_hull((core[:,None,:]+sphere[None,:,:]).reshape(-1,3))
def bore_x(c):
 b=cyl(1.7,60,[0,0,0]);b.apply_transform(t.geometry.align_vectors([0,0,1],[1,0,0]));b.apply_translation(c);return b
# Rounded integrated root spans the previous tile+flange thickness: no bolt interface remains.
root=round_convex(box([80,80,16],[0,0,8]),3)
spokes=union([box([198,18,8],[0,0,4]),box([18,174,8],[0,0,4])]);spokes=t.boolean.intersection([spokes,hex_prism(100,-1,9)],engine='manifold')
beam=round_convex(box([28,28,138],[0,0,83]),3)
brace=t.convex.convex_hull(np.array([[x,y,z+8] for x in [-7,7] for y,z in [(-35,6),(-12,6),(-12,143)]]));brace=round_convex(brace,3)
front=round_convex(box([24,24,18],[0,0,157]),2.5)
rot=t.transformations.rotation_matrix(np.deg2rad(-5),[1,0,0],point=[0,0,150]);front.apply_transform(rot)
body=union([open_hex,spokes,root,beam,brace,front])
# Reproduce source nail-tab aperture, so the vertical spoke cannot fill it.
nail_window=box([14,23,12],[0,79.5,4]);nail_void=diff(nail_window,[native])
up_void=box([10.4,16,10.4],[0,9.8,138]);up_bolt=bore_x([0,8.2,138])
fv=box([10.4,10.4,16],[0,0,161.8]);fv.apply_transform(rot)
fb=bore_x([0,0,160.2]);fb.apply_transform(rot)
body=diff(body,[nail_void,up_void,up_bolt,fv,fb])
# Reuse both existing removable peg inserts at their unchanged installed positions.
peg=t.load('outputs/v10/peg_insert_1.stl')
up=peg.copy();up.apply_transform(t.transformations.rotation_matrix(-np.pi/2,[1,0,0]));up.apply_translation([0,2.4,138])
f=peg.copy();f.apply_translation([0,0,154.4]);f.apply_transform(rot)
checks={}
for name,m in [('level_flight',up),('wall_parallel',f)]:
 v=abs(t.boolean.intersection([body,m],engine='manifold').volume);assert v<.01,(name,v);checks[name+'_insert_intersection_mm3']=v
# Source-tab and original exterior frame are unaffected.
q=t.boolean.intersection([body,nail_window],engine='manifold');err=abs(diff(q,[nail]).volume)+abs(diff(nail,[q]).volume);assert err<.01
checks['source_nail_tab_difference_mm3']=err
slab=t.boolean.intersection([body,box([300,300,8],[0,0,4])],engine='manifold');outer=diff(slab,[hex_prism(100,-1,9)]);ref=diff(open_hex,[hex_prism(100,-1,9)]);edge_err=abs(diff(outer,[ref]).volume)+abs(diff(ref,[outer]).volume);assert edge_err<.01
checks['original_outer_band_difference_mm3']=edge_err
# Four former mounting locations must now be solid through the complete joint thickness.
filled=[]
for x in [-28,28]:
 for y in [-28,28]:
  probe=cyl(1.8,14,[x,y,8]);missing=abs(diff(probe,[body]).volume);assert missing<.01;filled.append(missing)
checks['former_mounting_hole_void_mm3']=filled
models={'hex_ship_integrated_rounded_arm':body}
for name in ['hex_open_original_size','hex_plaque_flush_clips','rim_clip_fit_test','peg_insert_1','peg_insert_2','socket_fit_test','peg_fit_7.7mm','peg_fit_7.8mm','peg_fit_7.9mm','original_joint_test_top','original_joint_test_bottom']:
 models[name]=t.load('outputs/v10/'+name+'.stl')
report={}
for name,m in models.items():
 assert m.is_watertight and m.is_winding_consistent and len(m.split())==1 and m.volume>0,name
 assert max(m.extents[:2])<=250
 m.export(out/(name+'.stl'));report[name]={'dimensions_mm':m.extents.tolist(),'watertight':True,'components':1,'volume_cm3':m.volume/1000}
report['geometry_checks']=checks;report['external_rounding_radii_mm']={'root':3,'beam':3,'brace':3,'end_receiver':2.5};report['level_flight_axis_distance_from_wall_mm']=138
(out/'geometry_checks.json').write_text(json.dumps(report,indent=2));up.export('work/v11_up_insert.stl');f.export('work/v11_front_insert.stl')
# Appearance comparison with old assembled pieces, for rendering only.
old=t.load('outputs/v10/hex_ship_original_size.stl');b=t.load('outputs/v10/B_dual_socket_arm_130mm.stl');b.apply_translation([0,0,8]);t.util.concatenate([old,b]).export('work/v11_previous_arm.stl')
print(json.dumps(report['hex_ship_integrated_rounded_arm'],indent=2));print(json.dumps(checks,indent=2))
