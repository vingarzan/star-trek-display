exec(open('work/render.py').read().split('draw(fig.add_subplot(131')[0].replace("A=t.load('outputs/A_hex_carrier.stl');B=t.load('outputs/B_arm_5deg_up.stl');scene=t.load('work/assembly.glb')",''))
plt.close(fig);fig=plt.figure(figsize=(14,8),facecolor='#f3f5f7')
T=np.eye(4);T[:3,:3]=[[1,0,0],[0,0,-1],[0,1,0]]
for i,(version,title) in enumerate([('v13','Previous · 80 × 80 × 16 mm base'),('v14','Revised · 36 × 54 × 8 mm base')]):
 m=t.load('outputs/'+version+'/hex_ship_integrated_rounded_arm.stl');m.apply_transform(T)
 draw(fig.add_subplot(1,2,i+1,projection='3d'),[m],['#56a4ac'],title,[(-110,110),(-180,10),(-100,100)],24,-55)
fig.suptitle('Compact base · flush with the hexagon · square corners',fontsize=21,y=.94)
fig.text(.5,.08,'24% less solid model volume overall · Original sockets, reach, connectors and nail tab preserved',ha='center',fontsize=12)
fig.text(.5,.035,'Geometry checked; revised junction has not been physically load-tested.',ha='center',fontsize=11,color='#6b5550')
plt.subplots_adjust(left=0,right=1,top=.85,bottom=.13,wspace=.02);plt.savefig('outputs/v14/compact_base_preview.png',dpi=160,facecolor=fig.get_facecolor())
