"""POD Mockup Forge - Template Registry & Scene Geometries.

Defines pixel placement matrices, perspective bounding quads,
and optical lighting blend modes for top 8 high-converting POD mockups.
100% Python Standard Library.
"""

from dataclasses import dataclass
from typing import Dict, List, Any, Tuple, Optional

@dataclass
class PrintAreaBox:
    x_percent: float
    y_percent: float
    width_percent: float
    height_percent: float
    rotation_deg: float = 0.0

@dataclass
class MockupTemplate:
    template_id: str
    product_name: str
    scene_name: str
    category: str
    aspect_ratio: str  # "1:1" (Square) or "4:3" (Etsy Optimal)
    canvas_width: int
    canvas_height: int
    print_area: PrintAreaBox
    blend_mode: str  # "multiply", "overlay", "soft-light"
    supported_colors: List[Dict[str, str]]
    lighting_highlight_opacity: float
    shadow_depth_opacity: float
    description: str

MOCKUP_TEMPLATES: Dict[str, MockupTemplate] = {
    "gildan_18000_flatlay": MockupTemplate(
        template_id="gildan_18000_flatlay",
        product_name="Gildan 18000 Crewneck Sweatshirt",
        scene_name="Flat Lay on Rustic Dark Oak Wood",
        category="Apparel",
        aspect_ratio="1:1",
        canvas_width=2000,
        canvas_height=2000,
        print_area=PrintAreaBox(x_percent=0.32, y_percent=0.28, width_percent=0.36, height_percent=0.42),
        blend_mode="multiply",
        supported_colors=[
            {"name": "Sand", "hex": "#D6C7A1"},
            {"name": "Forest Green", "hex": "#2D4233"},
            {"name": "Ash Grey", "hex": "#CFD3D6"},
            {"name": "Navy", "hex": "#1C2833"},
            {"name": "Black", "hex": "#1A1A1A"}
        ],
        lighting_highlight_opacity=0.18,
        shadow_depth_opacity=0.25,
        description="Cozy overhead flat lay styled on rustic weathered dark oak with natural textured fabric folds."
    ),
    "comfort_colors_1717_hanger": MockupTemplate(
        template_id="comfort_colors_1717_hanger",
        product_name="Comfort Colors 1717 Garment-Dyed Tee",
        scene_name="Minimalist Brass Hanger & Sunlit Stucco",
        category="Apparel",
        aspect_ratio="4:3",
        canvas_width=2700,
        canvas_height=2025,
        print_area=PrintAreaBox(x_percent=0.35, y_percent=0.32, width_percent=0.30, height_percent=0.44),
        blend_mode="multiply",
        supported_colors=[
            {"name": "Pepper", "hex": "#3E3B3A"},
            {"name": "Moss", "hex": "#626B58"},
            {"name": "Terracotta", "hex": "#B85C43"},
            {"name": "Chambray", "hex": "#8FA9BA"},
            {"name": "Ivory", "hex": "#F4F1EA"}
        ],
        lighting_highlight_opacity=0.22,
        shadow_depth_opacity=0.30,
        description="Modern boutique hanger mockup bathed in warm afternoon sunlight with gentle botanical leaf shadows."
    ),
    "bella_canvas_3001_model": MockupTemplate(
        template_id="bella_canvas_3001_model",
        product_name="Bella+Canvas 3001 Unisex Tee",
        scene_name="Urban Lifestyle Casual Daylight",
        category="Apparel",
        aspect_ratio="1:1",
        canvas_width=2000,
        canvas_height=2000,
        print_area=PrintAreaBox(x_percent=0.34, y_percent=0.26, width_percent=0.32, height_percent=0.40),
        blend_mode="multiply",
        supported_colors=[
            {"name": "White", "hex": "#FFFFFF"},
            {"name": "Heather Peach", "hex": "#F7C5B0"},
            {"name": "Mauve", "hex": "#8A6B75"},
            {"name": "Dark Grey Heather", "hex": "#404040"},
            {"name": "Olive", "hex": "#4B5320"}
        ],
        lighting_highlight_opacity=0.15,
        shadow_depth_opacity=0.20,
        description="Authentic real-world portrait model mockup delivering genuine human emotional connection."
    ),
    "ceramic_mug_15oz_kitchen": MockupTemplate(
        template_id="ceramic_mug_15oz_kitchen",
        product_name="White Gloss Ceramic Mug 15oz",
        scene_name="Carrara Marble Counter & French Press",
        category="Drinkware",
        aspect_ratio="1:1",
        canvas_width=2000,
        canvas_height=2000,
        print_area=PrintAreaBox(x_percent=0.30, y_percent=0.36, width_percent=0.40, height_percent=0.38),
        blend_mode="multiply",
        supported_colors=[
            {"name": "Pure Gloss White", "hex": "#FFFFFF"},
            {"name": "Sage Two-Tone", "hex": "#8A9A86"},
            {"name": "Dusty Rose Two-Tone", "hex": "#C9A098"}
        ],
        lighting_highlight_opacity=0.35,
        shadow_depth_opacity=0.40,
        description="Bright, airy kitchen still life on polished Italian Carrara marble beside warm coffee morning essentials."
    ),
    "canvas_gallery_wrap_livingroom": MockupTemplate(
        template_id="canvas_gallery_wrap_livingroom",
        product_name="Stretched Canvas Gallery Wrap 16x20",
        scene_name="Scandinavian Minimalist Living Room",
        category="Wall Art",
        aspect_ratio="4:3",
        canvas_width=2700,
        canvas_height=2025,
        print_area=PrintAreaBox(x_percent=0.36, y_percent=0.18, width_percent=0.28, height_percent=0.46),
        blend_mode="multiply",
        supported_colors=[
            {"name": "Standard Wrap", "hex": "#FFFFFF"}
        ],
        lighting_highlight_opacity=0.12,
        shadow_depth_opacity=0.35,
        description="Spacious Scandinavian interior styled above a teak wood credenza with architectural gallery lighting."
    ),
    "matte_poster_wood_frame": MockupTemplate(
        template_id="matte_poster_wood_frame",
        product_name="Museum-Quality Matte Paper Poster 18x24",
        scene_name="Natural Solid Oak Frame on Off-White Wall",
        category="Wall Art",
        aspect_ratio="1:1",
        canvas_width=2000,
        canvas_height=2000,
        print_area=PrintAreaBox(x_percent=0.28, y_percent=0.16, width_percent=0.44, height_percent=0.62),
        blend_mode="multiply",
        supported_colors=[
            {"name": "Natural Oak Frame", "hex": "#C49A6C"},
            {"name": "Matte Black Frame", "hex": "#1F1F1F"},
            {"name": "Clean White Frame", "hex": "#F0F0F0"}
        ],
        lighting_highlight_opacity=0.14,
        shadow_depth_opacity=0.28,
        description="Crisp gallery wall framing with realistic beveled glass reflection and soft ambient shadow drop."
    ),
    "canvas_tote_farmers_market": MockupTemplate(
        template_id="canvas_tote_farmers_market",
        product_name="Heavyweight Cotton Market Tote",
        scene_name="French Farmers Market & Fresh Peonies",
        category="Accessories",
        aspect_ratio="1:1",
        canvas_width=2000,
        canvas_height=2000,
        print_area=PrintAreaBox(x_percent=0.30, y_percent=0.38, width_percent=0.40, height_percent=0.42),
        blend_mode="multiply",
        supported_colors=[
            {"name": "Natural Cream", "hex": "#EFEBD9"},
            {"name": "Classic Black", "hex": "#232323"}
        ],
        lighting_highlight_opacity=0.16,
        shadow_depth_opacity=0.24,
        description="Textured organic canvas tote overflowing with garden fresh lavender and farmer market goods."
    ),
    "phone_case_flatlay": MockupTemplate(
        template_id="phone_case_flatlay",
        product_name="Impact Dual-Layer Tough Phone Case",
        scene_name="Obsidian Desk & Executive EDC Flat Lay",
        category="Accessories",
        aspect_ratio="1:1",
        canvas_width=2000,
        canvas_height=2000,
        print_area=PrintAreaBox(x_percent=0.38, y_percent=0.24, width_percent=0.24, height_percent=0.52),
        blend_mode="multiply",
        supported_colors=[
            {"name": "Glossy Shield", "hex": "#FFFFFF"},
            {"name": "Matte Stealth", "hex": "#2B2B2B"}
        ],
        lighting_highlight_opacity=0.32,
        shadow_depth_opacity=0.38,
        description="High-contrast modern workspace flat lay styled beside premium notebook and metal EDC gear."
    )
}

def get_all_templates() -> List[Dict[str, Any]]:
    result = []
    for t in MOCKUP_TEMPLATES.values():
        result.append({
            "id": t.template_id,
            "name": f"{t.product_name} ({t.scene_name})",
            "product_name": t.product_name,
            "scene_name": t.scene_name,
            "category": t.category,
            "vibe": t.scene_name,
            "aspect_ratio": t.aspect_ratio,
            "canvas_dimensions": f"{t.canvas_width}x{t.canvas_height}px",
            "canvas_width": t.canvas_width,
            "canvas_height": t.canvas_height,
            "print_area": {
                "x": int(t.canvas_width * t.print_area.x_percent if t.print_area.x_percent <= 1.0 else t.print_area.x_percent),
                "y": int(t.canvas_height * t.print_area.y_percent if t.print_area.y_percent <= 1.0 else t.print_area.y_percent),
                "width": int(t.canvas_width * t.print_area.width_percent if t.print_area.width_percent <= 1.0 else t.print_area.width_percent),
                "height": int(t.canvas_height * t.print_area.height_percent if t.print_area.height_percent <= 1.0 else t.print_area.height_percent),
                "x_percent": t.print_area.x_percent,
                "y_percent": t.print_area.y_percent,
                "width_percent": t.print_area.width_percent,
                "height_percent": t.print_area.height_percent
            },
            "blend_mode": t.blend_mode,
            "color_palette": t.supported_colors,
            "colors": [c["name"] for c in t.supported_colors] if isinstance(t.supported_colors[0], dict) else t.supported_colors,
            "description": t.description
        })
    return result

def get_template(template_id: str) -> Optional[MockupTemplate]:
    return MOCKUP_TEMPLATES.get(template_id)

