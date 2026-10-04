import trimesh as t,numpy as np,json
from pathlib import Path
out=Path('outputs/v9')
def box(sz,c):
 m=t.creation.box(sz);m.apply_translation(c);return m
def cyl(r,h,c,n=64):
 m=t.creation.cylinder(radius=r,height=h,sections=n);m.apply_translation(c);return m
def union(ms):return t.boolean.union(ms,engine='manifold')
def diff(a,bs):return t.boolean.difference([a]+bs,engine='manifold')
def hex_prism(radius,z0=-1,z1=30):
 return t.convex.convex_hull(np.array([[radius*np.cos(a),radius*np.sin(a),z] for a in np.arange(6)*np.pi/3 for z in [z0,z1]]))
# Use exactly the WITH-NAIL STL, removing the complete original diagonal arm/spoke.
src=t.load('source_models/obj_2_Inclined display with nail.stl');native=sorted(src.split(),key=lambda m:m.extents[2])[0];native.apply_translation([-435.20001220703125,-126,0])
inside=hex_prism(98.07179677,-1,9)
ring=diff(native,[inside]);nail=t.boolean.intersection([native,box([14,23,12],[0,79.5,4])],engine='manifold');open_hex=union([ring,nail])
outline=hex_prism(105,-1,40)
# Raised plaque, unchanged from revision 8.
s=t.load('source_models/xxx_-_stand_sovereign_d.stl');base=t.boolean.intersection([s,box([300,300,11.4],[128,122,5.7])],engine='manifold');base.apply_translation([-133.9122,-101.9995,0]);a=json.load(open('outputs/v6/geometry_checks.json'))['plaque']['rotation_counterclockwise_degrees'];base.apply_transform(t.transformations.rotation_matrix(np.deg2rad(a),[0,0,1]));base.apply_translation([0,2,0])
BACK=12.25;FRONT=18.55
parts=[open_hex];stats=[]
for x in [-35,35]:
 rim=t.boolean.intersection([base,box([16,45,20],[x,-84,5])],engine='manifold');edge=float(rim.bounds[0,1]);seat=edge-.15
 # Compact root sits ON the bottom perimeter bar, without an interior crossbar.
 root=box([16,5.5,6.25],[x,-87.55,9.125]) # X 27..43, Y -90.3..-84.8, Z6..12.25
 rear=box([16,10.3,4],[x,seat+2.15,10.25])
 floor=box([16,3,FRONT+3-8.25],[x,seat-1.5,(8.25+FRONT+3)/2])
 lip=box([16,11,3],[x,seat+2.5,FRONT+1.5])
 cradle=union([root,rear,floor,lip]);parts.append(cradle)
 stats.append({'x_mm':x,'seat_y_mm':seat,'bottom_y_mm':seat-3})
# A small removable side keeper uses the spare space between disc rim and right hex point.
# It is lifted off after loosening/removing an M2 screw, rather than rotated outside the boundary.
px=101.5
post=cyl(2.3,FRONT-7.8,[px,0,(FRONT+7.8)/2]);parts.append(post)
holder=diff(union(parts),[cyl(1.15,40,[px,0,15]),cyl(2.43,2.0,[px,0,.95],6)])
keeper=diff(box([13.5,4,2.5],[96.75,0,19.95]),[cyl(1.15,20,[px,0,20])]) # X90..103.5, bottom18.7
# Closed keeper is wholly inside the same hex outline; removal is by lifting it off.
assert abs(diff(keeper,[outline]).volume)<.01
# No new clip material is allowed beyond the native main hex boundary (original edge tabs excepted).
new_bits=diff(holder,[open_hex]);outside=abs(diff(new_bits,[outline]).volume);assert outside<.01,outside
# Ship mount still needs structural spokes, but now uses the same original nail-tab geometry.
inner_reinforcement=union([box([80,80,8],[0,0,4]),box([198,18,8],[0,0,4]),box([18,174,8],[0,0,4])]);inner_reinforcement=t.boolean.intersection([inner_reinforcement,hex_prism(100,-1,9)],engine='manifold')
# Preserve original nail aperture by cutting its empty volume through any added support.
nail_window=box([14,23,12],[0,79.5,4]);nail_void=diff(nail_window,[native])
ship=union([open_hex,inner_reinforcement]);cuts=[nail_void]
for x in [-28,28]:
 for y in [-28,28]:cuts.extend([cyl(2.3,20,[x,y,4]),cyl(4.27,3.4,[x,y,1.65],6)])
ship=diff(ship,cuts)
plaque=base.copy();plaque.apply_translation([0,0,BACK]);checks={}
for dy in [0,2,5,8,10,12]:
 p=plaque.copy();p.apply_translation([0,dy,0]);v=abs(t.boolean.intersection([holder,p],engine='manifold').volume);checks['lift_'+str(dy)+'mm_overlap_mm3']=v
checks['seated_keeper_overlap_mm3']=abs(t.boolean.intersection([keeper,plaque],engine='manifold').volume)
for dz in [0,2,5,10,20]:
 p=plaque.copy();p.apply_translation([0,10,dz]);v=abs(t.boolean.intersection([holder,p],engine='manifold').volume);checks['approach_'+str(dz)+'mm_overlap_mm3']=v
print('clearances',checks,flush=True);assert max(checks.values())<.01
kp=keeper.copy();kp.apply_translation([-96.75,0,-18.7])
models={'hex_open_original_size':open_hex,'hex_plaque_clip_cradle':holder,'plaque_side_keeper':kp,'hex_ship_original_size':ship}
for name in ['rim_clip_fit_test','B_dual_socket_arm_130mm','peg_insert_1','peg_insert_2','socket_fit_test','peg_fit_7.7mm','peg_fit_7.8mm','peg_fit_7.9mm','original_joint_test_top','original_joint_test_bottom']:
 models[name]=t.load('outputs/v8/'+name+'.stl')
report={}
for name,m in models.items():
 assert m.is_watertight and m.is_winding_consistent and len(m.split())==1 and m.volume>0,(name,m.is_watertight,len(m.split()))
 assert max(m.extents[:2])<=250
 m.export(out/(name+'.stl'));report[name]={'dimensions_mm':m.extents.tolist(),'volume_cm3':m.volume/1000,'watertight':True,'components':1}
# Source-tab geometry comparison within its own window, including its hole.
for name,m in [('open',open_hex),('plaque',holder),('ship',ship)]:
 q=t.boolean.intersection([m,nail_window],engine='manifold');err=abs(diff(q,[nail]).volume)+abs(diff(nail,[q]).volume);assert err<.01,(name,err);report[name+'_source_nail_tab_difference_mm3']=err
# Ensure no leftover diagonal arm remains in the open frame's centre away from the original tab.
central=t.boolean.intersection([open_hex,hex_prism(97.8,-1,9)],engine='manifold');non_tab=diff(central,[nail_window]);assert abs(non_tab.volume)<.01
report['open_frame_central_material_other_than_nail_tab_mm3']=abs(non_tab.volume)
report['new_clip_material_outside_hex_outline_mm3']=outside
report['keeper_material_outside_hex_outline_mm3']=abs(diff(keeper,[outline]).volume)
report['clearance_checks']=checks;report['lower_clips']=stats;report['side_keeper_pivot_xy_mm']=[px,0]
(out/'geometry_checks.json').write_text(json.dumps(report,indent=2));plaque.export('work/v9_plaque.ply');keeper.export('work/v9_keeper.stl');nail.export('work/v9_nail_detail.stl')
print('all checks passed')
