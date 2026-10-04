exec(open('work/render.py').read().split('draw(fig.add_subplot(131')[0].replace("A=t.load('outputs/A_hex_carrier.stl');B=t.load('outputs/B_arm_5deg_up.stl');scene=t.load('work/assembly.glb')",''))
plt.close(fig);fig=plt.figure(figsize=(12,6),facecolor='#f3f5f7')
clip=t.creation.box(extents=[34,34,12]);clip.apply_translation([0,79,4])
for i,(v,title) in enumerate([('v20','Previous · recess behind nail tab'),('v21','Revised · solid through full frame thickness')]):
 m=t.load('outputs/'+v+'/hex_ship_integrated_rounded_arm.stl');m=t.boolean.intersection([m,clip],engine='manifold');m.apply_translation([0,-79,0])
 draw(fig.add_subplot(1,2,i+1,projection='3d'),[m],['#56a4ac'],title,[(-19,19),(-19,19),(-1,12)],50,-70)
fig.suptitle('Nail adapter detail · all surrounding gaps filled',fontsize=20,y=.94)
fig.text(.5,.055,'Original nail-hole outline retained and extended through the full 8 mm thickness',ha='center',fontsize=12)
plt.subplots_adjust(left=0,right=1,top=.8,bottom=.13,wspace=.03);plt.savefig('outputs/v21/nail_adapter_preview.png',dpi=160,facecolor=fig.get_facecolor())
