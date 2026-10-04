exec(open('work/build_v10.py').read().split('parts=[open_hex]')[0])
import shutil
out=Path('outputs/v12');out.mkdir(exist_ok=True)
base.apply_translation([0,-4.5,0])
parts=[open_hex];stats=[]
for x in [-45.5,45.5]:
 rim=t.boolean.intersection([base,box([12,45,20],[x,-84,5])],engine='manifold');edge=float(rim.bounds[0,1]);seat=edge-.15
 root=box([12,5.5,2],[x,-87.55,7])
 floor=box([12,3,FRONT+3-6],[x,seat-1.5,(6+FRONT+3)/2])
 lip=box([12,6,3],[x,seat,FRONT+1.5])
 cradle=t.boolean.intersection([union([root,floor,lip]),outline],engine='manifold');parts.append(cradle)
 stats.append({'x_mm':x,'seat_y_mm':seat,'bottom_y_mm':seat-3})
holder=union(parts);plaque=base.copy();plaque.apply_translation([0,0,BACK]);checks={}
for dy in [0,2,5,8,10,12]:
 p=plaque.copy();p.apply_translation([0,dy,0]);checks['lift_'+str(dy)]=abs(t.boolean.intersection([holder,p],engine='manifold').volume)
for dz in [0,2,5,10,20]:
 p=plaque.copy();p.apply_translation([0,10,dz]);checks['approach_'+str(dz)]=abs(t.boolean.intersection([holder,p],engine='manifold').volume)
print(stats,checks);assert max(checks.values())<.01
outside=abs(diff(diff(holder,[open_hex]),[outline]).volume);assert outside<.01
assert holder.is_volume and len(holder.split())==1
for p in Path('outputs/v11').glob('*.stl'):shutil.copy2(p,out/p.name)
holder.export(out/'hex_plaque_flush_clips.stl');q=t.load(out/'hex_plaque_flush_clips.stl')
f=q.faces;q.update_faces((f[:,0]!=f[:,1])&(f[:,1]!=f[:,2])&(f[:,0]!=f[:,2]));q.update_faces(q.unique_faces());q.remove_unreferenced_vertices();assert q.is_volume;q.export(out/'hex_plaque_flush_clips.stl');assert t.load(out/'hex_plaque_flush_clips.stl').is_volume
plaque.export('work/v12_plaque.ply')
r=json.load(open('outputs/v11/geometry_checks.json'));r['hex_plaque_flush_clips']={'dimensions_mm':q.extents.tolist(),'volume_cm3':q.volume/1000,'watertight':True,'components':1,'export_reload_verified':True};r['plaque_corner_clips']={'clips':stats,'outside_hex_mm3':outside,'clearance_checks_mm3':checks,'back_plane_mm':8}
(out/'geometry_checks.json').write_text(json.dumps(r,indent=2))
