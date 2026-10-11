# POD Mockup Forge

Mockup placement math, SVG scene specs, a 10-slot Etsy photo-pack planner and
an Etsy listing-photo auditor for print-on-demand products. Pure stdlib.

## Use

```bash
export PYTHONPATH=src
python3 -m pod_mockup_forge.cli list
python3 -m pod_mockup_forge.cli render --template ceramic_mug_15oz_kitchen --artwork https://example.com/art.png --output-svg mug.svg
python3 -m pod_mockup_forge.cli fit --help
python3 -m pod_mockup_forge.cli pack
python3 -m pod_mockup_forge.cli audit --file listing-photo.jpg     # reads real PNG/JPEG/GIF/WebP headers
python3 -m pod_mockup_forge.cli audit --width 2700 --height 2025 --mb 4
python3 -m pod_mockup_forge.cli server                              # web UI on :8119
```

## Audit rules

Shortest side >= 2000px, <= 20MB (warning above 10MB), 4:3 or 1:1 aspect.
Colour space is not inspected (`srgb_color_space: null`).

## Safety

Rendered SVG is safe to open in a browser: colours must be hex, artwork must be
an http(s) URL, an image `data:` URI or a relative image path (no
`javascript:`, quotes or angle brackets), and all attributes are escaped.
Unknown templates and invalid dimensions raise errors instead of silently
falling back to the Gildan template.

## Test

```bash
python3 -m pytest -q tests/
```
