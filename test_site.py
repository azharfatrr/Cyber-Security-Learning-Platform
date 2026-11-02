import unittest
from pathlib import Path


class SiteTest(unittest.TestCase):
    def test_required_documentation_and_lab_images_exist(self):
        root = Path(__file__).parent
        required_files = (
            "docs/index.md",
            "docs/00-common-setup.md",
            "docs/01-devom-setup.md",
            "docs/02-bugbazaar-setup.md",
            "docs/29-components.md",
            "docs/30-runtime-bypass.md",
            "docs/assets/apk/module-29-caller.apk",
            "docs/images/lab-29/bugbazaar-synthetic-address.png",
            "docs/images/lab-29/ordinary-app-provider-result.png",
            "docs/images/lab-30/passcode-rejected.png",
            "docs/images/lab-30/passcode-correct.png",
            "docs/images/lab-30/passcode-hook-success.png",
        )

        for required_file in required_files:
            with self.subTest(path=required_file):
                self.assertTrue((root / required_file).is_file())

    def test_user_facing_pages_do_not_mark_labs_as_pilots(self):
        root = Path(__file__).parent
        pages = [root / "README.md", root / "lab-expansion-plan.md"]
        pages.extend(
            path
            for path in (root / "docs").rglob("*.md")
            if "superpowers" not in path.parts
        )

        for page in pages:
            with self.subTest(path=str(page.relative_to(root))):
                self.assertNotIn("pilot", page.read_text().lower())

    def test_each_lab_has_a_key_observation_callout(self):
        root = Path(__file__).parent
        lab_pages = (
            "09-jwt-account-state.md",
            "10-otp-bypass.md",
            "14-command-injection.md",
            "24-file-upload.md",
            "25-path-traversal.md",
            "26-transactions.md",
            "27-cloud-database.md",
            "28-bola.md",
            "29-components.md",
            "30-runtime-bypass.md",
        )

        for lab_page in lab_pages:
            with self.subTest(path=lab_page):
                content = (root / "docs" / lab_page).read_text()
                self.assertIn('!!! important "Key observation"', content)

    def test_key_observation_callouts_use_orange_in_both_themes(self):
        root = Path(__file__).parent
        stylesheet = (root / "docs/stylesheets/extra.css").read_text()

        self.assertIn(".md-typeset .admonition.important", stylesheet)
        self.assertIn("#a75a07", stylesheet)
        self.assertIn('[data-md-color-scheme="slate"] .md-typeset .admonition.important', stylesheet)
        self.assertIn("#ffae54", stylesheet)

    def test_hints_are_nested_under_evidence_on_every_lab_page(self):
        root = Path(__file__).parent
        lab_pages = (
            "09-jwt-account-state.md",
            "10-otp-bypass.md",
            "14-command-injection.md",
            "24-file-upload.md",
            "25-path-traversal.md",
            "26-transactions.md",
            "27-cloud-database.md",
            "28-bola.md",
            "29-components.md",
            "30-runtime-bypass.md",
        )

        for lab_page in lab_pages:
            with self.subTest(path=lab_page):
                content = (root / "docs" / lab_page).read_text()
                evidence = content.index("## Evidence")
                hints = content.index("<summary>Hints</summary>")
                vulnerability = content.index("## Vulnerability and Impact")
                self.assertLess(evidence, hints)
                self.assertLess(hints, vulnerability)

    def test_target_setup_guides_use_restricted_egress_not_airplane_mode(self):
        root = Path(__file__).parent
        devom_setup = (root / "docs/01-devom-setup.md").read_text().lower()
        bugbazaar_setup = (root / "docs/02-bugbazaar-setup.md").read_text().lower()

        self.assertIn("network egress", devom_setup)
        self.assertIn("network egress", bugbazaar_setup)
        self.assertNotIn("airplane mode", bugbazaar_setup)
        self.assertNotIn("offline", bugbazaar_setup)

        for lab_page in ("27-cloud-database.md", "29-components.md", "30-runtime-bypass.md"):
            with self.subTest(path=lab_page):
                content = (root / "docs" / lab_page).read_text().lower()
                self.assertNotIn("keep the emulator offline", content)


if __name__ == "__main__":
    unittest.main()
