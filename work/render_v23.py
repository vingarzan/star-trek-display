exec(open('work/render.py').read().split('draw(fig.add_subplot(131')[0].replace("A=t.load('outputs/A_hex_carrier.stl');B=t.load('outputs/B_arm_5deg_up.stl');scene=t.load('work/assembly.glb')",''))
plt.close(fig);fig=plt.figure(figsize=(12,6),facecolor='#f3f5f7')
clip=t.creation.box(extents=[34,34,12]);clip.apply_translation([0,79,4])
for i,(withcap,title) in enumerate([(False,'Recessed seat · cap removed'),(True,'Removable cap · fastener hidden')]):
 m=t.load('outputs/v23/hex_ship_integrated_rounded_arm.stl');m=t.boolean.intersection([m,clip],engine='manifold');m.apply_translation([0,-79,0]);meshes=[m];colors=['#56a4ac']
 if withcap:
  cap=t.load('work/v23_cap_installed.stl');cap.apply_translation([0,-79,0]);meshes.append(cap);colors.append('#d7dfe1')
 draw(fig.add_subplot(1,2,i+1,projection='3d'),meshes,colors,title,[(-19,19),(-19,19),(-1,12)],50,-70)
fig.suptitle('Recessed nail adapter with removable cover',fontsize=20,y=.94)
fig.text(.5,.055,'Original 5 mm seat height restored · Cap stands 2.4 mm above frame · Fit-test piece included',ha='center',fontsize=12)
plt.subplots_adjust(left=0,right=1,top=.8,bottom=.13,wspace=.03);plt.savefig('outputs/v23/nail_cap_preview.png',dpi=160,facecolor=fig.get_facecolor())
