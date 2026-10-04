"""Fill the original internal title-holder recess; preserve external mating slots."""
from pathlib import Path
import json
import numpy as np
import trimesh as t

def hexagon(radius):
 return t.convex.convex_hull(np.array([[radius*np.cos(a),radius*np.sin(a),z]
  for a in np.arange(6)*np.pi/3 for z in [0,8]]))
def patch():
 ring=t.boolean.difference([hexagon(105),hexagon(98.07179677)],engine='manifold')
 region=t.creation.box([9,9.5,8]);region.apply_translation([94.5,11.25,4])
 return t.boolean.intersection([ring,region],engine='manifold')
def filled(mesh):
 result=t.boolean.union([mesh,patch()],engine='manifold')
 f=result.faces;result.update_faces((f[:,0]!=f[:,1])&(f[:,1]!=f[:,2])&(f[:,0]!=f[:,2]));result.update_faces(result.unique_faces());result.remove_unreferenced_vertices()
 return result

def main():
 import matplotlib
 matplotlib.use('Agg')
 import matplotlib.pyplot as plt
 root=Path(__file__).resolve().parents[1];out=root/'outputs'
 checks=json.loads((out/'geometry_checks.json').read_text());reports={}
 before=t.load(out/'hex_empty_original_size.stl')
 for path in sorted(out.glob('hex_*.stl')):
  old=t.load(path);new=filled(old);new.export(path);new=t.load(path)
  assert new.is_volume and len(new.split())==1
  assert np.allclose(old.bounds,new.bounds,atol=.0001)
  added=t.boolean.difference([new,old],engine='manifold')
  removed=abs(t.boolean.difference([old,new],engine='manifold').volume)
  region=t.creation.box([9.1,9.6,8.2]);region.apply_translation([94.5,11.25,4])
  a=t.boolean.difference([new,region],engine='manifold');b=t.boolean.difference([old,region],engine='manifold')
  outside=abs(t.boolean.difference([a,b],engine='manifold').volume)+abs(t.boolean.difference([b,a],engine='manifold').volume)
  remaining=abs(t.boolean.difference([patch(),new],engine='manifold').volume)
  print(path.name, removed,outside,remaining,flush=True)
  assert max(removed,outside,remaining)<.01
  reports[path.stem]=dict(added_material_mm3=float(new.volume-old.volume),removed_material_mm3=float(removed),changes_outside_title_recess_mm3=float(outside),unfilled_recess_mm3=float(remaining))
  checks.setdefault(path.stem,{}).update(dimensions_mm=new.extents.tolist(),volume_cm3=float(new.volume/1000),watertight=True,components=1,export_reload_verified=True,title_notch_filled=True)
 checks['title_notch_fill']=reports
 (out/'geometry_checks.json').write_text(json.dumps(checks,indent=2)+'\n')
 after=t.load(out/'hex_empty_original_size.stl')
 fig,axes=plt.subplots(1,2,figsize=(10,6))
 for ax,m,title in zip(axes,[before,after],['Previous title-holder notch','Filled inner edge — all hexagons']):
  section=m.section(plane_origin=[0,0,2],plane_normal=[0,0,1])
  for e in section.entities:
   points=section.vertices[e.points];ax.plot(points[:,0],points[:,1],color='#416986',linewidth=2)
  ax.set(xlim=(89,101),ylim=(4,18),aspect='equal',title=title,xlabel='X (mm)',ylabel='Y (mm)')
 fig.suptitle('Upper-right frame detail · section 2 mm above the back')
 fig.tight_layout();fig.savefig(out/'filled_title_notch_preview.png',dpi=150)
 print(json.dumps(reports,indent=2))
if __name__=='__main__':main()
