import importlib
import sys
import types
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from cleaner import CleanResult
from scanner import FoundFile


def _load_web_app_module():
    webview_stub = types.ModuleType("webview")
    webview_stub.create_window = lambda *args, **kwargs: object()
    webview_stub.start = lambda *args, **kwargs: None

    class _ImageStub:
        class Resampling:
            LANCZOS = 1

        @staticmethod
        def open(*_args, **_kwargs):
            raise RuntimeError("Image loading is not needed in this test")

    pil_stub = types.ModuleType("PIL")
    pil_stub.Image = _ImageStub

    with patch.dict(sys.modules, {"webview": webview_stub, "PIL": pil_stub}):
        if "ui.web_app" in sys.modules:
            del sys.modules["ui.web_app"]
        return importlib.import_module("ui.web_app")


class WebApiTests(unittest.TestCase):
    def test_api_clean_files_sends_only_given_items(self):
        web_app = _load_web_app_module()
        api = web_app.Api()

        home = str(Path.home())
        files_data = [
            {"path": f"{home}/Library/Caches/test_a", "size_bytes": 10, "category": "Cache"},
            {"path": f"{home}/Library/Caches/test_b", "size_bytes": 20, "category": "Log"},
        ]

        captured = {}

        def fake_trash(files):
            captured["files"] = files
            return CleanResult(success=files[:1], failed=[])

        with patch.object(web_app, "trash_files", side_effect=fake_trash):
            result = api.clean_files(files_data)

        self.assertEqual(len(captured["files"]), 2)
        self.assertTrue(all(isinstance(item, FoundFile) for item in captured["files"]))
        self.assertEqual([str(item.path) for item in captured["files"]], [f"{home}/Library/Caches/test_a", f"{home}/Library/Caches/test_b"])
        self.assertEqual(result["success_count"], 1)
        self.assertTrue(result["undo_available"])

    def test_api_clean_files_returns_failed_paths_and_reasons(self):
        web_app = _load_web_app_module()
        api = web_app.Api()

        home = str(Path.home())
        files_data = [
            {"path": f"{home}/Library/Caches/test_ok", "size_bytes": 10, "category": "Cache"},
            {"path": f"{home}/Library/Caches/test_fail", "size_bytes": 20, "category": "Cache"},
        ]

        def fake_trash(files):
            return CleanResult(success=[files[0]], failed=[(files[1], "Permission denied")])

        with patch.object(web_app, "trash_files", side_effect=fake_trash):
            result = api.clean_files(files_data)

        self.assertEqual(result["success_count"], 1)
        self.assertEqual(result["failed_count"], 1)
        self.assertEqual(result["failed_paths"], [f"{home}/Library/Caches/test_fail"])
        self.assertEqual(result["failed_reasons"], ["Permission denied"])

    def test_api_undo_last_cleanup_restores_from_trash(self):
        web_app = _load_web_app_module()
        api = web_app.Api()

        home = str(Path.home())
        original_path = f"{home}/Library/Caches/test_restore"
        files_data = [
            {"path": original_path, "size_bytes": 10, "category": "Cache"},
        ]

        def fake_trash(files):
            return CleanResult(success=files, failed=[])

        with patch.object(web_app, "trash_files", side_effect=fake_trash):
            clean_result = api.clean_files(files_data)

        self.assertTrue(clean_result["undo_available"])

        with patch.object(web_app, "_find_trashed_item_for_original", return_value=Path("/tmp/trashed_test_restore")), \
             patch.object(web_app.shutil, "move") as mocked_move:
            undo_result = api.undo_last_cleanup()

        self.assertTrue(undo_result["ok"])
        self.assertEqual(undo_result["success_count"], 1)
        self.assertEqual(undo_result["failed_count"], 0)
        self.assertFalse(undo_result["undo_available"])
        mocked_move.assert_called_once()


    def test_api_scan_app_leftovers_groups_by_category(self):
        web_app = _load_web_app_module()
        api = web_app.Api()

        fake_files = [
            FoundFile(path=Path("/tmp/a"), size_bytes=100, category="Cache"),
            FoundFile(path=Path("/tmp/b"), size_bytes=200, category="Cache"),
            FoundFile(path=Path("/tmp/c"), size_bytes=50, category="Preferences"),
        ]

        class _ScanResult:
            app_name = "DemoApp"
            bundle_id = "com.demo.app"
            files = fake_files
            total_display_size = "350 B"

        with patch.object(web_app, "scan_app", return_value=_ScanResult()):
            result = api.scan_app_leftovers("/Applications/DemoApp.app")

        self.assertEqual(result["app_name"], "DemoApp")
        self.assertEqual(result["bundle_id"], "com.demo.app")
        categories = {g["category"]: g["files"] for g in result["groups"]}
        self.assertIn("Cache", categories)
        self.assertEqual(len(categories["Cache"]), 2)
        self.assertIn("Preferences", categories)
        self.assertEqual(len(categories["Preferences"]), 1)

    def test_api_clean_files_blocks_dangerous_root_paths(self):
        web_app = _load_web_app_module()
        api = web_app.Api()

        files_data = [
            {"path": "/", "size_bytes": 1, "category": "System"},
            {"path": "/Applications", "size_bytes": 1, "category": "Application"},
        ]

        captured = {}

        def fake_trash(files):
            captured["files"] = files
            return CleanResult(success=[], failed=[])

        with patch.object(web_app, "trash_files", side_effect=fake_trash):
            api.clean_files(files_data)

        self.assertEqual(captured["files"], [])

    def test_api_clean_files_allows_app_bundle_in_applications(self):
        web_app = _load_web_app_module()
        api = web_app.Api()

        files_data = [
            {"path": "/Applications/FakeApp.app", "size_bytes": 123, "category": "Application"},
        ]

        captured = {}

        def fake_trash(files):
            captured["files"] = files
            return CleanResult(success=[], failed=[])

        with patch.object(web_app, "trash_files", side_effect=fake_trash):
            api.clean_files(files_data)

        self.assertEqual(len(captured["files"]), 1)
        self.assertEqual(str(captured["files"][0].path), "/Applications/FakeApp.app")

    def test_api_empty_trash_missing_items_are_not_failed(self):
        web_app = _load_web_app_module()
        api = web_app.Api()

        missing_path = str(Path.home() / ".Trash" / "__macsweeper_missing_test_item__")
        files_data = [
            {"path": missing_path, "size_bytes": 1234, "category": "System Trash"},
        ]

        result = api.empty_trash(files_data)

        self.assertEqual(result["success_count"], 0)
        self.assertEqual(result["failed_count"], 0)
        self.assertEqual(result["success_paths"], [])

    def test_api_empty_trash_deletes_broken_symlink(self):
        web_app = _load_web_app_module()
        api = web_app.Api()

        with tempfile.TemporaryDirectory() as tmp:
            fake_home = Path(tmp)
            trash_dir = fake_home / ".Trash"
            trash_dir.mkdir(parents=True, exist_ok=True)

            broken_link = trash_dir / "broken-link"
            broken_link.symlink_to(fake_home / "missing-target")

            files_data = [
                {"path": str(broken_link), "size_bytes": 0, "category": "System Trash"},
            ]

            with patch.object(web_app.Path, "home", return_value=fake_home):
                result = api.empty_trash(files_data)

            self.assertEqual(result["success_count"], 1)
            self.assertEqual(result["failed_count"], 0)
            self.assertFalse(broken_link.exists())

    def test_api_reveal_path_existing_uses_open_reveal(self):
        web_app = _load_web_app_module()
        api = web_app.Api()

        existing_path = str(Path(__file__).resolve())

        with patch.object(web_app.subprocess, "run") as mocked_run:
            result = api.reveal_path(existing_path)

        self.assertTrue(result["ok"])
        mocked_run.assert_called_once_with(["open", "-R", existing_path], timeout=8, check=False)

    def test_api_reveal_path_missing_opens_parent_folder(self):
        web_app = _load_web_app_module()
        api = web_app.Api()

        missing_path = str(Path("/tmp") / "__macsweeper_missing_path_for_reveal__")

        with patch.object(web_app.subprocess, "run") as mocked_run:
            result = api.reveal_path(missing_path)

        self.assertTrue(result["ok"])
        mocked_run.assert_called_once_with(["open", "/tmp"], timeout=8, check=False)




if __name__ == "__main__":
    unittest.main()
