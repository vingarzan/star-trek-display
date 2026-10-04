# Version publication workflow
The user explicitly requests every new design version be committed and pushed to https://github.com/vingarzan/star-trek-display.

- Keep only the latest outputs and supporting files on main. Store deliverables directly in outputs/, checksums in manifest.json and supporting scripts under stable names in work/. Do not create version-numbered directories or filenames in the repository. Remove superseded versions from the current tree when publishing a new version; preserve their existing commits and tags.
- Never track ZIP files. Local ZIP downloads may still be produced, but are excluded from repository uploads.
- Include current STLs, preview, assembly notes and geometry checks. Preserve fit_test_ prefixes.
- Update README.md, the current manifest and VERSIONS.md; historical links must point to version tags, not deleted current-tree paths.
- Validate exported files and inspect previews before committing. Geometry checks do not imply physical testing.
- Create a descriptive commit per design version and an unused vN tag, then push main and the new tag. The user has authorized this workflow; do not ask repeatedly.
- Fetch first and preserve remote work. Never force-push, rewrite published versions or move published tags.
- Report failed publication explicitly. Do not upload personal photos, credentials, virtual environments or unrelated scratch files.
