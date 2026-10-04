exec(open('work/render.py').read().split('draw(fig.add_subplot(131')[0].replace("A=t.load('outputs/A_hex_carrier.stl');B=t.load('outputs/B_arm_5deg_up.stl');scene=t.load('work/assembly.glb')",''))
plt.close(fig);fig=plt.figure(figsize=(14,8),facecolor='#f3f5f7')
T=np.eye(4);T[:3,:3]=[[1,0,0],[0,0,-1],[0,1,0]]
clip=t.creation.box(extents=[70,100,46]);clip.apply_translation([0,-20,23])
for i,(version,title) in enumerate([('v18','Previous · mismatched brace transition'),('v19','Revised · transition follows angled brace')]):
 m=t.load('outputs/'+version+'/hex_ship_integrated_rounded_arm.stl');m=t.boolean.intersection([m,clip],engine='manifold');m.apply_transform(T)
 draw(fig.add_subplot(1,2,i+1,projection='3d'),[m],['#56a4ac'],title,[(-38,38),(-48,3),(-73,33)],-25,-55)
fig.suptitle('Underside joint detail · rounded transition fitted to the brace',fontsize=20,y=.95)
fig.text(.5,.075,'Close-up cropped for visibility · Flat base and diagonal frame braces retained',ha='center',fontsize=12)
fig.text(.5,.035,'Geometry verified; physical fit and strength remain untested.',ha='center',fontsize=11,color='#6b5550')
plt.subplots_adjust(left=0,right=1,top=.85,bottom=.12,wspace=.02);plt.savefig('outputs/v19/brace_transition_preview.png',dpi=160,facecolor=fig.get_facecolor())
