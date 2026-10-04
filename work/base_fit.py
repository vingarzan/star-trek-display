import trimesh as t,numpy as np,json
from pathlib import Path
out=Path('outputs/base_fit')
s=t.load('source_models/xxx_-_stand_sovereign_d.stl')
b=t.creation.box([300,300,11.4]);b.apply_translation([128,122,5.7]);base=t.boolean.intersection([s,b],engine='manifold');base.apply_translation([-133.9122,-101.9995,0]);base.export('work/decorative_base_trimmed.stl')
tri=base.triangles;lo=tri[:,:,:2].min(axis=1);hi=tri[:,:,:2].max(axis=1)
def heights(x,y):
 tt=tri[(lo[:,0]<=x+1e-6)&(hi[:,0]>=x-1e-6)&(lo[:,1]<=y+1e-6)&(hi[:,1]>=y-1e-6)]
 a=tt[:,0];u=tt[:,1]-a;v=tt[:,2]-a;d=u[:,0]*v[:,1]-u[:,1]*v[:,0];ok=abs(d)>1e-9;a=a[ok];u=u[ok];v=v[ok];d=d[ok]
 w=np.c_[np.full(len(a),x)-a[:,0],np.full(len(a),y)-a[:,1]]
 p=(w[:,0]*v[:,1]-w[:,1]*v[:,0])/d;q=(u[:,0]*w[:,1]-u[:,1]*w[:,0])/d
 ok=(p>=-1e-6)&(q>=-1e-6)&(p+q<=1+1e-6)
 zz=(a[:,2]+p*u[:,2]+q*v[:,2])[ok];return sorted(set(np.round(zz,5)))
report={'base_bounds_mm':base.bounds.tolist(),'bolt_locations':[]}
for x in [-28,28]:
 for y in [-28,28]:
  values=[]
  for r in [0,3,6]:
   for a in np.linspace(0,2*np.pi,24,endpoint=False):
    h=heights(x+r*np.cos(a),y+r*np.sin(a));values.append(max(h) if h else np.nan)
  report['bolt_locations'].append({'xy':[x,y],'surface_at_centre':heights(x,y),'surface_over_12mm_bearing_diameter':[float(np.nanmin(values)),float(np.nanmax(values))]})
print(json.dumps(report,indent=2),flush=True)
# Dense front-surface map covering the flange plus its immediate surroundings.
xx=np.linspace(-45,45,121);yy=np.linspace(-45,45,121);h=np.array([[max(heights(x,y),default=np.nan) for x in xx] for y in yy]);np.savez('work/base_surface.npz',x=xx,y=yy,h=h)
report['flange_surface_height_range_mm']=[float(np.nanmin(h)),float(np.nanmax(h))]
(out/'fit_measurements.json').write_text(json.dumps(report,indent=2))
