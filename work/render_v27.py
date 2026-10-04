exec(open('work/render.py').read().split('draw(fig.add_subplot(131')[0].replace("A=t.load('outputs/A_hex_carrier.stl');B=t.load('outputs/B_arm_5deg_up.stl');scene=t.load('work/assembly.glb')",''))
plt.close(fig);fig=plt.figure(figsize=(12,6),facecolor='#f3f5f7')
items=[('outputs/v26/peg_insert_6mm.stl','Previous 6 mm · 5 mm straight taper'),('outputs/v27/peg_insert_8mm.stl','8 mm peg · 19 mm engagement'),('outputs/v27/peg_insert_6mm.stl','6 mm peg · 11 mm engagement')]
for i,(path,title) in enumerate(items):
 m=t.load(path);draw(fig.add_subplot(1,3,i+1,projection='3d'),[m],['#56a4ac'],title,[(-11,11),(-11,11),(0,35)],20,-55)
fig.suptitle('Curved peg transitions · shorter 6 mm peg shoulder',fontsize=20,y=.94)
fig.text(.5,.055,'8 mm peg: 3 mm curved transition · 6 mm peg: 2 mm radius fillet · Cross-bolts unchanged',ha='center',fontsize=11)
plt.subplots_adjust(left=.01,right=.99,top=.81,bottom=.13,wspace=.04);plt.savefig('outputs/v27/rounded_pegs_preview.png',dpi=160,facecolor=fig.get_facecolor())
