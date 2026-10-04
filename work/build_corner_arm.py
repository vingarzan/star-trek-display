"""Add a corner-braced alternative, preserving the current arm and mounting interfaces."""
from pathlib import Path
import json
import numpy as np
import trimesh as t
from render import draw, plt
ROOT=Path(__file__).resolve().parents[1]
out=ROOT/'outputs'
def box(size, centre):
 m=t.creation.box(size);m.apply_translation(centre);return m
def hexagon(r,z0,z1):
 return t.convex.convex_hull(np.array([[r*np.cos(a),r*np.sin(a),z] for a in np.arange(6)*np.pi/3 for z in [z0,z1]]))
def diff(a,b):return t.boolean.difference([a,b],engine='manifold')
def intersect(a,b):return t.boolean.intersection([a,b],engine='manifold')
def union(ms):return t.boolean.union(ms,engine='manifold')
original=t.load(out/'hex_ship_integrated_rounded_arm.stl')
# Use the plain open frame so its original nail tab is restored exactly.
frame=t.load(out/'hex_open_original_size.stl')
root=hexagon(48,0,8)
# Retain only the arm above the frame; its footprint joins the new base at Z=8.
retained=intersect(original,box([120,120,200],[0,0,107.99]))
retained=diff(retained,diff(box([120,120,8],[0,0,4]),root))
ribs=[]
for angle in [0,60,120]:
 m=box([220,12,8],[0,0,4]);m.apply_transform(t.transformations.rotation_matrix(np.deg2rad(angle),[0,0,1]));ribs.append(m)
ribs=intersect(union(ribs),hexagon(100,0,8))
model=union([frame,root,retained,ribs])
path=out/'hex_ship_corner_braced_arm.stl';model.export(path)
model=t.load(path)
f=model.faces;model.update_faces((f[:,0]!=f[:,1])&(f[:,1]!=f[:,2])&(f[:,0]!=f[:,2]));model.update_faces(model.unique_faces());model.remove_unreferenced_vertices();model.export(path)
model=t.load(path);assert model.is_volume and len(model.split())==1
# Verify sockets, root fillets, and every feature above the flat frame are identical.
upper=box([400,400,200],[0,0,108.0001])
def error(a,b):return float(abs(diff(a,b).volume)+abs(diff(b,a).volume))
upper_error=error(intersect(model,upper),intersect(original,upper));assert upper_error<.001
border_error=error(diff(model,hexagon(100,-1,200)),diff(original,hexagon(100,-1,200)));assert border_error<.001
nail_window=box([30,35,12],[0,80,4])
nail_error=error(intersect(model,nail_window),intersect(frame,nail_window));assert nail_error<.001
assert np.allclose(model.bounds,original.bounds,atol=.0001)
# All of the rounded arm footprint must be supported by the centred base.
foot=intersect(retained,box([120,120,.02],[0,0,8]))
unsupported=abs(diff(foot,hexagon(48,7.9,8.1)).volume)
assert unsupported<.001
# Confirm the former upper brace is clear between base and nail tab.
clearance=intersect(model,box([12,22,8],[0,57,4]))
assert abs(clearance.volume)<.001
checks=json.loads((out/'geometry_checks.json').read_text())
checks['hex_ship_corner_braced_arm']=dict(dimensions_mm=model.extents.tolist(),volume_cm3=float(model.volume/1000),watertight=True,components=1,export_reload_verified=True,brace_width_mm=12,brace_thickness_mm=8,diametric_brace_angles_degrees=[0,60,120],upper_nail_support_retained=False,central_hex_width_mm=96,central_hex_height_mm=float(96*np.cos(np.pi/6)),central_hex_centre_mm=[0,0],nail_holder_matches="hex_open_original_size.stl",arm_above_frame_difference_mm3=upper_error,outer_border_difference_mm3=border_error,nail_mount_difference_mm3=nail_error,unsupported_arm_footprint_mm3=float(unsupported),former_vertical_brace_volume_mm3=float(abs(clearance.volume)))
(out/'geometry_checks.json').write_text(json.dumps(checks,indent=2)+'\n')
fig=plt.figure(figsize=(14,7),facecolor='#f3f5f7')
draw(fig.add_subplot(121,projection='3d'),[model],['#688ca5'],'Corner-to-corner braces — front view',[(-112,112),(-100,100),(0,175)],elev=90,azim=-90)
draw(fig.add_subplot(122,projection='3d'),[model],['#688ca5'],'Integrated arm — angled view',[(-112,112),(-100,100),(0,175)],elev=30,azim=-55)
fig.tight_layout();fig.savefig(out/'corner_braced_arm_preview.png',dpi=140,bbox_inches='tight',pad_inches=.2)
print(json.dumps(checks['hex_ship_corner_braced_arm'],indent=2))
