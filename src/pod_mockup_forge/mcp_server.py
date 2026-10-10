"""POD Mockup Forge - Antigravity MCP Server
Implements 6 production JSON-RPC 2.0 tools for mockup generation, placement calculations, and Etsy photo auditing.
"""

import json
import sys
from typing import Dict, Any, List

from .templates import get_all_templates, get_template, MOCKUP_TEMPLATES
from .composite_engine import MockupCompositeEngine
from .etsy_specs import EtsyPhotoAuditor

TOOLS = [
    {
        "name": "mockup_list_templates",
        "description": "List all available POD mockup templates (apparel, mugs, wall art, accessories) with print dimensions and color options.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "category": {
                    "type": "string",
                    "description": "Optional category filter: apparel, drinkware, wall_art, accessories",
                    "enum": ["apparel", "drinkware", "wall_art", "accessories"]
                }
            }
        }
    },
    {
        "name": "mockup_generate_scene",
        "description": "Generate a high-fidelity SVG/JSON mockup scene specification with exact bounding coordinates, blend modes, and shadows.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "template_id": {
                    "type": "string",
                    "description": "Template identifier (e.g. gildan_18000_flatlay, comfort_colors_1717_hanger, mug_15oz_kitchen)"
                },
                "artwork_url": {
                    "type": "string",
                    "description": "URL or path of high-resolution transparent PNG artwork"
                },
                "color_hex": {
                    "type": "string",
                    "description": "Optional hex color for apparel/product surface (e.g. #F5F5DC, #1F2937)"
                },
                "watermark": {
                    "type": "boolean",
                    "description": "Whether to render anti-theft watermark protection grid"
                }
            },
            "required": ["template_id", "artwork_url"]
        }
    },
    {
        "name": "mockup_calculate_aspect_fit",
        "description": "Calculate exact coordinate bounding boxes, scale factor, and print margins to fit artwork onto a product's printable zone.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "artwork_width": {"type": "integer", "description": "Artwork width in pixels"},
                "artwork_height": {"type": "integer", "description": "Artwork height in pixels"},
                "target_width": {"type": "integer", "description": "Print area bounding box width in pixels"},
                "target_height": {"type": "integer", "description": "Print area bounding box height in pixels"}
            },
            "required": ["artwork_width", "artwork_height", "target_width", "target_height"]
        }
    },
    {
        "name": "mockup_batch_generate_listing_pack",
        "description": "Generate a comprehensive 10-slot Etsy carousel listing pack strategy covering hero, details, scale, colors, and lifestyle scenes.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "product_type": {
                    "type": "string",
                    "description": "Product type: sweatshirt, t_shirt, mug, canvas_print, tote_bag, phone_case",
                    "default": "sweatshirt"
                }
            }
        }
    },
    {
        "name": "mockup_audit_etsy_compliance",
        "description": "Audit an image's resolution, aspect ratio, and file size against Etsy's official 2026 seller photo standards.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "width_px": {"type": "integer", "description": "Image pixel width"},
                "height_px": {"type": "integer", "description": "Image pixel height"},
                "file_size_mb": {"type": "number", "description": "File size in megabytes"}
            },
            "required": ["width_px", "height_px", "file_size_mb"]
        }
    },
    {
        "name": "mockup_add_watermark_protection",
        "description": "Generate SVG anti-theft diagonal pattern and copyright overlay coordinates to safeguard mockups against image scrapers.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "canvas_width": {"type": "integer", "description": "Mockup canvas width in pixels", "default": 2000},
                "canvas_height": {"type": "integer", "description": "Mockup canvas height in pixels", "default": 2000},
                "watermark_text": {"type": "string", "description": "Watermark label/brand name", "default": "PREVIEW • DO NOT COPY"}
            }
        }
    }
]

def handle_call_tool(name: str, args: Dict[str, Any]) -> Dict[str, Any]:
    if name == "mockup_list_templates":
        cat = args.get("category")
        templates = get_all_templates()
        if cat:
            templates = [t for t in templates if t.get("category", "").lower() == cat.lower()]
        return {"count": len(templates), "templates": templates}


    elif name == "mockup_generate_scene":
        tid = args["template_id"]
        art = args["artwork_url"]
        color = args.get("color_hex")
        wm = bool(args.get("watermark", False))
        spec = MockupCompositeEngine.render_scene_spec(tid, art, color, wm)
        return {"status": "success", "scene_spec": spec}

    elif name == "mockup_calculate_aspect_fit":
        aw = args["artwork_width"]
        ah = args["artwork_height"]
        tw = args["target_width"]
        th = args["target_height"]
        metrics = MockupCompositeEngine.calculate_aspect_fit(aw, ah, tw, th)
        return {"aspect_metrics": metrics}

    elif name == "mockup_batch_generate_listing_pack":
        ptype = args.get("product_type", "sweatshirt")
        pack = EtsyPhotoAuditor.generate_listing_pack_plan()
        return {"product_type": ptype, "listing_pack": pack}

    elif name == "mockup_audit_etsy_compliance":
        w = args["width_px"]
        h = args["height_px"]
        mb = args["file_size_mb"]
        audit = EtsyPhotoAuditor.audit_image(w, h, mb)
        return {"etsy_audit": audit}

    elif name == "mockup_add_watermark_protection":
        cw = args.get("canvas_width", 2000)
        ch = args.get("canvas_height", 2000)
        text = args.get("watermark_text", "PREVIEW • DO NOT COPY")
        svg_snippet = f"""<svg width="{cw}" height="{ch}" xmlns="http://www.w3.org/2000/svg" style="pointer-events:none;">
  <defs>
    <pattern id="wmPattern" width="300" height="150" patternTransform="rotate(-30 0 0)" patternUnits="userSpaceOnUse">
      <text x="20" y="75" fill="rgba(255,255,255,0.18)" font-family="sans-serif" font-weight="900" font-size="20" letter-spacing="3">{text}</text>
    </pattern>
  </defs>
  <rect width="100%" height="100%" fill="url(#wmPattern)" />
</svg>"""
        return {
            "status": "success",
            "canvas_dimensions": {"width": cw, "height": ch},
            "svg_overlay": svg_snippet
        }

    raise ValueError(f"Unknown tool: {name}")

def run_mcp():
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            req = json.loads(line)
            req_id = req.get("id")
            method = req.get("method")

            if method == "tools/list":
                resp = {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "result": {"tools": TOOLS}
                }
            elif method == "tools/call":
                params = req.get("params", {})
                t_name = params.get("name")
                t_args = params.get("arguments", {})
                res = handle_call_tool(t_name, t_args)
                resp = {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "result": {"content": [{"type": "text", "text": json.dumps(res, indent=2)}]}
                }
            elif method == "initialize":
                resp = {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "result": {
                        "protocolVersion": "2024-11-05",
                        "capabilities": {"tools": {}},
                        "serverInfo": {"name": "pod-mockup-forge", "version": "1.0.0"}
                    }
                }
            else:
                resp = {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "error": {"code": -32601, "message": f"Method not found: {method}"}
                }

            sys.stdout.write(json.dumps(resp) + "\n")
            sys.stdout.flush()
        except Exception as e:
            err_resp = {
                "jsonrpc": "2.0",
                "id": req.get("id") if "req" in locals() else None,
                "error": {"code": -32603, "message": str(e)}
            }
            sys.stdout.write(json.dumps(err_resp) + "\n")
            sys.stdout.flush()

if __name__ == "__main__":
    run_mcp()
