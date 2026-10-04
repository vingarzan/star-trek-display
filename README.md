# Star Trek wall display

Current design: **v32 — title-holder notch filled on every hexagon**.

- [Latest print files, notes and previews](outputs/)
- [Geometry checks](outputs/geometry_checks.json)
- [Version history and tagged archives](VERSIONS.md)
- [Artifact checksums](manifest.json)

Only the latest version files are kept on main. ZIP files are not tracked. Earlier designs remain accessible through Git commits and version tags.

All six hexagon variants now have the original inner-edge title-holder recess filled with solid material. External interlocking connectors retain their geometry. See the [notch detail](outputs/filled_title_notch_preview.png). Run `work/fill_title_notches.py` after regenerating any older frame geometry.

The [corner-braced arm mount](outputs/hex_ship_corner_braced_arm.stl) is a parallel option to the original side-braced arm mount. Three 12 × 8 mm braces connect opposite corners; the upper nail support remains. The arm, peg sockets, central base, nail recess and outer connectors are preserved. See the [preview](outputs/corner_braced_arm_preview.png). Geometry is checked; physical strength has not been tested.

An additional [empty hexagon](outputs/hex_empty_original_size.stl) preserves the original 210 × 185.865 × 8 mm frame and interlocking connectors, with no nail tab or internal supports. Print flat at 100% scale. The existing open frame with nail tab remains available.

The current inserts have identical 10.3 mm square stems, rounded shoulders and 0.15 mm nominal bottom clearance at bolt alignment. Pin-free retention relies on tested physical friction. The 8 mm round peg has 19 mm engagement; the 6 mm peg has 10 mm engagement. Snug plaque-holder/latch sets are included for 5.7 mm and 4.7 mm plates.

Dimensions are millimetres. Print at 100% scale. Geometry checks do not establish physical fit or load capacity. See assembly notes and print the relevant fit tests first.

`source_models` contains the supplied reference meshes. `work` contains the current peg generator, renderer, packaging script and shared rendering helper. Paths stay stable across versions; Git commits and tags identify each revision.
