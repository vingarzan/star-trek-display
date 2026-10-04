exec(open('work/render.py').read().split("draw(fig.add_subplot(131")[0].replace("A=t.load('outputs/A_hex_carrier.stl');B=t.load('outputs/B_arm_5deg_up.stl');scene=t.load('work/assembly.glb')", ""))
plt.close(fig);fig=plt.figure(figsize=(15,9),facecolor='#f3f5f7')
A=t.load('outputs/v3/A_hex_carrier_244mm.stl');B=t.load('outputs/v3/B_dual_socket_arm_130mm.stl');B.apply_translation([0,0,8]);base=t.load('work/decorative_base_trimmed.stl');base.apply_translation([220,-320,8]);hanger=t.load('outputs/v4/plaque_hidden_hanger.stl');hanger.apply_translation([220,-300,0])
ax=fig.add_subplot(121,projection='3d');draw(ax,[A,B,hanger,base],['#319aa1','#d88b36','#e8b841','#b8c5d1'],'Front view · separate plaque, below and right\nPlacement shown is adjustable',[(-335,360),(-455,165),(0,200)],90,-90)
# Dashed envelope is explicitly illustrative because no ship mesh was supplied.
ax.plot([-300,300,300,-300,-300],[-130,-130,130,130,-130],[190]*5,color='#54788a',ls='--',lw=1.3)
ax.text(0,147,190,'Illustrative ship envelope — actual width unverified',ha='center',fontsize=8,color='#385563')
# Exploded plaque mount, independent of ship tile.
b=t.load('work/decorative_base_trimmed.stl');b.apply_translation([0,0,45]);h=t.load('outputs/v4/plaque_hidden_hanger.stl');h.apply_translation([0,20,0]);T=np.eye(4);T[:3,:3]=[[1,0,0],[0,0,-1],[0,1,0]]
for m in [b,h]:m.apply_transform(T)
draw(fig.add_subplot(122,projection='3d'),[h,b],['#e8b841','#b8c5d1'],'Plaque hanger · exploded view\nTwo M4 screws through flat areas, 80 mm apart',[(-145,135),(-65,15),(-115,155)],20,-68)
fig.suptitle('Separate the ship support from the decorative wall plaque',fontsize=21,y=.95)
fig.text(.5,.065,'Ship arm → hexagon → wall       |       Decorative base → its own hidden hanger → wall',ha='center',fontsize=12,color='#385563')
fig.text(.5,.032,'Decorative base remains vertical. Neither its position nor its hanger carries the ship.',ha='center',fontsize=11,color='#385563')
plt.subplots_adjust(left=.01,right=.99,bottom=.10,top=.85,wspace=.02);plt.savefig('outputs/v4/layout_preview.png',dpi=160,facecolor=fig.get_facecolor())
