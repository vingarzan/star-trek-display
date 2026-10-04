exec(open('work/render.py').read().split("draw(fig.add_subplot(131")[0].replace("A=t.load('outputs/A_hex_carrier.stl');B=t.load('outputs/B_arm_5deg_up.stl');scene=t.load('work/assembly.glb')", ""))
from matplotlib.patches import Rectangle,Circle
plt.close(fig);fig=plt.figure(figsize=(16,12),facecolor='#f3f5f7')
A=t.load('outputs/v3/A_hex_carrier_244mm.stl');base=t.load('work/decorative_base_trimmed.stl');B=t.load('outputs/v3/B_dual_socket_arm_130mm.stl');peg=t.load('work/v3_level_flight_insert.stl')
base.apply_translation([0,0,8]);B.apply_translation([0,0,19.4]);peg.apply_translation([0,0,19.4])
# Front view shows coverage rather than falsely implying the frame is unobscured.
draw(fig.add_subplot(221,projection='3d'),[A,base,B],['#319aa1','#b8c5d1','#d88b36'],'Front view · actual decorative outline\n244 mm hexagon is partly hidden',[(-145,135),(-115,155),(0,185)],90,-90)
T=np.eye(4);T[:3,:3]=[[1,0,0],[0,0,-1],[0,1,0]]
ms=[m.copy() for m in [A,base,B,peg]]
for m in ms:m.apply_transform(T)
draw(fig.add_subplot(222,projection='3d'),ms,['#319aa1','#b8c5d1','#d88b36','#319aa1'],'Assembled · current version 3 positioning\nArm placed above the highest decoration',[(-145,135),(-195,15),(-115,155)],22,-65)
# Exploded structural proposal: spacers through clearance holes in base, not just loose washers on artwork.
ae=A.copy();be=base.copy();be.apply_translation([0,0,42]);arm=B.copy();arm.apply_translation([0,0,90]);pp=peg.copy();pp.apply_translation([0,0,90]);sp=[]
for x in [-28,28]:
 for y in [-28,28]:
  o=t.creation.cylinder(radius=5,height=12.4,sections=32);i=t.creation.cylinder(radius=2.3,height=16,sections=32);c=t.boolean.difference([o,i],engine='manifold');c.apply_translation([x,y,85]);sp.append(c)
ms=[ae,be,*sp,arm,pp]
for m in ms:m.apply_transform(T)
draw(fig.add_subplot(223,projection='3d'),ms,['#319aa1','#b8c5d1',*(['#e8b841']*4),'#d88b36','#319aa1'],'Exploded proposal · yellow = four rigid spacers\nCarrier → decorative base → arm',[(-145,135),(-295,15),(-115,155)],22,-65)
ax=fig.add_subplot(224);data=np.load('work/base_surface.npz');im=ax.imshow(data['h'],origin='lower',extent=[-45,45,-45,45],cmap='cividis',vmin=5.7,vmax=11.4)
ax.add_patch(Rectangle((-40,-40),80,80,fill=False,lw=2,edgecolor='#ef8e3c'))
for x,y,h in [(-28,-28,5.7),(-28,28,5.7),(28,-28,11.4),(28,28,5.7)]:
 ax.add_patch(Circle((x,y),6,fill=False,edgecolor='white',lw=1.5));ax.plot(x,y,'+',color='white',ms=9);ax.text(x,y+9,f'{h:.1f} mm',ha='center',fontsize=10,color='white',bbox=dict(facecolor='#203442',alpha=.85,edgecolor='none',pad=2))
ax.set_title('Surface beneath the 80 × 80 mm arm flange\nBolt centres land at different heights',fontsize=13);ax.set_xlabel('mm from mounting centre');ax.set_ylabel('mm from mounting centre');cb=fig.colorbar(im,ax=ax,fraction=.035,pad=.03);cb.set_label('Base thickness (mm)')
fig.suptitle('Decorative base fit — geometry from your Sovereign STL',fontsize=21,y=.97)
fig.text(.5,.03,'Teal: wall carrier   ·   Grey: reused decorative plate   ·   Orange: arm   ·   Yellow: proposed spacers (not in v3 files)',ha='center',fontsize=12,color='#385563')
plt.subplots_adjust(left=.035,right=.97,bottom=.08,top=.90,wspace=.15,hspace=.18);plt.savefig('outputs/base_fit/base_fit_overview.png',dpi=145,facecolor=fig.get_facecolor())
