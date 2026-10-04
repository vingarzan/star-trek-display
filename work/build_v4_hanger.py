import trimesh as t,json
from pathlib import Path
out=Path('outputs/v4')
def box(sz,c):
 m=t.creation.box(sz);m.apply_translation(c);return m
def cyl(r,h,c,n=64):
 m=t.creation.cylinder(radius=r,height=h,sections=n);m.apply_translation(c);return m
holes=[]
for x in [-40,40]:holes.extend([cyl(2.3,20,[x,0,4]),cyl(4.27,3.4,[x,0,1.65],6)])
for x in [-18,18]:holes.extend([cyl(2.3,20,[x,0,4]),cyl(4.75,4.2,[x,0,6])])
rail=t.boolean.difference([box([100,24,8],[0,0,4])]+holes,engine='manifold')
template=t.boolean.difference([box([100,24,2],[0,0,1])]+[cyl(1.25,10,[x,0,1]) for x in [-40,40]],engine='manifold')
for name,m in [('plaque_hidden_hanger',rail),('plaque_drilling_template',template)]:
 assert m.is_watertight and m.is_winding_consistent and len(m.split())==1 and m.volume>0
 m.export(out/(name+'.stl'))
print('Hanger 100 x 24 x 8 mm; base fasteners 80 mm apart; wall fixings 36 mm apart.')
