import subprocess
import tempfile
import unittest
from pathlib import Path


class SiteTest(unittest.TestCase):
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
            self.assertNotIn('Learn by investigating', home)
            self.assertIn("Blocked", home)
            self.assertIn("data-md-color-scheme", home)
            styles = (Path(output) / "stylesheets" / "extra.css").read_text(encoding="utf-8")
            self.assertIn(".md-typeset .grid.cards > ul > li { border-radius: .75rem; padding: .9rem 1rem; }", styles)
            self.assertIn(".md-typeset .grid.cards > ul > li strong { display: inline; margin-bottom: 0; }", styles)
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


if __name__ == "__main__":
    unittest.main()
