# Star Trek wall display

Interlocking wall-display frames, ship-support arms, decorative plaque holders and removable peg inserts for 3D printing.

Current version: **v29 — Snug removable peg inserts with optional retaining pin**.

- [Print files and previews](outputs/v29/)
- [Version history](VERSIONS.md)
- [Artifact checksums](manifests/v29.json)

All dimensions are millimetres. Print at 100% scale. These are evolving prototypes: geometric validation is not a load rating or a substitute for physical fit and strength testing.

The `outputs` tree preserves each available version and its original packaged ZIP when one was produced. `work` contains historical design scripts, and `source_models` contains the supplied reference meshes. Future versions are committed and pushed here as part of the design workflow.

Current inserts: 8 mm diameter × 19 mm engagement and 6 mm diameter × 10 mm engagement for a 12 mm-deep hole. Both omit the overhanging disk and retain optional M3 cross-bolt holes; pin-free use requires verified friction retention. All fit-test STLs start with `fit_test_`.

Version 26 adds round conical peg transitions and two matched plaque-holder/latch sets with 0.2 mm nominal clearance. Print the matching gap sample first. The 4.7 mm set assumes the same plaque outline.

Version 27 replaces the straight conical transitions with curved fillets. The 6 mm transition is now 2 mm high; the 8 mm transition remains 3 mm high. Shaft engagement lengths and socket interfaces are unchanged.

Version 28 gives both inserts identical 11.6 mm square bases and shortens the 6 mm round shaft to 10 mm. The rounded transitions start at the socket rim; bolt positions remain unchanged.

Version 29 uses identical 10.3 mm square stems with a lead-in chamfer and 0.15 mm nominal floor clearance at bolt alignment. Three stem-width fit samples are included. Without a bolt there is no axial stop; actual grip must be tested before use with a ship.
