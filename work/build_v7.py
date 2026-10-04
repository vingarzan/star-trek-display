# Reuse native-size frame functions and interior wall-fixing pattern, without exporting old plaque mount.
exec(open('work/build_v6.py').read().split('# The formerly lower-right')[0])
out=Path('outputs/v7')
# Load source plaque in full precision and reorient exactly as revision 6.
s=t.load('source_models/xxx_-_stand_sovereign_d.stl');base=t.boolean.intersection([s,box([300,300,11.4],[128,122,5.7])],engine='manifold');base.apply_translation([-133.9122,-101.9995,0]);angle=np.deg2rad(json.load(open('outputs/v6/geometry_checks.json'))['plaque']['rotation_counterclockwise_degrees']);base.apply_transform(t.transformations.rotation_matrix(angle,[0,0,1]));base.apply_translation([0,-20,0])
BACK=12.25;FRONT=BACK+5.7+.6
# Rear load path is inside original perimeter; forward clip arms can reach beyond it.
core=diff(reinforced([spine,beam([-46,-74],[46,-74],16),beam([0,48],[42,63],18)]),fixholes)
adds=[core];clip_stats=[];clip_samples=[]
for x in [-35,35]:
 # Find the exact lowest surface of the disc in this clip's width, including rim bevel.
 region=box([16,45,20],[x,-106,5]);rim=t.boolean.intersection([base,region],engine='manifold');edge=float(rim.bounds[0,1]);seat=edge-.15
 root=box([16,20,6.25],[x,-74,9.125]) # z6..12.25, overlaps core
 back=box([16,(-74)-(seat-3),4],[x,((-74)+(seat-3))/2,10.25]) # z8.25..12.25
 floor=box([16,3,FRONT+3-8.25],[x,seat-1.5,(8.25+FRONT+3)/2])
 lip=box([16,11,3],[x,seat+2.5,FRONT+1.5]) # Y seat-3..seat+8
 holder=union([root,back,floor,lip]);adds.append(holder)
 sample=union([box([16,16,4],[0,0,2]),box([16,3,13.3],[0,-6.5,6.65]),box([16,11,3],[0,-2.5,11.8])]);clip_samples.append(sample)
 contact=t.boolean.intersection([base,box([16,11,20],[x,seat+2.5,5])],engine='manifold')
 clip_stats.append({'x_mm':x,'disc_edge_min_y_mm':edge,'seat_y_mm':seat,'rim_max_z_mm':float(contact.bounds[1,2]),'nominal_front_gap_mm':.6})
# Keeper mounting extension stays ahead of the original perimeter at Z >= 8.25.
pivot=np.array([60.,90.]);arm=beam([38,62],pivot,16);arm.apply_translation([0,0,8.25]);# original beam thickness8 now z8.25..16.25
# Keep arm rear face off neighbours, and trim its front face to plaque back support plane.
arm=t.boolean.intersection([arm,box([300,300,4],[0,0,10.25])],engine='manifold')
root=box([20,20,6.25],[38,62,9.125]);boss=box([14,14,FRONT-8.25],[60,90,(8.25+FRONT)/2]);adds.extend([arm,root,boss])
holder=union(adds)
keeper_bore=cyl(1.7,40,[60,90,15]);nut=cyl(3.35,2.8,[60,90,9.55],6) # rear-loaded M3 nut
holder=diff(holder,[keeper_bore,nut])
# Keeper front is separated by 0.2 mm to rotate, standard M3 screw sets friction.
keeper=diff(box([12,38,3],[60,75,FRONT+1.7]),[cyl(1.7,20,[60,90,FRONT+2])])
# Two rounded ends are optional visually; simple rectangular tab is robust and finger-accessible.
plaque=base.copy();plaque.apply_translation([0,0,BACK])
# Verify seated and insertion positions. During insertion keeper is swung 180 degrees away.
opened=keeper.copy();opened.apply_transform(t.transformations.rotation_matrix(np.pi,[0,0,1],point=[60,90,0]))
checks={}
for dy in [0,2,5,8,10,12]:
 moved=plaque.copy();moved.apply_translation([0,dy,0]);v=abs(t.boolean.intersection([holder,moved],engine='manifold').volume);checks['lift_'+str(dy)+'mm_holder_overlap_mm3']=v
# Closed keeper only required to clear the seated plaque; open keeper for insertion sweep.
checks['closed_keeper_plaque_overlap_mm3']=abs(t.boolean.intersection([keeper,plaque],engine='manifold').volume)
checks['open_keeper_plaque_overlap_mm3']=abs(t.boolean.intersection([opened,plaque],engine='manifold').volume)
# Report before assertion so any obstruction can be corrected.
print('clip stats',clip_stats,'checks',checks,flush=True)
assert max(checks.values())<.01,checks
# Stem rotation itself stays in front of the plaque; confirm intermediate keeper positions.
for deg in [0,30,60,90,120,150,180]:
 k=keeper.copy();k.apply_transform(t.transformations.rotation_matrix(np.deg2rad(deg),[0,0,1],point=[60,90,0]));v=abs(t.boolean.intersection([k,plaque],engine='manifold').volume);assert v<.01,(deg,v)
# Save keeper flat on bed, pivot remains at its assembly XY location for simple placement.
keeper_print=keeper.copy();keeper_print.apply_translation([-60,-75,-(FRONT+.2)])
models={'hex_plaque_clip_cradle':holder,'plaque_turn_button':keeper_print,'rim_clip_fit_test':clip_samples[0]}
for name in ['hex_ship_original_size','hex_open_original_size','B_dual_socket_arm_130mm','peg_insert_1','peg_insert_2','socket_fit_test','peg_fit_7.7mm','peg_fit_7.8mm','peg_fit_7.9mm','original_joint_test_top','original_joint_test_bottom']:
 models[name]=t.load('outputs/v6/'+name+'.stl')
report={}
for name,m in models.items():
 assert m.is_watertight and m.is_winding_consistent and len(m.split())==1 and m.volume>0,name
 assert max(m.extents[:2])<=250
 m.export(out/(name+'.stl'));report[name]={'dimensions_mm':m.extents.tolist(),'watertight':True,'components':1,'volume_cm3':m.volume/1000}
# Compare ONLY the original connection slab Z 0..8 outside the inner hex.
slab=t.boolean.intersection([holder,box([300,300,8],[0,0,4])],engine='manifold');oldband=diff(frame,[clip]);newband=diff(slab,[clip]);err=abs(diff(oldband,[newband]).volume)+abs(diff(newband,[oldband]).volume);assert err<.01
report['native_connector_band_difference_mm3']=err;report['plaque_back_plane_mm']=BACK;report['clips']=clip_stats;report['clearance_checks']=checks;report['keeper_pivot_xy_mm']=pivot.tolist()
(out/'geometry_checks.json').write_text(json.dumps(report,indent=2));plaque.export('work/v7_plaque.ply');keeper.export('work/v7_keeper_closed.stl');opened.export('work/v7_keeper_open.stl')
print('all checks passed')
