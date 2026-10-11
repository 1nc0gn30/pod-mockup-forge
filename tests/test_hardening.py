"""Security, validation and image-probe tests for POD Mockup Forge."""
import os, sys, subprocess, unittest, tempfile
SRC = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src"))
sys.path.insert(0, SRC)
from pod_mockup_forge.composite_engine import MockupCompositeEngine as E
from pod_mockup_forge.etsy_specs import EtsyPhotoAuditor as A
from pod_mockup_forge.templates import MOCKUP_TEMPLATES
from pod_mockup_forge.image_probe import probe_image

try:
    from PIL import Image
except ImportError:  # probe tests need Pillow only to *create* fixtures
    Image = None


class TestSvgSafety(unittest.TestCase):
    def test_rejects_script_urls_and_bad_colors(self):
        for url in ('javascript:alert(1)', 'https://x"/><script>alert(1)</script>', ''):
            with self.subTest(url=url), self.assertRaises(ValueError):
                E.render_scene_spec("gildan_18000_flatlay", url)
        with self.assertRaises(ValueError):
            E.render_scene_spec("gildan_18000_flatlay", "https://a/b.png", color_hex='#fff" onload="x')

    def test_urls_are_escaped_in_svg(self):
        svg = E.render_scene_spec("gildan_18000_flatlay", "https://cdn.example/a.png?x=1&y=2")["svg_preview"]
        self.assertIn('href="https://cdn.example/a.png?x=1&amp;y=2"', svg)

    def test_allowed_url_forms(self):
        for url in ("https://a.b/c.png", "http://localhost:8119/a.jpg", "data:image/png;base64,AAAA", "./art.png", "art.webp"):
            E.render_scene_spec("gildan_18000_flatlay", url)

    def test_unknown_template_raises(self):
        with self.assertRaises(ValueError):
            E.render_scene_spec("does_not_exist", "https://a/b.png")

    def test_every_template_renders_inside_canvas(self):
        for tid, t in MOCKUP_TEMPLATES.items():
            p = E.render_scene_spec(tid, "https://a/b.png", artwork_width=1800, artwork_height=2400)["placement"]
            self.assertGreaterEqual(p["x"], 0, tid)
            self.assertLessEqual(p["x"] + p["width"], t.canvas_width + 0.5, tid)
            self.assertLessEqual(p["y"] + p["height"], t.canvas_height + 0.5, tid)


class TestFitAndAudit(unittest.TestCase):
    def test_fit_contain_preserves_aspect(self):
        f = E.calculate_aspect_fit(4000, 2000, 1000, 1000)
        self.assertEqual((f["width"], f["height"], f["offset_y"]), (1000.0, 500.0, 250.0))
        c = E.calculate_aspect_fit(4000, 2000, 1000, 1000, mode="cover")
        self.assertEqual((c["width"], c["height"]), (2000.0, 1000.0))

    def test_fit_rejects_bad_input(self):
        for args in ((0, 10, 10, 10), (10, 10, -1, 10)):
            with self.assertRaises(ValueError):
                E.calculate_aspect_fit(*args)
        with self.assertRaises(ValueError):
            E.calculate_aspect_fit(1, 1, 1, 1, mode="stretch")

    def test_audit_zero_height_is_error_not_crash(self):
        with self.assertRaises(ValueError):
            A.audit_image(2000, 0)

    def test_audit_tiers(self):
        self.assertEqual(A.audit_image(2700, 2025, 4)["etsy_search_readiness"], "EXCELLENT")
        self.assertFalse(A.audit_image(1600, 1200, 1)["passed"])
        self.assertFalse(A.audit_image(3000, 3000, 25)["passed"])


@unittest.skipIf(Image is None, "Pillow not installed")
class TestImageProbe(unittest.TestCase):
    def test_probe_formats_match_pillow(self):
        with tempfile.TemporaryDirectory() as d:
            for fmt, ext, extra in (("PNG", "png", {}), ("JPEG", "jpg", {"progressive": True}), ("JPEG", "jpeg", {}),
                                    ("GIF", "gif", {}), ("WEBP", "webp", {}), ("WEBP", "lossless.webp", {"lossless": True})):
                path = os.path.join(d, f"t.{ext}")
                Image.new("RGB", (2701, 2026), "white").save(path, fmt, **extra)
                w, h, mb = probe_image(path)
                self.assertEqual((w, h), (2701, 2026), ext)
                self.assertGreater(mb, 0)

    def test_probe_rejects_non_image(self):
        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as f:
            f.write(b"not an image at all" * 4)
        try:
            with self.assertRaises(ValueError):
                probe_image(f.name)
        finally:
            os.unlink(f.name)

    def test_cli_audit_file(self):
        with tempfile.TemporaryDirectory() as d:
            path = os.path.join(d, "ok.png")
            Image.new("RGB", (2700, 2025)).save(path)
            out = subprocess.run([sys.executable, "-m", "pod_mockup_forge.cli", "audit", "--file", path],
                                 capture_output=True, text=True, env=dict(os.environ, PYTHONPATH=SRC))
            self.assertEqual(out.returncode, 0, out.stderr)
            self.assertIn("2700x2025", out.stdout)


if __name__ == "__main__":
    unittest.main()
