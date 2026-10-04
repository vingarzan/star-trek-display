exec(open('work/render.py').read().split('draw(fig.add_subplot(131')[0].replace("A=t.load('outputs/A_hex_carrier.stl');B=t.load('outputs/B_arm_5deg_up.stl');scene=t.load('work/assembly.glb')",''))
plt.close(fig);fig=plt.figure(figsize=(14,8),facecolor='#f3f5f7')
T=np.eye(4);T[:3,:3]=[[1,0,0],[0,0,-1],[0,1,0]]
for i,(version,title) in enumerate([('v15','Previous · short base edges and rounded root'),('v16','Revised · extended slopes and outward chamfer')]):
 m=t.load('outputs/'+version+'/hex_ship_integrated_rounded_arm.stl');m.apply_transform(T)
 draw(fig.add_subplot(1,2,i+1,projection='3d'),[m],['#56a4ac'],title,[(-110,110),(-180,10),(-100,100)],24,-55)
fig.suptitle('Extended base slopes · reinforced arm junction',fontsize=21,y=.94)
fig.text(.5,.08,'Base slopes meet the ribs · 6 mm outward chamfer adds material around the arm root',ha='center',fontsize=12)
fig.text(.5,.035,'Geometry checked; revised junction has not been physically load-tested.',ha='center',fontsize=11,color='#6b5550')
plt.subplots_adjust(left=0,right=1,top=.85,bottom=.13,wspace=.02);plt.savefig('outputs/v16/extended_base_preview.png',dpi=160,facecolor=fig.get_facecolor())
