# Star Trek wall display

Current design: **v40 — intermediate Galaxy retainer holes for M2.5 screws**.

- [Latest print files, notes and previews](outputs/)
- [Geometry checks](outputs/geometry_checks.json)
- [Version history and tagged archives](VERSIONS.md)
- [Artifact checksums](manifest.json)

Only the latest version files are kept on main. ZIP files are not tracked. Earlier designs remain accessible through Git commits and version tags.

All eight hexagon variants now have the original inner-edge title-holder recess filled with solid material. External interlocking connectors retain their geometry. See the [notch detail](outputs/filled_title_notch_preview.png). Run `work/fill_title_notches.py` after regenerating any older frame geometry.

The [lighter corner-braced arm](outputs/hex_ship_corner_braced_light_arm.stl) removes the 5-degree outward socket and retains the upward socket at its original 130 mm clearance from the frame front. It has a centred 38 mm-wide base, an arm approximately 17 mm wide near its base and a 20 × 20 mm socket housing, and a rounded tip at 147 mm from the wall. Solid-model volume is 44.9% lower than the dual-socket corner-braced version; actual filament savings depend on slicing. Both existing peg inserts still fit geometrically. The original variants remain available. See the [preview](outputs/light_arm_preview.png). Strength of this slimmer variant is not physically validated.

For the smaller Galaxy plaque, use [hex_plaque_galaxy_4.7mm.stl](outputs/hex_plaque_galaxy_4.7mm.stl) and [plaque_retainer_galaxy_4.7mm.stl](outputs/plaque_retainer_galaxy_4.7mm.stl). It has bottom-centre, lower-left and lower-right clips and an upper-right removable retainer (M2.5 × 12 mm screw). The gap is 4.9 mm for the measured 4.7 mm plaque. The holder pilot is 2.35 mm and the retainer clearance hole is 3.1 mm, splitting the difference between the previous sizes and the proposed M2.5 sizes. The retainer position and body are unchanged from v39. The larger plaque holders retain their existing holes. See the [Galaxy preview](outputs/galaxy_holder_preview.png). The older generic 4.7 mm holder has the larger Sovereign outline and is not the Galaxy holder.

The [corner-braced arm mount](outputs/hex_ship_corner_braced_arm.stl) is a parallel option to the original side-braced arm mount. Three 12 × 8 mm braces connect opposite corners. The inner hexagon is centred and measures 96 × 83.14 × 8 mm, supporting the rounded arm joint. The vertical nail brace is removed and the nail tab matches the plain open hexagon. The arm, peg sockets and outer connectors are preserved. The existing nail cover is intended for the side-braced mount, not this restored tab. See the [preview](outputs/corner_braced_arm_preview.png). Geometry is checked; physical strength has not been tested.

An additional [empty hexagon](outputs/hex_empty_original_size.stl) preserves the original 210 × 185.865 × 8 mm frame and interlocking connectors, with no nail tab or internal supports. Print flat at 100% scale. The existing open frame with nail tab remains available.

The current inserts have identical 10.3 mm square stems, rounded shoulders and 0.15 mm nominal bottom clearance at bolt alignment. Pin-free retention relies on tested physical friction. The 8 mm round peg has 19 mm engagement; the 6 mm peg has 10 mm engagement. Snug plaque-holder/latch sets are included for 5.7 mm and 4.7 mm plates.

Dimensions are millimetres. Print at 100% scale. Geometry checks do not establish physical fit or load capacity. See assembly notes and print the relevant fit tests first.

`source_models` contains the supplied reference meshes. `work` contains the current peg generator, renderer, packaging script and shared rendering helper. Paths stay stable across versions; Git commits and tags identify each revision.
