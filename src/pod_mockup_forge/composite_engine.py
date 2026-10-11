"""POD Mockup Forge - Composite Rendering Engine.

Generates mathematical placement bounds, SVG lifestyle scenes,
and HTML5 Canvas rendering instructions with zero external pip dependencies.
100% Python Standard Library.
"""

import re
from html import escape as _esc
from typing import Dict, Any, Optional, Tuple
from .templates import MOCKUP_TEMPLATES, MockupTemplate

_HEX_RE = re.compile(r"^#(?:[0-9a-fA-F]{3}|[0-9a-fA-F]{6})$")
_SAFE_URL_RE = re.compile(r"^(?:https?://|data:image/(?:png|jpe?g|webp|gif|svg\+xml);base64,|\.{0,2}/|[\w.-]+\.(?:png|jpe?g|webp|gif|svg)$)", re.I)


def validate_hex_color(value: str) -> str:
    if not isinstance(value, str) or not _HEX_RE.match(value.strip()):
        raise ValueError(f"color must be a hex value like #F5F5DC, got {value!r}")
    return value.strip()


def validate_artwork_url(url: str) -> str:
    """Allow http(s), image data: URIs and relative image paths; block javascript: etc."""
    if not isinstance(url, str) or not url.strip() or not _SAFE_URL_RE.match(url.strip()) \
            or any(ch in url for ch in '"<>\'`') or any(ch.isspace() for ch in url.strip()):
        raise ValueError(f"artwork must be an http(s) URL, image data: URI or relative image path, got {url!r}")
    return url.strip()

class MockupCompositeEngine:
    """Computes placement coordinates, aspect ratios, and generates composite render specs."""

    @staticmethod
    def calculate_aspect_fit(
        art_w: float,
        art_h: float,
        target_w: float,
        target_h: float,
        mode: str = "contain"
    ) -> Dict[str, float]:
        """Calculates centered scaling dimensions to fit artwork within print area without distortion."""
        if art_w <= 0 or art_h <= 0 or target_w <= 0 or target_h <= 0:
            raise ValueError("artwork and target dimensions must all be > 0")
        if mode not in ("contain", "cover"):
            raise ValueError("mode must be 'contain' or 'cover'")

        art_aspect = art_w / art_h
        target_aspect = target_w / target_h

        if mode == "contain":
            if art_aspect > target_aspect:
                # Wider than target
                fit_w = target_w
                fit_h = target_w / art_aspect
            else:
                # Taller than target
                fit_h = target_h
                fit_w = target_h * art_aspect
        else:  # cover
            if art_aspect > target_aspect:
                fit_h = target_h
                fit_w = target_h * art_aspect
            else:
                fit_w = target_w
                fit_h = target_w / art_aspect

        offset_x = (target_w - fit_w) / 2.0
        offset_y = (target_h - fit_h) / 2.0

        return {
            "width": round(fit_w, 1),
            "height": round(fit_h, 1),
            "offset_x": round(offset_x, 1),
            "offset_y": round(offset_y, 1),
            "scale_factor": round(fit_w / art_w, 3)
        }

    @classmethod
    def render_scene_spec(
        cls,
        template_id: str,
        artwork_url: str,
        color_hex: Optional[str] = None,
        watermark: bool = False,
        artwork_width: int = 1200,
        artwork_height: int = 1200
    ) -> Dict[str, Any]:
        """Generates a complete scene composite specification."""
        tpl = MOCKUP_TEMPLATES.get(template_id)
        if tpl is None:
            raise ValueError(f"Unknown template {template_id!r}. Use one of: {', '.join(MOCKUP_TEMPLATES)}")
        chosen_hex = validate_hex_color(color_hex) if color_hex else tpl.supported_colors[0]["hex"]
        artwork_url = validate_artwork_url(artwork_url)

        # Calculate absolute pixel bounding box on target canvas
        box_x = tpl.canvas_width * tpl.print_area.x_percent
        box_y = tpl.canvas_height * tpl.print_area.y_percent
        box_w = tpl.canvas_width * tpl.print_area.width_percent
        box_h = tpl.canvas_height * tpl.print_area.height_percent

        fit = cls.calculate_aspect_fit(artwork_width, artwork_height, box_w, box_h, mode="contain")

        art_placed_x = round(box_x + fit["offset_x"], 1)
        art_placed_y = round(box_y + fit["offset_y"], 1)
        art_placed_w = fit["width"]
        art_placed_h = fit["height"]

        # Generate lightweight vector SVG composite layer
        svg_mockup = cls._generate_svg_preview(
            tpl=tpl,
            chosen_hex=chosen_hex,
            art_x=art_placed_x,
            art_y=art_placed_y,
            art_w=art_placed_w,
            art_h=art_placed_h,
            artwork_url=artwork_url,
            watermark=watermark
        )

        return {
            "template_id": tpl.template_id,
            "product_name": tpl.product_name,
            "scene_name": tpl.scene_name,
            "canvas_width": tpl.canvas_width,
            "canvas_height": tpl.canvas_height,
            "aspect_ratio": tpl.aspect_ratio,
            "selected_color": chosen_hex,
            "placement": {
                "x": art_placed_x,
                "y": art_placed_y,
                "width": art_placed_w,
                "height": art_placed_h,
                "blend_mode": tpl.blend_mode,
                "rotation_deg": tpl.print_area.rotation_deg
            },
            "lighting": {
                "highlight_opacity": tpl.lighting_highlight_opacity,
                "shadow_opacity": tpl.shadow_depth_opacity
            },
            "watermark_applied": watermark,
            "svg_preview": svg_mockup
        }

    @staticmethod
    def _generate_svg_preview(
        tpl: MockupTemplate,
        chosen_hex: str,
        art_x: float,
        art_y: float,
        art_w: float,
        art_h: float,
        artwork_url: str,
        watermark: bool
    ) -> str:
        """Generates an embedded standalone SVG markup simulating fabric texture and lighting."""
        w = tpl.canvas_width
        h = tpl.canvas_height
        href = _esc(artwork_url, quote=True)  # defence in depth on top of validation
        fill = _esc(chosen_hex, quote=True)
        blend = _esc(str(tpl.blend_mode), quote=True)
        rot = float(tpl.print_area.rotation_deg or 0.0)
        cx, cy = art_x + art_w / 2.0, art_y + art_h / 2.0
        rotate_attr = f' transform="rotate({rot:g} {cx:.1f} {cy:.1f})"' if rot else ""

        watermark_xml = ""
        if watermark:
            watermark_xml = f"""
            <text x="{w/2}" y="{h/2}" font-family="Space Grotesk, sans-serif" font-size="42" font-weight="bold" fill="rgba(255,255,255,0.4)" text-anchor="middle" transform="rotate(-30 {w/2} {h/2})">
              SAMPLE PREVIEW • SOVEREIGN MOCKUP
            </text>
            """

        return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="100%" height="100%">
  <defs>
    <radialGradient id="ambientLight" cx="40%" cy="30%" r="70%">
      <stop offset="0%" stop-color="#FFFFFF" stop-opacity="{tpl.lighting_highlight_opacity}"/>
      <stop offset="100%" stop-color="#000000" stop-opacity="{tpl.shadow_depth_opacity}"/>
    </radialGradient>
    <filter id="fabricTexture">
      <feTurbulence type="fractalNoise" baseFrequency="0.04" numOctaves="3" result="noise"/>
      <feColorMatrix type="matrix" values="1 0 0 0 0  0 1 0 0 0  0 0 1 0 0  0 0 0 0.08 0" in="noise" result="coloredNoise"/>
      <feBlend mode="multiply" in="SourceGraphic" in2="coloredNoise"/>
    </filter>
  </defs>

  <!-- Background Environment -->
  <rect width="{w}" height="{h}" fill="#141824"/>

  <!-- Product Base Substrate -->
  <rect x="{w*0.15}" y="{h*0.1}" width="{w*0.7}" height="{h*0.8}" rx="24" fill="{fill}" filter="url(#fabricTexture)"/>

  <!-- Fabric Lighting Overlay -->
  <rect x="{w*0.15}" y="{h*0.1}" width="{w*0.7}" height="{h*0.8}" rx="24" fill="url(#ambientLight)" style="mix-blend-mode: multiply;"/>

  <!-- Artwork Layer -->
  <image href="{href}" x="{art_x}" y="{art_y}" width="{art_w}" height="{art_h}" preserveAspectRatio="xMidYMid meet" opacity="0.95" style="mix-blend-mode: {blend};"{rotate_attr}/>

  {watermark_xml}
</svg>"""
