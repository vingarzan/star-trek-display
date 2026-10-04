"""Generate an empty original-size frame from the supplied no-nail STL."""
from pathlib import Path
import json
import numpy as np
import trimesh as t
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.collections import PolyCollection

ROOT = Path(__file__).resolve().parents[1]
out = ROOT / 'outputs'
source = t.load(ROOT / 'source_models/obj_1_Inclined display.stl')
frame = sorted(source.split(), key=lambda m: m.extents[2])[0]
frame.apply_translation([-128, -126, 0])
radius = 98.07179677
cut = t.convex.convex_hull(np.array([
    [radius*np.cos(a), radius*np.sin(a), z]
    for a in np.arange(6)*np.pi/3 for z in [-1, 9]
]))
empty = t.boolean.difference([frame, cut], engine='manifold')
path = out / 'hex_empty_original_size.stl'
empty.export(path)
mesh = t.load(path)
assert mesh.is_volume and len(mesh.split()) == 1
assert np.allclose(mesh.extents, [210, 185.86534882, 8], atol=0.0001)
assert abs(t.boolean.intersection([mesh, cut], engine='manifold').volume) < 0.001
# All removed material must be confined to the central opening.
original_border = t.boolean.difference([frame, cut], engine='manifold')
errors = [abs(t.boolean.difference([a,b], engine='manifold').volume)
          for a,b in [(mesh, original_border), (original_border, mesh)]]
assert max(errors) < 0.001
checks = json.loads((out / 'geometry_checks.json').read_text())
checks['hex_empty_original_size'] = dict(dimensions_mm=mesh.extents.tolist(),
    watertight=bool(mesh.is_watertight), components=1, export_reload_verified=True,
    volume_cm3=float(mesh.volume/1000), original_border_difference_mm3=errors,
    inner_opening_empty=True, nail_tab=False)
(out / 'geometry_checks.json').write_text(json.dumps(checks, indent=2)+'\n')
fig, ax = plt.subplots(figsize=(8,8))
ax.add_collection(PolyCollection(mesh.triangles[:,:,:2], facecolor='#527a97', edgecolor='none'))
ax.set(xlim=(-113,113), ylim=(-100,105), aspect='equal', xlabel='mm', ylabel='mm',
       title='Empty original-size hexagon\n210 × 185.865 × 8 mm · original interlocking border')
fig.tight_layout()
fig.savefig(out / 'empty_hex_preview.png', dpi=160)
print(json.dumps(checks['hex_empty_original_size'], indent=2))
