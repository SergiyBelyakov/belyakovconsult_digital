# Interactive data journey

The test website now includes `/data-journey/`, with 13 stages, nine service areas and 78 component explanations. The homepage includes an invitation using the nine original master icons. All 39 navigation menus link to the experience; all nine Ukrainian service pages link directly to their corresponding stage.

The homepage invitation is localized in Ukrainian, English and Portuguese. The journey itself is Ukrainian. English and Portuguese entry points explicitly say “UA”.

## Assets and rendering

All 57 PNGs under `data-journey/assets/icons/` are the unchanged originals extracted from the supplied presentation. `data-journey/assets/icon-manifest.json` records the source slides and SHA-256 checksums.

The scene is 2.5D: original artwork is displayed on camera-facing planes in a spatial scene. It does not provide volumetric versions or a 360-degree view of the icons. Three.js r128 is bundled locally. Browsers without WebGL use the Canvas perspective renderer with the same original PNGs. Google Fonts have system font fallbacks.

Journey CSS and JavaScript load only on the journey page. `journey-preview.css` is scoped to the homepage invitation. The site needs no build step, database or new API credentials.

## Navigation

Journey service and contact links stay on the same deployment. The brand and “На сайт” link return to the homepage. The initial hash is restored after the chapters are inserted, so `/data-journey/#quality` opens stage 04 directly.

Existing root-relative website navigation assumes deployment at the domain root, as before this integration. GitHub project Pages hosting at a repository subpath would require a separate base-path adaptation. GitHub Pages was not enabled for this repository at integration time.

## Validation

- All 57 PNG files compared byte-for-byte with the source artwork.
- Local links and resources on the three homepages and journey page checked.
- Journey JavaScript syntax checked with Node.js.
- Browser verification covered homepage navigation, original-icon invitation, component comments, service links, return links and direct stage opening.
- The cloud browser used the Canvas fallback. Native WebGL and physical mobile-device rendering were not verified.

To deploy, serve this repository's static files from the domain root. No Sites-specific hosting files or credentials are included in this repository. To undo the integration, revert its Git commit.
