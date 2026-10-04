exec(open('work/render.py').read().split("draw(fig.add_subplot(131")[0].replace("A=t.load('outputs/A_hex_carrier.stl');B=t.load('outputs/B_arm_5deg_up.stl');scene=t.load('work/assembly.glb')", ""))
plt.close(fig);fig=plt.figure(figsize=(16,10),facecolor='#f3f5f7')
ship=t.load('outputs/v5/tile_ship_arm.stl');connector=t.load('outputs/v5/tile_open_connector.stl');connector.apply_translation([0,-240,0]);plaque=t.load('outputs/v5/tile_plaque.stl');plaque.apply_translation([240,-240,0]);base=t.load('work/decorative_base_trimmed.stl');base.apply_translation([240,-300,8]);arm=t.load('outputs/v5/B_dual_socket_arm_130mm.stl');arm.apply_translation([0,0,8])
ax=fig.add_subplot(121,projection='3d');draw(ax,[ship,connector,plaque,base,arm],['#319aa1','#319aa1','#319aa1','#bac7d0','#d88b36'],'Example connected layout\nShip above-left · decorative plaque below-right',[(-155,390),(-420,155),(0,200)],90,-90)
ax.text(0,-225,18,'OPEN\nCONNECTOR',ha='center',va='center',fontsize=9,color='#284957')
# Right panel: components separated to explain mounting and joining geometry.
a=t.load('outputs/v5/tile_ship_arm.stl');p=t.load('outputs/v5/tile_plaque.stl');p.apply_translation([270,0,0]);j=t.load('outputs/v5/tile_open_connector.stl');j.apply_translation([135,-280,0]);
ax2=fig.add_subplot(122,projection='3d');draw(ax2,[a,p,j],['#319aa1','#7e9eb5','#a8bbc2'],'Three tile types · same interlocking edges\n244 × 244 mm maximum print footprint',[(-145,415),(-420,150),(0,80)],90,-90)
ax2.text(0,140,10,'ARM TILE',ha='center',fontsize=10,color='#284957');ax2.text(270,140,10,'PLAQUE TILE',ha='center',fontsize=10,color='#284957');ax2.text(135,-140,10,'OPEN TILE',ha='center',fontsize=10,color='#284957')
fig.suptitle('Revision 5 — a modular wall-display system',fontsize=23,y=.96)
fig.text(.5,.078,'240 mm grid · front-inserted dovetail joints · two nail keyholes and two screw holes per tile',ha='center',fontsize=13,color='#385563')
fig.text(.5,.043,'Plaque has five mounting heights. Use open tiles to leave enough room for the actual ship; no ship outline is assumed here.',ha='center',fontsize=11,color='#385563')
plt.subplots_adjust(left=.01,right=.99,bottom=.12,top=.84,wspace=.04);plt.savefig('outputs/v5/system_preview.png',dpi=155,facecolor=fig.get_facecolor())
