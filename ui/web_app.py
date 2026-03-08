import os
import sys
import shutil
import subprocess
import webview
import base64
import plistlib
from io import BytesIO
from pathlib import Path
from PIL import Image, IcnsImagePlugin
Image.register_open(IcnsImagePlugin.IcnsImageFile.format, IcnsImagePlugin.IcnsImageFile)
Image.register_extension(IcnsImagePlugin.IcnsImageFile.format, ".icns")
Image.register_mime(IcnsImagePlugin.IcnsImageFile.format, "image/icns")
from scanner import list_installed_apps, find_orphaned_files, scan_app, FoundFile
from cleaner import trash_files
from system_junk import scan_system_junk, scan_large_files, scan_dev_junk, scan_trash


LAUNCH_AGENT_LABEL = "com.macsweeper.openatlogin"


_BLOCKED_EXACT_PATHS = {
    Path("/"),
    Path.home(),
    Path("/System"),
    Path("/usr"),
    Path("/bin"),
    Path("/sbin"),
    Path("/etc"),
    Path("/Applications"),
    Path("/Library"),
    Path("/private"),
    Path("/private/var"),
}


def _is_safe_clean_target(resolved: Path, category: str, allowed_prefixes: tuple[str, ...]) -> bool:
    """Defensive path filter to avoid accidental deletion of critical paths."""
    resolved_str = str(resolved)

    if resolved in _BLOCKED_EXACT_PATHS:
        return False

    if not resolved_str.startswith(allowed_prefixes):
        return False

    # Allow app bundles inside /Applications, but never arbitrary non-app entries.
    is_app_bundle_in_applications = False
    if resolved_str.startswith("/Applications/"):
        lower_cat = (category or "").lower()
        is_app_bundle_in_applications = resolved_str.endswith(".app") and lower_cat == "application"
        if not is_app_bundle_in_applications:
            return False

    # Ignore unexpectedly shallow paths such as /Users/<name>/Documents itself.
    if len(resolved.parts) < 4 and not is_app_bundle_in_applications:
        return False

    return True


def _is_trash_path(path: Path) -> bool:
    path_str = str(path)
    home_trash = str(Path.home() / ".Trash")
    return path_str.startswith(home_trash) or "/.Trashes/" in path_str


def _trash_roots() -> list[Path]:
    roots: list[Path] = []
    home_root = Path.home() / ".Trash"
    roots.append(home_root)

    uid = str(os.getuid())
    volumes_root = Path("/Volumes")
    if volumes_root.exists() and volumes_root.is_dir():
        try:
            for vol in volumes_root.iterdir():
                if not vol.is_dir():
                    continue
                roots.append(vol / ".Trashes" / uid)
        except OSError:
            pass

    return roots


def _find_trashed_item_for_original(original_path: Path) -> Path | None:
    """Best-effort search for the trashed counterpart of an original path."""
    target_name = original_path.name
    if not target_name:
        return None

    candidates: list[Path] = []
    for root in _trash_roots():
        if not root.exists() or not root.is_dir():
            continue
        try:
            for entry in root.iterdir():
                name = entry.name
                if name == target_name or name.startswith(target_name + " "):
                    candidates.append(entry)
        except OSError:
            continue

    if not candidates:
        return None

    try:
        return max(candidates, key=lambda p: p.stat().st_mtime)
    except OSError:
        return candidates[0]


def _resolve_restore_destination(original_path: Path) -> Path:
    """Return a non-conflicting destination path for restore."""
    if not original_path.exists():
        return original_path

    parent = original_path.parent
    stem = original_path.stem
    suffix = original_path.suffix

    for i in range(1, 200):
        candidate = parent / f"{stem} (restored {i}){suffix}"
        if not candidate.exists():
            return candidate

    return parent / f"{stem} (restored){suffix}"


def _launch_agent_path() -> Path:
    return Path.home() / "Library" / "LaunchAgents" / f"{LAUNCH_AGENT_LABEL}.plist"


def _main_script_path() -> Path:
    # ui/web_app.py -> ui -> macsweeper root
    return Path(__file__).resolve().parent.parent / "main.py"


def _is_frozen_build() -> bool:
    return bool(getattr(sys, "frozen", False))


def _web_root_path() -> Path:
    """Resolve UI web assets for both source and py2app/PyInstaller builds."""
    if _is_frozen_build():
        # PyInstaller uses _MEIPASS
        if hasattr(sys, "_MEIPASS"):
            bundle_root = Path(sys._MEIPASS)
            return bundle_root / "ui" / "web"
        # py2app uses sys.executable which is within Contents/MacOS/
        # Resources are in Contents/Resources
        executable_path = Path(sys.executable).resolve()
        contents_dir = executable_path.parent.parent
        return contents_dir / "Resources" / "ui" / "web"
    return Path(__file__).resolve().parent / "web"


def _build_launch_agent_payload() -> dict:
    if _is_frozen_build():
        program_args = [sys.executable]
        working_dir = str(Path(sys.executable).resolve().parent)
    else:
        program_args = [sys.executable, str(_main_script_path())]
        working_dir = str(_main_script_path().parent)

    return {
        "Label": LAUNCH_AGENT_LABEL,
        "ProgramArguments": program_args,
        "RunAtLoad": True,
        "KeepAlive": False,
        "WorkingDirectory": working_dir,
        "StandardOutPath": str(Path.home() / "Library" / "Logs" / "macsweeper-launchd.log"),
        "StandardErrorPath": str(Path.home() / "Library" / "Logs" / "macsweeper-launchd.err.log"),
    }


def _launchctl_bootstrap(plist_path: Path):
    uid = str(os.getuid())
    subprocess.run(
        ["launchctl", "bootstrap", f"gui/{uid}", str(plist_path)],
        capture_output=True,
        timeout=8,
    )


def _launchctl_bootout(plist_path: Path):
    uid = str(os.getuid())
    subprocess.run(
        ["launchctl", "bootout", f"gui/{uid}", str(plist_path)],
        capture_output=True,
        timeout=8,
    )

def get_app_icon_base64(app_path_str: str) -> str:
    try:
        app_path = Path(app_path_str)
        info_plist = app_path / "Contents" / "Info.plist"
        if not info_plist.exists(): return ""
        with open(info_plist, "rb") as f:
            plist = plistlib.load(f)
        icon_file = plist.get("CFBundleIconFile")
        if not icon_file: return ""
        if not icon_file.endswith(".icns"): icon_file += ".icns"
        icns_path = app_path / "Contents" / "Resources" / icon_file
        if not icns_path.exists(): return ""
        
        img = Image.open(icns_path)
        img = img.resize((64, 64), Image.Resampling.LANCZOS)
        buffered = BytesIO()
        img.save(buffered, format="PNG")
        return "data:image/png;base64," + base64.b64encode(buffered.getvalue()).decode()
    except Exception as e:
        print(f"Image: failed to import - {e}")
        return ""

class Api:
    def __init__(self, window=None):
        self.window = window
        self._icon_cache: dict[str, str] = {}
        self._last_cleanup: list[dict] = []

    def get_apps(self):
        """Return list of installed applications."""
        # Startup path: keep this fast by skipping plist metadata parsing.
        apps = list_installed_apps(fast_mode=True)
        for a in apps:
            # Icons are loaded lazily by the frontend to avoid a blocked launch.
            a["icon_base64"] = ""
        return apps

    def get_app_icon(self, app_path: str):
        """Return a single app icon as base64 (lazy-loaded by UI)."""
        cached = self._icon_cache.get(app_path)
        if cached is not None:
            return {"icon_base64": cached}

        icon = get_app_icon_base64(app_path)
        self._icon_cache[app_path] = icon
        return {"icon_base64": icon}

    def reveal_path(self, path: str):
        """Reveal a path in Finder, or open parent if target is missing."""
        try:
            target = Path(path)
            if target.exists():
                subprocess.run(["open", "-R", str(target)], timeout=8, check=False)
                return {"ok": True}

            parent = target.parent if target.parent.exists() else Path.home()
            subprocess.run(["open", str(parent)], timeout=8, check=False)
            return {"ok": True}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def scan_app_leftovers(self, app_path):
        """Scan a specific app and return its leftovers grouped."""
        result = scan_app(app_path)
        
        grouped = {}
        for f in result.files:
            if f.category not in grouped:
                grouped[f.category] = []
            grouped[f.category].append({
                "path": str(f.path),
                "size_bytes": f.size_bytes,
                "display_size": f.display_size,
                "category": f.category
            })
            
        grouped_array = [{"category": k, "files": v} for k, v in grouped.items()]
        
        return {
            "app_name": result.app_name,
            "bundle_id": result.bundle_id,
            "groups": grouped_array,
            "total_size": result.total_display_size
        }

    def clean_files(self, files_data):
        """Move given files to Trash."""
        # Convert dict array back to FoundFile objects
        to_clean = []
        self._last_cleanup = []
        home = str(Path.home())
        allowed_prefixes = (
            home + "/Library/",
            home + "/.",
            home + "/Downloads/",
            home + "/Documents/",
            home + "/Desktop/",
            home + "/Movies/",
            "/Library/",
            "/private/var/",
            "/Applications/",
        )

        for fd in files_data:
            raw = fd["path"]
            category = fd.get("category", "")

            try:
                resolved_path = Path(raw).resolve()
            except OSError:
                continue

            if not _is_safe_clean_target(resolved_path, category, allowed_prefixes):
                continue  # skip potentially dangerous paths

            to_clean.append(FoundFile(
                path=Path(raw),
                size_bytes=fd["size_bytes"],
                category=category
            ))
        
        result = trash_files(to_clean)
        by_path = {str(Path(fd["path"])): fd for fd in files_data if "path" in fd}

        success_paths = [str(f.path) for f in result.success]
        for p in success_paths:
            fd = by_path.get(p)
            if not fd:
                continue
            original = Path(fd["path"])
            if _is_trash_path(original):
                continue
            self._last_cleanup.append({
                "path": str(original),
                "size_bytes": fd.get("size_bytes", 0),
                "category": fd.get("category", ""),
            })

        return {
            "freed_display": result.freed_display,
            "success_count": len(result.success),
            "failed_count": len(result.failed),
            "success_paths": success_paths,
            "failed_paths": [str(f.path) for f, _ in result.failed],
            "failed_reasons": [msg for _, msg in result.failed],
            "undo_available": len(self._last_cleanup) > 0,
        }

    def undo_last_cleanup(self):
        """Restore files from Trash for the last successful clean_files operation."""
        if not self._last_cleanup:
            return {
                "ok": False,
                "success_count": 0,
                "failed_count": 0,
                "message": "Nothing to undo.",
                "restored_paths": [],
                "failed_paths": [],
            }

        restored_paths: list[str] = []
        failed_paths: list[str] = []
        still_pending: list[dict] = []

        for item in self._last_cleanup:
            original = Path(item["path"])
            trashed = _find_trashed_item_for_original(original)
            if trashed is None:
                failed_paths.append(str(original))
                still_pending.append(item)
                continue

            try:
                destination = _resolve_restore_destination(original)
                destination.parent.mkdir(parents=True, exist_ok=True)
                shutil.move(str(trashed), str(destination))
                restored_paths.append(str(destination))
            except (OSError, PermissionError):
                failed_paths.append(str(original))
                still_pending.append(item)

        self._last_cleanup = still_pending

        return {
            "ok": len(restored_paths) > 0,
            "success_count": len(restored_paths),
            "failed_count": len(failed_paths),
            "restored_paths": restored_paths,
            "failed_paths": failed_paths,
            "undo_available": len(self._last_cleanup) > 0,
        }

    def empty_trash(self, files_data):
        """Permanently delete files from Trash."""
        import os
        import shutil

        def _path_exists_or_link(path: Path) -> bool:
            return os.path.lexists(str(path))

        def _delete_path(path: Path):
            if path.is_symlink():
                os.unlink(str(path))
            elif path.is_dir():
                shutil.rmtree(str(path))
            else:
                os.remove(str(path))

        def _force_delete_local(path: Path):
            """Try unlocking + deleting without admin privileges first."""
            try:
                subprocess.run(["chflags", "-R", "nouchg", str(path)], capture_output=True, timeout=8, check=False)
                subprocess.run(["chmod", "-R", "u+w", str(path)], capture_output=True, timeout=8, check=False)
            except Exception:
                pass
            _delete_path(path)

        def _force_delete_with_admin(path: Path) -> bool:
            script = (
                "on run argv\n"
                "set p to item 1 of argv\n"
                "do shell script \"chflags -R nouchg -- \" & quoted form of p & \"; "
                "chmod -R u+w -- \" & quoted form of p & \"; "
                "rm -rf -- \" & quoted form of p with administrator privileges\n"
                "end run"
            )
            try:
                subprocess.run(["osascript", "-e", script, str(path)], capture_output=True, timeout=20, check=False)
            except Exception:
                return False
            return not _path_exists_or_link(path)

        home = str(Path.home())
        trash_prefixes = (
            home + "/.Trash/",
            "/.Trashes/",
        )

        success_count = 0
        freed_bytes = 0
        success_paths = []
        permission_failed_paths = []
        failed_count = 0
        failed_paths = []
        failed_reasons = []

        for fd in files_data:
            raw = fd.get("path", "")
            if not raw:
                continue

            p = Path(raw).expanduser()
            raw_abs = str(p.absolute())

            # Only allow deletion of files actually in Trash
            if not any(raw_abs.startswith(prefix) or ("/.Trashes/" in raw_abs) for prefix in trash_prefixes):
                continue

            if not _path_exists_or_link(p):
                continue

            size = fd.get("size_bytes", 0)
            try:
                _delete_path(p)
                if not _path_exists_or_link(p):
                    success_count += 1
                    freed_bytes += size
                    success_paths.append(raw)
            except (OSError, PermissionError):
                try:
                    _force_delete_local(p)
                    if not _path_exists_or_link(p):
                        success_count += 1
                        freed_bytes += size
                        success_paths.append(raw)
                        continue
                except (OSError, PermissionError):
                    pass

                permission_failed_paths.append((p, size, raw))

        # Admin fallback for entries that resisted local force-delete.
        if permission_failed_paths:
            for p, size, raw in permission_failed_paths:
                if _force_delete_with_admin(p):
                    success_count += 1
                    freed_bytes += size
                    success_paths.append(raw)
                else:
                    failed_count += 1
                    failed_paths.append(raw)
                    failed_reasons.append("Permission denied")

        from utils.formatting import format_bytes
        return {
            "freed_display": format_bytes(freed_bytes),
            "success_count": success_count,
            "failed_count": failed_count,
            "success_paths": success_paths,
            "failed_paths": failed_paths,
            "failed_reasons": failed_reasons,
        }

    def get_orphans(self):
        """Find orphaned files from uninstalled apps."""
        groups = find_orphaned_files() # Returns list[OrphanGroup]
        return [
            {
               "app_name": g.inferred_name,
               "files": [
                   {
                        "path": str(f.path),
                        "size_bytes": f.size_bytes,
                        "display_size": f.display_size,
                        "category": f.category
                   } for f in g.files
               ]
            } for g in groups
        ]

    def get_system_junk(self):
        """Find user & system cache/log leftovers."""
        junk = scan_system_junk()
        return [
            {
                "path": str(f.path),
                "size_bytes": f.size_bytes,
                "display_size": f.display_size,
                "category": f.category
            } for f in junk
        ]
        
    def get_large_files(self, min_size_mb: int = 250):
        """Find very large files in user folders."""
        large = scan_large_files(min_size_mb=min_size_mb)
        return [
            {
                "path": str(f.path),
                "size_bytes": f.size_bytes,
                "display_size": f.display_size,
                "category": f.category
            } for f in large
        ]

    def get_dev_junk(self):
        """Find Developer specific heavy folders."""
        junk = scan_dev_junk()
        return [
            {
                "path": str(f.path),
                "size_bytes": f.size_bytes,
                "display_size": f.display_size,
                "category": f.category
            } for f in junk
        ]

    def get_trash(self):
        """Find files currently inside macOS Trash."""
        junk = scan_trash()
        return [
            {
                "path": str(f.path),
                "size_bytes": f.size_bytes,
                "display_size": f.display_size,
                "category": f.category
            } for f in junk
        ]

    def get_open_at_login_status(self):
        """Check whether launch-at-login is enabled for MacSweeper."""
        plist_path = _launch_agent_path()
        return {
            "enabled": plist_path.exists(),
            "path": str(plist_path),
        }

    def set_open_at_login(self, enabled: bool):
        """Enable or disable launch-at-login using a user LaunchAgent."""
        plist_path = _launch_agent_path()

        try:
            plist_path.parent.mkdir(parents=True, exist_ok=True)

            if enabled:
                payload = _build_launch_agent_payload()
                with open(plist_path, "wb") as f:
                    plistlib.dump(payload, f)
                _launchctl_bootout(plist_path)
                _launchctl_bootstrap(plist_path)
            else:
                if plist_path.exists():
                    _launchctl_bootout(plist_path)
                    plist_path.unlink(missing_ok=True)

            return {
                "ok": True,
                "enabled": enabled,
            }
        except Exception as e:
            return {
                "ok": False,
                "enabled": plist_path.exists(),
                "error": str(e),
            }

def run_web_app():
    api = Api()

    # Path to index.html (source tree or packaged bundle)
    html_path = _web_root_path() / 'index.html'
    
    window = webview.create_window(
        'MacSweeper Pro',
        f'file://{html_path}',
        js_api=api,
        width=1000,
        height=700,
        min_size=(800, 600),
        vibrancy=True,  # macOS native glassmorphism if available
        background_color='#1E1E1E' # Fallback background
    )
    api.window = window
    
    # Production-safe default; enable with MACSWEEPER_DEBUG=1 for local debugging.
    debug_mode = os.getenv("MACSWEEPER_DEBUG", "0") == "1"
    webview.start(debug=debug_mode)
