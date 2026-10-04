import trimesh as t,numpy as np,json
s=t.load('source_models/xxx_-_stand_sovereign_d.stl');cut=t.creation.box([300,300,11.4]);cut.apply_translation([128,122,5.7]);m=t.boolean.intersection([s,cut],engine='manifold');m.apply_translation([-133.9122,-101.9995,0]);a=json.load(open('outputs/v6/geometry_checks.json'))['plaque']['rotation_counterclockwise_degrees'];m.apply_transform(t.transformations.rotation_matrix(np.deg2rad(a),[0,0,1]));m.apply_translation([0,-20,0]);tri=m.triangles
# Intersection coordinate on Y line, given X and Z.
def ray_y(x,z):
 a=tri[:,0];u=tri[:,1]-a;v=tri[:,2]-a;d=u[:,0]*v[:,2]-u[:,2]*v[:,0];ok=abs(d)>1e-10;a=a[ok];u=u[ok];v=v[ok];d=d[ok];dx=x-a[:,0];dz=z-a[:,2];p=(dx*v[:,2]-dz*v[:,0])/d;q=(u[:,0]*dz-u[:,2]*dx)/d;ok=(p>=-1e-7)&(q>=-1e-7)&(p+q<=1+1e-7);yy=(a[:,1]+p*u[:,1]+q*v[:,1])[ok];return [float(min(yy)),float(max(yy))] if len(yy) else []
for x in [-50,-45,-40,-35,-30,-25,25,30,35,40,45,50,60,65,70]:
 print(x,{str(z):ray_y(x,z) for z in [1,5,6,7,10]},flush=True)
m.export('work/plaque_local_for_clips.ply')
