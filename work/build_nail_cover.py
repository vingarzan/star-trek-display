"""Flush snug cover for the side-braced mount's 14 x 12 x 3 mm recess."""
from pathlib import Path
import json,numpy as np,trimesh as t
from render import draw,plt
R=Path(__file__).resolve().parents[1];out=R/'outputs';y=78.93266296386719
def box(s,c):
 m=t.creation.box(s);m.apply_translation(c);return m
def union(ms):return t.boolean.union(ms,engine='manifold')
def diff(a,bs):return t.boolean.difference([a]+bs,engine='manifold')
def inter(a,b):return t.boolean.intersection([a,b],engine='manifold')
body=t.load(out/'hex_ship_integrated_rounded_arm.stl')
roof=box([13.9,11.9,.8],[0,y,7.6])
skirt=diff(box([13.9,11.9,2.25],[0,y,6.125]),[box([12.3,10.3,3],[0,y,6])])
slots=[box([2,.6,1.9],[x,y+v,5.95]) for x in [-6.55,6.55] for v in [-3.4,3.4]]
skirt=diff(skirt,slots)
nubs=[]
for sign in [-1,1]:
 pts=np.array([[sign*x,y+v,z] for x,z in [(6.85,5.35),(7.15,6.05),(6.85,6.7)] for v in [-1.5,1.5]])
 nubs.append(t.convex.convex_hull(pts))
base=union([roof,skirt]);cap=union([base]+nubs)
# Small top-edge opening permits removal without increasing the installed height.
notch=box([3,1.2,.85],[0,y-5.8,7.625]);cap=diff(cap,[notch]);base=diff(base,[notch])
assert abs(inter(base,body).volume)<.01
assert np.allclose(cap.bounds[:,2],[5,8],atol=1e-5)
head=t.creation.cylinder(radius=4.5,height=2,sections=96);head.apply_translation([0,y,6]);assert abs(inter(cap,head).volume)<.01
coupon=inter(body,box([18,16,8],[0,y,4]));coupon.apply_translation([0,-y,0])
printcap=cap.copy();printcap.apply_translation([0,-y,0]);printcap.apply_transform(t.transformations.rotation_matrix(np.pi,[1,0,0]));printcap.apply_translation([0,0,8])
checks=json.loads((out/'geometry_checks.json').read_text())
for name,m in [('nail_cover_cap',printcap),('fit_test_nail_cover',coupon)]:
 p=out/(name+'.stl');m.export(p);q=t.load(p);assert q.is_volume and len(q.split())==1
 checks[name]=dict(dimensions_mm=q.extents.tolist(),volume_cm3=float(q.volume/1000),watertight=True,components=1,export_reload_verified=True)
checks['nail_adapter']=dict(seat_height_from_wall_mm=5,recess_depth_mm=3,pocket_xy_mm=[14,12],cap_proud_of_frame_mm=0,cap_total_height_mm=3,cap_roof_thickness_mm=.8,cap_skirt_xy_mm=[13.9,11.9],head_envelope_diameter_mm=9,head_envelope_height_mm=2,cap_side_clearance_mm=.05,grip_nib_interference_each_side_mm=.15,nominal_cap_overlap_mm3=float(abs(inter(base,body).volume)),intentional_grip_overlap_mm3=float(abs(inter(cap,body).volume)),retention='slotted friction fingers; physical fit untested')
(out/'geometry_checks.json').write_text(json.dumps(checks,indent=2)+'\n')
fig=plt.figure(figsize=(12,5),facecolor='#f3f5f7')
installed=cap.copy();installed.apply_translation([0,-y,0])
draw(fig.add_subplot(121,projection='3d'),[coupon,installed],['#688ca5','#d49b48'],'Installed: cover face flush at 8 mm',[(-10,10),(-9,9),(0,10)],25,-55)
draw(fig.add_subplot(122,projection='3d'),[printcap],['#d49b48'],'Print roof-down · total height 3 mm',[(-8,8),(-7,7),(0,4)],35,-55)
fig.tight_layout();fig.savefig(out/'nail_cover_preview.png',dpi=160,bbox_inches='tight')
print(json.dumps(checks['nail_adapter'],indent=2))
