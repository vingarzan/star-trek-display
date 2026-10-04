exec(open('work/render.py').read().split('draw(fig.add_subplot(131')[0].replace("A=t.load('outputs/A_hex_carrier.stl');B=t.load('outputs/B_arm_5deg_up.stl');scene=t.load('work/assembly.glb')",''))
plt.close(fig);fig=plt.figure(figsize=(12,6),facecolor='#f3f5f7')
items=[('outputs/v28/peg_insert_6mm.stl','Previous · 10 mm square stem'),('outputs/v29/peg_insert_8mm.stl','8 mm peg · 19 mm engagement'),('outputs/v29/peg_insert_6mm.stl','6 mm peg · 10 mm engagement')]
for i,(path,title) in enumerate(items):
 m=t.load(path);draw(fig.add_subplot(1,3,i+1,projection='3d'),[m],['#56a4ac'],title,[(-11,11),(-11,11),(0,35)],20,-55)
fig.suptitle('Snug removable inserts · optional retaining bolt',fontsize=20,y=.94)
fig.text(.5,.055,'10.3 mm stems · 0.15 mm nominal bottom gap · Lead-in chamfer · Cross-bolts unchanged',ha='center',fontsize=11)
plt.subplots_adjust(left=.01,right=.99,top=.81,bottom=.13,wspace=.04);plt.savefig('outputs/v29/snug_stems_preview.png',dpi=160,facecolor=fig.get_facecolor())
