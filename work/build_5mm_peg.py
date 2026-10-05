import trimesh as t,numpy as np,json,shutil
from pathlib import Path
import argparse
parser=argparse.ArgumentParser();parser.add_argument('--shaft-length',type=float,default=8.0);args=parser.parse_args()
assert args.shaft_length>0
out=Path(__file__).resolve().parents[1]/'outputs'
def box(s,c):
 m=t.creation.box(s);m.apply_translation(c);return m
def cyl(r,h,c):
 m=t.creation.cylinder(radius=r,height=h,sections=128);m.apply_translation(c);return m
def union(ms):return t.boolean.union(ms,engine='manifold')
def diff(m,cs):return t.boolean.difference([m]+cs,engine='manifold')
body=t.load(out/'hex_ship_integrated_rounded_arm.stl');checks={};report=json.loads((out/'geometry_checks.json').read_text())
for diam,length,height in [(5,args.shaft_length,2)]:
 z0=12.05;shaft_start=z0+height;r=diam/2;spread=5.15-r
 # Quarter-ellipse profile, tangent to horizontal stem shoulder and vertical shaft.
 theta=np.linspace(0,np.pi/2,97)
 curve=np.c_[r+spread*(1-np.sin(theta)),z0+height*(1-np.cos(theta))]
 profile=np.vstack([[0,z0-.1],[5.15,z0-.1],curve,[0,shaft_start],[0,z0-.1]])
 fillet=t.creation.revolve(profile,sections=192)
 stem=union([box([10.3,10.3,z0-.35],[0,0,(z0+.35)/2]),t.convex.convex_hull(np.array([[x,y,0] for x in [-4.75,4.75] for y in [-4.75,4.75]]+[[x,y,.4] for x in [-5.15,5.15] for y in [-5.15,5.15]]))]);shaft=cyl(r,length+.1,[0,0,shaft_start-.05+length/2]);holes=[]
 for axis in [[1,0,0],[0,1,0]]:
  h=cyl(1.7,20,[0,0,0]);h.apply_transform(t.geometry.align_vectors([0,0,1],axis));h.apply_translation([0,0,6.25]);holes.append(h)
 peg=diff(union([stem,fillet,shaft]),holes)
 p=out/f'peg_insert_{diam}mm.stl';peg.export(p);q=t.load(p);f=q.faces;q.update_faces((f[:,0]!=f[:,1])&(f[:,1]!=f[:,2])&(f[:,0]!=f[:,2]));q.update_faces(q.unique_faces());q.remove_unreferenced_vertices();assert q.is_volume and len(q.split())==1;q.export(p)
 up=q.copy();up.apply_transform(t.transformations.rotation_matrix(-np.pi/2,[1,0,0]));up.apply_translation([0,1.95,138])
 front=q.copy();front.apply_translation([0,0,153.95]);front.apply_transform(t.transformations.rotation_matrix(np.deg2rad(-5),[1,0,0],point=[0,0,150]))
 for label,m in [('upward',up),('outward',front)]:checks[f'{diam}mm_{label}_overlap_mm3']=abs(t.boolean.intersection([body,m],engine='manifold').volume)
 report[p.stem]={'dimensions_mm':q.extents.tolist(),'volume_cm3':q.volume/1000,'watertight':True,'components':1,'export_reload_verified':True,'round_shaft_length_mm':length,'transition_height_mm':height,'transition_profile':'quarter ellipse, revolved','radial_spread_mm':spread}
# Check the new insert against each currently supplied arm socket.
for name in ['hex_ship_corner_braced_arm','hex_ship_corner_braced_light_arm']:
 arm=t.load(out/(name+'.stl'))
 for lift in [0,.15,1,4,8,13]:
  probe=up.copy();probe.apply_translation([0,lift,0])
  checks[name+'_upward_lift_'+str(lift)+'_overlap_mm3']=float(abs(t.boolean.intersection([arm,probe],engine='manifold').volume))
 if name=='hex_ship_corner_braced_arm':
  checks[name+'_outward_overlap_mm3']=float(abs(t.boolean.intersection([arm,front],engine='manifold').volume))
assert max(checks.values())<.01
report['peg_5mm_fit_checks']=checks
(out/'geometry_checks.json').write_text(json.dumps(report,indent=2)+'\n')
print(checks)

# Simple shaft-only gauge, using the same nominal diameter and engagement length.
coupon=union([box([12,12,2],[0,0,1]),cyl(2.5,args.shaft_length+.1,[0,0,1.95+args.shaft_length/2])])
coupon.export(out/'fit_test_peg_5.0mm.stl');assert t.load(out/'fit_test_peg_5.0mm.stl').is_volume
from render import draw,plt
fig=plt.figure(figsize=(10,5),facecolor='#f3f5f7')
draw(fig.add_subplot(121,projection='3d'),[q],['#688ca5'],'5 mm peg · 8 mm shaft',[(-7,7),(-7,7),(0,24)],25,-55)
draw(fig.add_subplot(122,projection='3d'),[coupon],['#d49b48'],'5 mm diameter fit test',[(-7,7),(-7,7),(0,12)],30,-55)
fig.tight_layout();fig.savefig(out/'peg_5mm_preview.png',dpi=150,bbox_inches='tight')
