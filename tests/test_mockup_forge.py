"""POD Mockup Forge - Comprehensive Unit Test Suite
Zero-dependency Python unittest testing templates, composite math, Etsy audit, and MCP tools.
"""

import unittest
import sys
from pathlib import Path

# Add src to python path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from pod_mockup_forge.templates import (
    MOCKUP_TEMPLATES,
    get_all_templates,
    get_template
)
from pod_mockup_forge.composite_engine import MockupCompositeEngine
from pod_mockup_forge.etsy_specs import EtsyPhotoAuditor, ETSY_PHOTO_CAROUSEL_STRATEGY
from pod_mockup_forge.mcp_server import handle_call_tool, TOOLS

class TestPODMockupForge(unittest.TestCase):
    """Rigorous test suite for POD Mockup Forge core engines."""

    def test_templates_registry(self):
        """Verify all 8 core templates exist and possess valid dimensions and colors."""
        templates = get_all_templates()
        self.assertEqual(len(templates), 8)

        expected_ids = [
            "gildan_18000_flatlay",
            "comfort_colors_1717_hanger",
            "bella_canvas_3001_model",
            "ceramic_mug_15oz_kitchen",
            "canvas_gallery_wrap_livingroom",
            "matte_poster_wood_frame",
            "canvas_tote_farmers_market",
            "phone_case_flatlay"
        ]
        for tid in expected_ids:
            tpl = get_template(tid)
            self.assertIsNotNone(tpl, f"Template {tid} must exist in registry")
            self.assertIn(tpl.aspect_ratio, ["1:1", "4:3"])
            self.assertGreaterEqual(tpl.canvas_width, 2000)
            self.assertGreaterEqual(tpl.canvas_height, 2000)
            self.assertTrue(len(tpl.supported_colors) >= 1)
            self.assertTrue(tpl.print_area.width_percent > 0)
            self.assertTrue(tpl.print_area.height_percent > 0)

    def test_composite_engine_aspect_fit(self):
        """Test bounding box aspect fit calculations for various image proportions."""
        # Square art into tall box
        fit1 = MockupCompositeEngine.calculate_aspect_fit(
            art_w=1000, art_h=1000, target_w=800, target_h=1000
        )
        self.assertEqual(fit1["width"], 800)
        self.assertEqual(fit1["height"], 800)
        self.assertEqual(fit1["offset_x"], 0)
        self.assertEqual(fit1["offset_y"], 100.0)

        # Wide art into square box
        fit2 = MockupCompositeEngine.calculate_aspect_fit(
            art_w=1600, art_h=800, target_w=800, target_h=800
        )
        self.assertEqual(fit2["width"], 800)
        self.assertEqual(fit2["height"], 400)
        self.assertEqual(fit2["offset_x"], 0)
        self.assertEqual(fit2["offset_y"], 200.0)


    def test_composite_engine_render_scene(self):
        """Verify vector SVG mockup generation with color customization and watermarks."""
        spec = MockupCompositeEngine.render_scene_spec(
            template_id="gildan_18000_flatlay",
            artwork_url="https://nullai.tech/artwork/vintage_sun.png",
            color_hex="#2D4233",
            watermark=True
        )
        self.assertEqual(spec["template_id"], "gildan_18000_flatlay")
        self.assertEqual(spec["selected_color"], "#2D4233")
        self.assertTrue(spec["watermark_applied"])
        self.assertIn("<svg", spec["svg_preview"])
        self.assertIn("SAMPLE PREVIEW", spec["svg_preview"])
        self.assertIn("vintage_sun.png", spec["svg_preview"])

    def test_etsy_photo_auditor_compliance(self):
        """Verify Etsy 2026 photo standards evaluation."""
        # Perfect 1:1 image
        audit_1_1 = EtsyPhotoAuditor.audit_image(2000, 2000, 3.2)
        self.assertTrue(audit_1_1["is_compliant"])
        self.assertEqual(audit_1_1["compliance_score"], 100)
        self.assertEqual(len(audit_1_1["issues"]), 0)

        # Perfect 4:3 optimal image
        audit_4_3 = EtsyPhotoAuditor.audit_image(2700, 2025, 4.5)
        self.assertTrue(audit_4_3["is_compliant"])
        self.assertEqual(audit_4_3["compliance_score"], 100)

        # Undersized image (< 2000px)
        audit_low_res = EtsyPhotoAuditor.audit_image(1200, 1200, 1.5)
        self.assertFalse(audit_low_res["is_compliant"])
        self.assertGreater(len(audit_low_res["issues"]), 0)
        self.assertLess(audit_low_res["compliance_score"], 80)

        # Oversized file (> 20MB)
        audit_huge = EtsyPhotoAuditor.audit_image(3000, 3000, 25.5)
        self.assertFalse(audit_huge["is_compliant"])
        self.assertIn("exceeds Etsy's 20MB upload ceiling", audit_huge["issues"][0])

    def test_etsy_10_slot_carousel(self):
        """Verify the standard 10-slot Etsy carousel listing strategy."""
        plan = EtsyPhotoAuditor.generate_listing_pack_plan("Bella Canvas 3001")
        self.assertEqual(plan["total_slots"], 10)
        self.assertEqual(len(plan["slots"]), 10)
        slots = plan["slots"]
        self.assertEqual(slots[0]["title"], "Primary Hero Image")
        self.assertTrue(slots[0]["mandatory"])
        self.assertEqual(slots[1]["title"], "Secondary Lifestyle Angle")
        self.assertTrue(slots[3]["mandatory"])  # Sizing chart

    def test_mcp_tools(self):
        """Verify all 6 MCP JSON-RPC tools execute properly."""
        self.assertEqual(len(TOOLS), 6)

        # 1. mockup_list_templates
        res1 = handle_call_tool("mockup_list_templates", {"category": "apparel"})
        self.assertGreaterEqual(res1["count"], 3)

        # 2. mockup_generate_scene
        res2 = handle_call_tool("mockup_generate_scene", {
            "template_id": "comfort_colors_1717_hanger",
            "artwork_url": "https://nullai.tech/art.png"
        })
        self.assertEqual(res2["status"], "success")
        self.assertIn("scene_spec", res2)

        # 3. mockup_calculate_aspect_fit
        res3 = handle_call_tool("mockup_calculate_aspect_fit", {
            "artwork_width": 1000,
            "artwork_height": 1500,
            "target_width": 500,
            "target_height": 500
        })
        self.assertIn("aspect_metrics", res3)
        self.assertEqual(res3["aspect_metrics"]["height"], 500)

        # 4. mockup_batch_generate_listing_pack
        res4 = handle_call_tool("mockup_batch_generate_listing_pack", {"product_type": "mug"})
        self.assertEqual(len(res4["listing_pack"]["slots"]), 10)

        # 5. mockup_audit_etsy_compliance
        res5 = handle_call_tool("mockup_audit_etsy_compliance", {
            "width_px": 2700,
            "height_px": 2025,
            "file_size_mb": 4.1
        })
        self.assertTrue(res5["etsy_audit"]["is_compliant"])

        # 6. mockup_add_watermark_protection
        res6 = handle_call_tool("mockup_add_watermark_protection", {
            "canvas_width": 2000,
            "canvas_height": 2000,
            "watermark_text": "SOVEREIGN ART"
        })
        self.assertEqual(res6["status"], "success")
        self.assertIn("SOVEREIGN ART", res6["svg_overlay"])

if __name__ == "__main__":
    unittest.main()
