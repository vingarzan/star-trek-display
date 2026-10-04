# Version publication workflow
The user explicitly requests that every new design version be committed and pushed to https://github.com/vingarzan/star-trek-display.

- Keep historical outputs immutable. Add outputs/vN for each new version and preserve fit_test_ prefixes.
- Include printable STLs, relevant preview, assembly notes and geometry checks. Include the version ZIP if produced.
- Update README.md, VERSIONS.md and manifests/vN.json; add/update the relevant generator and renderer.
- Validate exported files and inspect the preview before committing. Geometry checks do not imply physical testing.
- Create one descriptive commit per version and an unused vN tag. Push main and the new tag after the version is ready; no repeated permission request is needed for this authorized workflow.
- Fetch first and preserve remote work. Never force-push or rewrite published historical versions.
- Report any authentication or push failure explicitly instead of claiming publication.
- Do not commit personal photos, credentials, virtual environments or unrelated workspace files.
