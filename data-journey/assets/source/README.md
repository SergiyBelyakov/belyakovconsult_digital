# Geometry sources

These Python files recreate the glass GLB family from volumetric meshes. They are not needed to view or deploy the website. The included `reference.glb` is the exact supplied Architecture model.

Use Python 3.11 or 3.12. From the `data-journey` folder install the optional generator dependencies with `python3 -m pip install -r source/requirements.txt`. Run `python3 source/build_glass.py` to regenerate the 50 model files. It writes `assets/glass/catalog.generated.json`, keeping the website's current registry intact until it is refreshed explicitly.

The generated family uses transmission, volume, IOR and clearcoat extensions. Clear panes, hollow database shells, thin edge lines and ruby accents are modeled as meshes. The visual forms derive from the supplied Timesaver presentation. The Architecture master remains the supplied GLB.

`render_glass.py` creates previews directly from the meshes using Mitsuba. Install the additional render dependencies with `python3 -m pip install mitsuba pillow scipy`. Existing previews are retained; remove only the previews that you intend to regenerate, then run `python3 source/render_glass.py --samples 256`. Rendering is optional and can take several minutes. The initial nine service previews are supplied at 800 × 600.

After regenerating models and previews, run `python3 source/refresh_catalog.py` to update model metadata, preview dimensions, `glass-index.js` and the homepage service composition. No internet request is needed by these scripts after dependencies are installed.

The mesh conventions are Y-up and front +Z. Each GLB includes the animation clips `Turntable_360` and `Float_Idle`. The website uses its own focused inspection controls, so it does not need to play the embedded clips to support rotation.
