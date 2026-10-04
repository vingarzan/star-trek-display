import trimesh as t,numpy as np,json
from pathlib import Path
out=Path('outputs/v5')
def box(size,c):
 m=t.creation.box(size);m.apply_translation(c);return m
def cyl(r,h,c,n=48):
 m=t.creation.cylinder(radius=r,height=h,sections=n);m.apply_translation(c);return m
def union(ms):return t.boolean.union(ms,engine='manifold')
def diff(a,bs):return t.boolean.difference([a]+bs,engine='manifold')
def tab(y,clear=0):
 # Dovetail is inserted from front, perpendicular to wall. Main tile pitch is 240.
 x0=119.8-clear;x1=124+clear;w0=5+clear;w1=7+clear
 pts=np.array([[x,y+dy,z] for x,w in [(x0,w0),(x1,w1)] for dy in [-w,w] for z in [-.1,8.1]])
 return t.convex.convex_hull(pts)
# Full-height connectors remain flush with the tile faces.
frame=diff(box([240,240,8],[0,0,4]),[box([220,220,20],[0,0,4])])
adds=[frame];cuts=[]
for pos in [-60,60]:
 r=tab(pos);r=t.boolean.intersection([r,box([300,300,8],[0,0,4])],engine='manifold');adds.append(r)
 top=r.copy();top.apply_transform(t.transformations.rotation_matrix(np.pi/2,[0,0,1]));adds.append(top)
 left=tab(pos,.22);left.apply_translation([-240,0,0]);cuts.append(left)
 bottom=left.copy();bottom.apply_transform(t.transformations.rotation_matrix(np.pi/2,[0,0,1]));cuts.append(bottom)
frame=diff(union(adds),cuts)
# Fixing spine: same arrangement across every tile. Keyhole entrances are below necks.
spine=box([22,230,8],[0,0,4]);frame=union([frame,spine])
fix_cuts=[]
for y in [-96,96]:
 fix_cuts.extend([cyl(4,20,[0,y-6,4]),box([3.5,6,20],[0,y-3,4]),cyl(1.75,20,[0,y,4])])
# Separate screw-compatible through holes, so nail shank size does not constrain screws.
for y in [-76,76]:fix_cuts.extend([cyl(2.3,20,[0,y,4]),cyl(4.75,4.2,[0,y,6])])
frame=diff(frame,fix_cuts)
# Ship tile: direct arm attachment with original 56 mm square bolt pattern.
ship=union([frame,box([80,80,8],[0,0,4]),box([230,22,8],[0,0,4])]);holes=[]
for x in [-28,28]:
 for y in [-28,28]:holes.extend([cyl(2.3,20,[x,y,4]),cyl(4.27,3.4,[x,y,1.65],6)])
ship=diff(ship,holes)
# Plaque tile: two structural rails. Two bolts at one selected row hold the plaque.
plaque=union([frame,box([16,230,8],[-40,0,4]),box([16,230,8],[40,0,4]),box([96,16,8],[0,0,4])]);holes=[]
for x in [-40,40]:
 for y in [-40,-20,0,20,40]:holes.extend([cyl(2.3,20,[x,y,4]),cyl(4.27,3.4,[x,y,1.65],6)])
plaque=diff(plaque,holes)
models={'tile_ship_arm':ship,'tile_plaque':plaque,'tile_open_connector':frame}
for name in ['B_dual_socket_arm_130mm','peg_insert_1','peg_insert_2','socket_fit_test','peg_fit_7.7mm','peg_fit_7.8mm','peg_fit_7.9mm']:
 models[name]=t.load('outputs/v3/'+name+'.stl')
models['plaque_drilling_template']=t.load('outputs/v4/plaque_drilling_template.stl')
# Small mating corner/edge samples from the actual final frame: one male, one female.
for label,cx in [('male',116),('female',-116)]:
 clip=box([24,34,20],[cx,60,4]);sample=t.boolean.intersection([frame,clip],engine='manifold');sample.apply_translation([-cx,-60,0]);models['tile_joint_test_'+label]=sample
report={}
for name,m in models.items():
 assert m.is_watertight and m.is_winding_consistent and m.volume>0 and len(m.split())==1,name
 assert max(m.extents[:2])<=250,(name,m.extents)
 m.export(out/(name+'.stl'));report[name]={'dimensions_mm':m.extents.tolist(),'watertight':True,'components':1,'volume_cm3':m.volume/1000}
# Prove that identical tiles mate on both axes without unintended overlap.
report['mating_checks']={}
for axis,v in [('right',[240,0,0]),('above',[0,240,0])]:
 n=frame.copy();n.apply_translation(v);inter=t.boolean.intersection([frame,n],engine='manifold');vol=abs(float(inter.volume));assert vol<.001,(axis,vol);report['mating_checks'][axis+'_intersection_mm3']=vol
report['grid_pitch_mm']=240;report['nail_keyholes']={'entry_diameter_mm':8,'neck_width_mm':3.5,'slide_mm':6,'neck_centres_xy':[[0,-96],[0,96]]}
(out/'geometry_checks.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))
