# Current supporting scripts

Run from the repository root with Python, numpy, scipy, trimesh, manifold3d and matplotlib available.

- `build.py` regenerates the peg inserts against the current arm and geometry report in outputs; it does not rebuild the entire display system.
- `render_pegs.py` renders the current inserts using the shared `render.py` helper.
- `package.py` validates the insert interfaces, generates fit samples and creates an ignored local ZIP from current outputs. Assembly notes are maintained separately.

These scripts operate on the current outputs directly. Historical complete design workflows remain in older Git commits and tags. No version numbers are used in current filenames or output-directory paths.
