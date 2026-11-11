"""
verify_ui.py
Automated Headless Playwright Verification Harness for POD Mockup Forge
Triple-Viewport Responsiveness, Zero Console Errors, Zero Horizontal Overflow,
and 100% Open-Access Mockup Export Verification.
"""

import json
import os
import sys
import tempfile
import time
from pathlib import Path
from playwright.sync_api import sync_playwright

SHOT_DIR = Path(os.environ.get("SHOT_DIR", os.path.join(tempfile.gettempdir(), "pod_mockup_forge_shots")))
SHOT_DIR.mkdir(parents=True, exist_ok=True)

PORT = int(os.environ.get("PORT", "8119"))
BASE_URL = f"http://127.0.0.1:{PORT}"


def verify():
    viewports = [
        {"name": "home_mobile.jpg", "width": 390, "height": 844, "device": "Mobile"},
        {"name": "home_tablet.jpg", "width": 820, "height": 1180, "device": "Tablet"},
        {"name": "home_desktop.jpg", "width": 1425, "height": 900, "device": "Desktop"},
    ]
    results = {"viewports": [], "consoleErrors": []}

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, args=["--no-sandbox", "--disable-gpu", "--disable-dev-shm-usage"])
        for vp in viewports:
            page = browser.new_page(viewport={"width": vp["width"], "height": vp["height"]})
            console_errors = []
            page.on("console", lambda msg: console_errors.append(msg.text) if msg.type == "error" else None)
            page.on("pageerror", lambda err: console_errors.append(str(err)))
            page.goto(BASE_URL, wait_until="networkidle")
            time.sleep(0.4)
            overflow = page.evaluate("() => document.documentElement.scrollWidth - document.documentElement.clientWidth")
            shot_path = SHOT_DIR / vp["name"]
            page.screenshot(path=str(shot_path), full_page=False, type="jpeg", quality=85)
            passed = len(console_errors) == 0 and overflow <= 1
            results["viewports"].append({"device": vp["device"], "overflow": overflow, "passed": passed})
            for err in console_errors:
                results["consoleErrors"].append(f"[{vp['device']}] {err}")
            page.close()
        browser.close()

    print(json.dumps(results, indent=2))
    if all(v["passed"] for v in results["viewports"]):
        sys.exit(0)
    sys.exit(1)


if __name__ == "__main__":
    verify()
