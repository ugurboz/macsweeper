from pathlib import Path
import unittest
from unittest.mock import patch

import scanner


class ScannerTests(unittest.TestCase):
    def test_matches_bundle_id_and_app_name(self):
        self.assertTrue(scanner._matches("com.example.myapp.helper", "com.example.myapp", "MyApp"))
        self.assertTrue(scanner._matches("group.com.example.myapp", "com.example.myapp", "MyApp"))
        self.assertTrue(scanner._matches("myapp-cache", None, "MyApp"))
        self.assertFalse(scanner._matches("unrelated-entry", "com.example.myapp", "MyApp"))


    def test_list_installed_apps_multi_root_and_dedup_sorted(self):
        home_apps_root = scanner.HOME / "Applications"

        by_root = {
            Path("/Applications"): [
                Path("/Applications/Zeta.app"),
                Path("/Applications/Alpha.app"),
            ],
            home_apps_root: [
                Path(str(home_apps_root / "Beta.app")),
                Path("/Applications/Alpha.app"),
            ],
            Path("/System/Applications"): [
                Path("/System/Applications/Gamma.app"),
            ],
        }

        def fake_iter(root: Path):
            return by_root.get(root, [])

        with patch("scanner._iter_app_bundles", side_effect=fake_iter), \
             patch("scanner.get_bundle_id", side_effect=lambda p: f"bid.{Path(p).stem.lower()}"), \
             patch("scanner.get_app_name", side_effect=lambda p: Path(p).stem):
            apps = scanner.list_installed_apps()

        names = [a["name"] for a in apps]
        paths = [a["path"] for a in apps]

        self.assertEqual(names, ["Alpha", "Beta", "Gamma", "Zeta"])
        self.assertEqual(len(paths), len(set(paths)))
        self.assertTrue(all(a["bundle_id"].startswith("bid.") for a in apps))


if __name__ == "__main__":
    unittest.main()
