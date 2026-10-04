exec(open('work/build_v10.py').read().split('parts=[open_hex]')[0])
import shutil
out=Path('outputs/v13');out.mkdir(exist_ok=True)
base.apply_translation([0,-4.5,0])
rim=t.boolean.intersection([base,box([6,45,20],[48,-84,5])],engine='manifold');shift=-87.28-float(rim.bounds[0,1]);base.apply_translation([0,shift,0]);plaque=base.copy();plaque.apply_translation([0,0,8]);print('additional plaque shift',shift)
parts=[open_hex];stats=[]
# Keep the previous seats and inner contact edges; narrow the outer edges 3 mm.
for x,seat in [(-48,-87.43),(48,-87.43)]:
 root=box([6,5.5,2],[x,-87.55,7]);floor=box([6,3,11.3],[x,seat-1.5,11.65]);lip=box([4.2,6,3],[np.sign(x)*47.1,seat,15.8])
 parts.append(t.boolean.intersection([union([root,floor,lip]),outline],engine="manifold"));stats.append({'x':x,'width':6,'seat_y':seat})
# Upper right swivel keeper: M3 screw in a pilot hole, below a rounded lever.
px,py=51,88.3
holder=diff(union(parts),[cyl(1.3,7,[px,py,4.5])])
boss=cyl(2.5,6.6,[px,py,11.3])
keeper=union([boss,cyl(2.5,3,[px,py,16.1]),box([5,10,3],[px,py-5,16.1]),cyl(2.5,3,[px,py-10,16.1])]);keeper=diff(keeper,[cyl(1.7,20,[px,py,10])])
assert abs(diff(diff(holder,[open_hex]),[outline]).volume)<.01
assert abs(diff(keeper,[outline]).volume)<.01
checks={}
for label,m in [('holder',holder),('closed_latch',keeper)]:
 checks[label+'_seated_overlap_mm3']=abs(t.boolean.intersection([m,plaque],engine='manifold').volume)
assert max(checks.values())<.01,checks
# Remove the keeper straight forward after unscrewing, then lift plaque.
for dz in [0,1,3,6,10,20]:
 k=keeper.copy();k.apply_translation([0,0,dz]);checks['keeper_removal_'+str(dz)]=abs(t.boolean.intersection([k,plaque],engine='manifold').volume)
for dy in [0,1,2,3,4,5,8,10]:
 p=plaque.copy();p.apply_translation([0,dy,0]);checks['released_lift_'+str(dy)]=abs(t.boolean.intersection([holder,p],engine='manifold').volume)
assert max(checks.values())<.01,checks
for p in Path('outputs/v12').glob('*.stl'):
 if p.name!='hex_plaque_flush_clips.stl':shutil.copy2(p,out/p.name)
kp=keeper.copy();kp.apply_translation([-px,-py,-8])
for name,m in [('hex_plaque_flush_clips',holder),('plaque_upper_right_latch',kp)]:
 m.export(out/(name+'.stl'));q=t.load(out/(name+'.stl'));f=q.faces;q.update_faces((f[:,0]!=f[:,1])&(f[:,1]!=f[:,2])&(f[:,0]!=f[:,2]));q.update_faces(q.unique_faces());q.remove_unreferenced_vertices();assert q.is_volume and len(q.split())==1;q.export(out/(name+'.stl'));assert t.load(out/(name+'.stl')).is_volume
keeper.export('work/v13_latch.stl');plaque.export('work/v13_plaque.ply')
r=json.load(open('outputs/v12/geometry_checks.json'));r['plaque_corner_clips']={'clips':stats,'back_plane_mm':8};r['plaque_latch']={'pivot_xy':[px,py],'screw':'M3 x 16, 2.6 mm printed pilot in hex frame','clearance_checks':checks,'closed_inside_outline':True,'release':'unscrew and remove keeper forward; then lift plaque'}
for name in ['hex_plaque_flush_clips','plaque_upper_right_latch']:
 q=t.load(out/(name+'.stl'));r[name]={'dimensions_mm':q.extents.tolist(),'volume_cm3':q.volume/1000,'export_reload_verified':True,'watertight':True,'components':1}
(out/'geometry_checks.json').write_text(json.dumps(r,indent=2));print(checks)
