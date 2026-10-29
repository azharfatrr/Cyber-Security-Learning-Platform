import re
import subprocess
import tempfile
import unittest
from urllib.parse import unquote, urlsplit
from pathlib import Path


class SiteTest(unittest.TestCase):
    def test_pages_workflow_builds_before_deploying_main(self):
        root = Path(__file__).parent
        workflow_path = root / ".github" / "workflows" / "deploy.yml"
        self.assertTrue(workflow_path.is_file())
        workflow = workflow_path.read_text(encoding="utf-8")
        self.assertIn("on:\n  push:\n    branches:\n      - main", workflow)
        self.assertIn("python -m unittest -v test_site", workflow)
        self.assertIn("python -m mkdocs build --strict", workflow)
        self.assertIn("needs: build", workflow)
        self.assertIn("pages: write", workflow)
        self.assertIn("id-token: write", workflow)
        self.assertIn("actions: read", workflow)
        self.assertIn("cancel-in-progress: false", workflow)
        self.assertIn("actions/deploy-pages@v5", workflow)
        publishing = (root / "PUBLISHING.txt").read_text(encoding="utf-8")
        self.assertIn("GitHub Actions", publishing)
        self.assertIn("main", publishing)

    def test_github_readme_is_plain_markdown_and_mkdocs_home_is_index(self):
        root = Path(__file__).parent
        readme_path = root / "README.md"
        self.assertTrue(readme_path.is_file())
        readme = readme_path.read_text(encoding="utf-8")
        self.assertIn("# Cyber Security Learning Platform", readme)
        self.assertIn("python3 -m mkdocs serve", readme)
        self.assertNotIn("<div", readme)
        self.assertNotIn(".md-button", readme)
        self.assertIn("  - Home: index.md", (root / "mkdocs.yml").read_text(encoding="utf-8"))

    def test_build_contains_all_labs_and_collapsed_hints(self):
        root = Path(__file__).parent
        with tempfile.TemporaryDirectory() as output:
            result = subprocess.run(
                ["python", "-m", "mkdocs", "build", "--strict", "--site-dir", output],
                cwd=root, capture_output=True, text=True,
            )
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            home = (Path(output) / "index.html").read_text(encoding="utf-8")
            self.assertIn('class="grid cards auth-cards"', home)
            self.assertIn('class="catalog-hero"', home)
            self.assertIn('CYBER SECURITY LEARNING PLATFORM', home)
            self.assertNotIn('ANDROID INTERMEDIATE CLASS', home)
            self.assertIn('aria-label="Jump to a lab category"', home)
            self.assertIn('href="#authentication"', home)
            self.assertIn('>Security Labs</span>', home)
            self.assertIn('class="card-meta"', home)
            self.assertIn('<span class="card-meta">BugBazaar · Blocked</span>', home)
            self.assertNotIn('Learn by investigating', home)
            self.assertIn("Blocked", home)
            self.assertIn("data-md-color-scheme", home)
            styles = (Path(output) / "stylesheets" / "extra.css").read_text(encoding="utf-8")
            self.assertIn(".md-typeset .grid.cards > ul > li { border-radius: .75rem; padding: .9rem 1rem; }", styles)
            self.assertIn(".md-typeset .grid.cards > ul > li strong { display: inline; margin-bottom: 0; }", styles)
            self.assertIn(".md-typeset .grid.cards > ul > li .card-meta { font-size: .86em; color: #6b7280; }", styles)
            self.assertIn('[data-md-color-scheme="slate"] .md-typeset .grid.cards > ul > li .card-meta { color: #909ba6; }', styles)
            html = (Path(output) / "09-jwt-account-state" / "index.html").read_text(encoding="utf-8")
            self.assertIn("<details", html)
            self.assertIn("<summary>Hints</summary>", html)
            for number in (9, 10, 14, 24, 25, 26, 27, 28, 29, 30):
                self.assertIn(f"{number:02} —", html)
            pages = list((root / "docs").glob("[0-9][0-9]-*.md"))
            for page in pages:
                if page.name.startswith("00-"):
                    continue
                lab = (Path(output) / page.stem / "index.html").read_text(encoding="utf-8")
                self.assertIn("<summary>Hints</summary>", lab, page.name)
            cloud = (Path(output) / "27-cloud-database" / "index.html").read_text(encoding="utf-8")
            self.assertIn("not a runnable lab", cloud)

    def test_module_29_screenshots_are_copied_into_site(self):
        root = Path(__file__).parent
        with tempfile.TemporaryDirectory() as output:
            result = subprocess.run(
                ["python", "-m", "mkdocs", "build", "--strict", "--site-dir", output],
                cwd=root, capture_output=True, text=True,
            )
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            html_path = Path(output) / "29-components" / "index.html"
            html = html_path.read_text(encoding="utf-8")
            image_sources = re.findall(
                r'<img\b[^>]*\bsrc=["\']([^"\']*images/lab-29/[^"\']+)["\']',
                html,
            )
            self.assertTrue(image_sources, "module 29 should reference at least one lab screenshot")

            for source in image_sources:
                image_path = unquote(urlsplit(source).path)
                if image_path.startswith("/"):
                    generated_image = Path(output) / image_path.lstrip("/")
                else:
                    generated_image = html_path.parent / image_path
                self.assertTrue(generated_image.is_file(), source)

    def test_module_29_verifies_installed_target_hash(self):
        root = Path(__file__).parent
        guide = (root / "docs" / "29-components.md").read_text(encoding="utf-8")
        self.assertIn("INSTALLED_APK", guide)
        self.assertIn("EXPECTED_SHA=c307c7856b270da40357006eaa763c06bcdc2913d0d0b0bab7e0b2ed564f5f4c", guide)
        self.assertIn('shell sha256sum "$INSTALLED_APK"', guide)
        self.assertIn('if [ "$INSTALLED_SHA" != "$EXPECTED_SHA" ]; then', guide)

    def test_module_29_preserves_existing_target_preferences(self):
        root = Path(__file__).parent
        guide = (root / "docs" / "29-components.md").read_text(encoding="utf-8")
        self.assertIn("if [ -e shared_prefs/MyAppPreferences.xml ]", guide)
        self.assertGreaterEqual(guide.count("grep -Fq"), 2)
        self.assertIn("isFirstRun=false", guide)
        self.assertIn("Existing preferences are never overwritten", guide)

    def test_module_29_fails_closed_on_checksum_or_install_error(self):
        root = Path(__file__).parent
        guide = (root / "docs" / "29-components.md").read_text(encoding="utf-8")
        bash_blocks = re.findall(r"```bash\n(.*?)\n```", guide, re.DOTALL)
        target_block = next(block for block in bash_blocks if "BugBazaar_v1.2.1.apk" in block)
        caller_block = next(block for block in bash_blocks if "module-29-caller.apk" in block)
        self.assertIn("set -euo pipefail", target_block)
        self.assertIn("set -euo pipefail", caller_block)
        self.assertIn("CALLER_EXPECTED_SHA=eedfec951335a8ed876241d86bc9e6c53a7dff4833b98fa522f8cbfc1168900e", caller_block)
        self.assertLess(target_block.index("sha256sum --check -"), target_block.index('adb -s "$SERIAL" install'))
        self.assertLess(caller_block.index("sha256sum --check -"), caller_block.index("CALLER_INSTALLED_APK"))
        self.assertLess(caller_block.index('adb -s "$SERIAL" install'), caller_block.index("am start"))
        self.assertIn('if [ "$CALLER_INSTALLED_SHA" != "$CALLER_EXPECTED_SHA" ]; then', caller_block)

    def test_module_29_requires_all_network_transports_off(self):
        root = Path(__file__).parent
        guide = (root / "docs" / "29-components.md").read_text(encoding="utf-8")
        self.assertIn("cmd wifi status", guide)
        self.assertIn("Wifi is disabled", guide)
        self.assertIn('if [ "$AIRPLANE_STATUS" != "enabled" ]', guide)
        self.assertIn('case "$WIFI_STATUS" in', guide)
        self.assertIn('case "$CONNECTIVITY_STATUS" in', guide)
        self.assertIn("mobile data", guide.lower())
        self.assertIn("USB or Bluetooth tethering", guide)
        self.assertIn("Active default network: none", guide)

    def test_module_29_reuses_existing_synthetic_marker(self):
        root = Path(__file__).parent
        guide = (root / "docs" / "29-components.md").read_text(encoding="utf-8")
        self.assertIn("Search Addresses for the exact nickname below before saving", guide)
        self.assertIn("If exactly one matching record exists, reuse it", guide)
        self.assertIn("If multiple matches appear or the result is uncertain, stop", guide)


if __name__ == "__main__":
    unittest.main()
