"""POD Mockup Forge - Sovereign Command-Line Interface.

Zero-dependency Python 3.10+ Standard Library CLI.
"""

import argparse
import json
import sys

from .templates import get_all_templates, get_template
from .composite_engine import MockupCompositeEngine
from .etsy_specs import EtsyPhotoAuditor
from .server import run_server
from .mcp_server import run_mcp

def main():
    parser = argparse.ArgumentParser(
        prog="pod-mockup-forge",
        description="Autonomous Photorealistic Print-on-Demand Mockup Generator & Etsy Photo Auditor"
    )
    subparsers = parser.add_subparsers(dest="command", help="Available subcommands")

    # Command: list
    p_list = subparsers.add_parser("list", help="List all available mockup templates")
    p_list.add_argument("--category", choices=["apparel", "drinkware", "wall_art", "accessories"], help="Filter by category")
    p_list.add_argument("--json", action="store_true", help="Output raw JSON")

    # Command: render
    p_render = subparsers.add_parser("render", help="Generate mockup scene vector/SVG specification")
    p_render.add_argument("--template", default="gildan_18000_flatlay", help="Mockup template ID")
    p_render.add_argument("--artwork", default="https://nullai.tech/artwork/master.png", help="Artwork image URL")
    p_render.add_argument("--color", help="Custom surface hex color (e.g. #F5F5DC)")
    p_render.add_argument("--watermark", action="store_true", help="Render anti-theft watermark overlay")
    p_render.add_argument("--output-svg", help="Save generated SVG scene to file path")
    p_render.add_argument("--json", action="store_true", help="Output raw JSON")

    # Command: fit
    p_fit = subparsers.add_parser("fit", help="Calculate aspect fit and coordinate bounding box")
    p_fit.add_argument("--aw", type=int, required=True, help="Artwork width in px")
    p_fit.add_argument("--ah", type=int, required=True, help="Artwork height in px")
    p_fit.add_argument("--tw", type=int, default=800, help="Print area target width in px")
    p_fit.add_argument("--th", type=int, default=1000, help="Print area target height in px")
    p_fit.add_argument("--json", action="store_true", help="Output raw JSON")

    # Command: pack
    p_pack = subparsers.add_parser("pack", help="Plan 10-slot Etsy carousel listing pack")
    p_pack.add_argument("--json", action="store_true", help="Output raw JSON")

    # Command: audit
    p_audit = subparsers.add_parser("audit", help="Audit image against Etsy 2026 seller photo standards")
    p_audit.add_argument("--width", type=int, default=2000, help="Image width in px")
    p_audit.add_argument("--height", type=int, default=2000, help="Image height in px")
    p_audit.add_argument("--mb", type=float, default=3.5, help="File size in MB")
    p_audit.add_argument("--json", action="store_true", help="Output raw JSON")

    # Command: server
    p_server = subparsers.add_parser("server", help="Launch HTTP server & Web UI on port 8119")
    p_server.add_argument("--port", type=int, default=8119, help="Server port (default: 8119)")

    # Command: mcp
    p_mcp = subparsers.add_parser("mcp", help="Run Antigravity MCP stdio server")

    args = parser.parse_args()

    if args.command == "list":
        templates = get_all_templates()
        if args.category:
            templates = [t for t in templates if t["category"] == args.category]
        if args.json:
            print(json.dumps(templates, indent=2))
        else:
            print("=" * 70)
            print(f"POD MOCKUP FORGE - AVAILABLE TEMPLATES ({len(templates)})")
            print("=" * 70)
            for tpl in templates:
                print(f"• [{tpl['id']}] {tpl['name']} ({tpl['category'].upper()})")
                print(f"  Vibe: {tpl['vibe']} | Aspect: {tpl['aspect_ratio']} ({tpl['canvas_width']}x{tpl['canvas_height']}px)")
                print(f"  Print Zone: {tpl['print_area']['width']}x{tpl['print_area']['height']}px at ({tpl['print_area']['x']},{tpl['print_area']['y']})")
                colors = ", ".join([c["name"] for c in tpl["color_palette"]])
                print(f"  Colors: {colors}")
                print("-" * 70)

    elif args.command == "render":
        spec = MockupCompositeEngine.render_scene_spec(
            template_id=args.template,
            artwork_url=args.artwork,
            color_hex=args.color,
            watermark=args.watermark
        )
        svg_data = spec.get("svg_preview", "")
        if args.output_svg:
            with open(args.output_svg, "w", encoding="utf-8") as f:
                f.write(svg_data)
            print(f"Saved SVG mockup to {args.output_svg}")
        elif args.json:
            print(json.dumps(spec, indent=2))
        else:
            print("=" * 65)
            print(f"🎨 MOCKUP SCENE GENERATED: {spec['product_name']} ({spec['scene_name']})")
            print(f"Template ID:  {spec['template_id']}")
            print(f"Canvas:       {spec['canvas_width']}x{spec['canvas_height']}px (Aspect: {spec['aspect_ratio']})")
            print(f"Surface Hex:  {spec['selected_color']}")
            print(f"Print Placement: {spec['placement']['width']}x{spec['placement']['height']}px at ({spec['placement']['x']},{spec['placement']['y']})")
            print(f"SVG Code Length: {len(svg_data)} characters")
            print("=" * 65)

    elif args.command == "fit":
        metrics = MockupCompositeEngine.calculate_aspect_fit(
            args.aw, args.ah, args.tw, args.th
        )
        if args.json:
            print(json.dumps(metrics, indent=2))
        else:
            print(f"Artwork: {args.aw}x{args.ah}px → Target: {args.tw}x{args.th}px")
            print(f"Render Dimensions: {metrics['width']}x{metrics['height']}px")
            print(f"Offset Margins: Top {metrics['offset_y']}px, Left {metrics['offset_x']}px")
            print(f"Scale: {metrics['scale_factor']}")


    elif args.command == "pack":
        plan = EtsyPhotoAuditor.generate_listing_pack_plan()
        if args.json:
            print(json.dumps(plan, indent=2))
        else:
            print("=" * 70)
            print("ETSY 10-SLOT LISTING PACK BLUEPRINT")
            print("=" * 70)
            for slot in plan["slots"]:
                req = " [MANDATORY]" if slot.get("mandatory") else ""
                print(f"Slot #{slot['slot']}: {slot['title']}{req}")
                print(f"  Purpose: {slot['purpose']}")
                print(f"  Template: {slot['recommended_template_id']}")
                print(f"  Conversion Tip: {slot['conversion_tip']}")
                print("-" * 70)

    elif args.command == "audit":
        audit = EtsyPhotoAuditor.audit_image(args.width, args.height, args.mb)
        if args.json:
            print(json.dumps(audit, indent=2))
        else:
            print("=" * 65)
            status_symbol = "✅ PASS" if audit["is_compliant"] else "❌ NON-COMPLIANT"
            print(f"ETSY 2026 PHOTO COMPLIANCE AUDIT: {status_symbol} (Score: {audit['compliance_score']}/100)")
            print(f"Resolution: {args.width}x{args.height}px | Aspect: {audit['aspect_ratio']['ratio_label']} ({audit['aspect_ratio']['formatted']})")
            print(f"File Size:  {args.mb:.2f}MB (Max: {audit['file_size']['max_allowed_mb']}MB)")
            print("Checks:")
            for k, v in audit["checks"].items():
                icon = "✓" if v else "✗"
                print(f"  [{icon}] {k}")
            if audit["recommendations"]:
                print("Recommendations:")
                for r in audit["recommendations"]:
                    print(f"  • {r}")
            print("=" * 65)

    elif args.command == "server":
        run_server(args.port)

    elif args.command == "mcp":
        run_mcp()

    else:
        parser.print_help()

if __name__ == "__main__":
    main()
