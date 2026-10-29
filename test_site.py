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
            "docs/images/lab-29/bugbazaar-synthetic-address.png",
            "docs/images/lab-29/ordinary-app-provider-result.png",
        )

        for required_file in required_files:
            with self.subTest(path=required_file):
                self.assertTrue((root / required_file).is_file())


if __name__ == "__main__":
    unittest.main()
