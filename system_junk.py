import os
import logging
import subprocess
from pathlib import Path
from scanner import FoundFile, _item_size

logger = logging.getLogger(__name__)

def scan_system_junk() -> list[FoundFile]:
    """Scan for user & system caches and logs."""
    junk = []
    seen: set[str] = set()
    
    # User Caches
    user_cache = Path.home() / "Library" / "Caches"
    _scan_dir_top_level(user_cache, "User Cache", junk, seen)
    
    # System Caches
    sys_cache = Path("/Library/Caches")
    _scan_dir_top_level(sys_cache, "System Cache", junk, seen)
    
    # User Logs
    user_logs = Path.home() / "Library" / "Logs"
    _scan_dir_top_level(user_logs, "User Log", junk, seen)
    
    # System Logs
    sys_logs = Path("/var/log")
    _scan_dir_top_level(sys_logs, "System Log", junk, seen)
    
    # Sort strictly by size descending for a better user experience
    junk.sort(key=lambda x: x.size_bytes, reverse=True)
    return junk

def scan_dev_junk() -> list[FoundFile]:
    """Scan for Xcode DerivedData, Archives, iOS Backups."""
    junk = []
    seen: set[str] = set()
    _scan_dir_top_level(Path.home() / "Library/Developer/Xcode/DerivedData", "Xcode Derived Data", junk, seen)
    _scan_dir_top_level(Path.home() / "Library/Developer/Xcode/Archives", "Xcode Archives", junk, seen)
    _scan_dir_top_level(Path.home() / "Library/Application Support/MobileSync/Backup", "iOS Backup", junk, seen)
    _scan_dir_top_level(Path.home() / "Library/Application Support/CrashReporter", "Crash Reports", junk, seen)
    junk.sort(key=lambda x: x.size_bytes, reverse=True)
    return junk

def scan_trash() -> list[FoundFile]:
    """Scan user and mounted volume Trash locations."""
    junk: list[FoundFile] = []
    seen_paths: set[str] = set()

    # Primary user trash
    _scan_trash_root(Path.home() / ".Trash", "System Trash", junk, seen_paths)

    # External / secondary volume trashes: /Volumes/<Volume>/.Trashes/<uid>
    uid = str(os.getuid())
    volumes_root = Path("/Volumes")
    if volumes_root.exists() and volumes_root.is_dir():
        try:
            for volume in volumes_root.iterdir():
                if not volume.is_dir():
                    continue
                volume_trash = volume / ".Trashes" / uid
                _scan_trash_root(
                    volume_trash,
                    f"Trash ({volume.name})",
                    junk,
                    seen_paths,
                )
        except (PermissionError, OSError):
            pass

    junk.sort(key=lambda x: x.size_bytes, reverse=True)
    return junk


def _scan_trash_root(folder: Path, category: str, results: list[FoundFile], seen: set[str]):
    """Scan a trash root without skipping hidden entries."""
    if not folder.exists() or not folder.is_dir():
        return

    try:
        for item in folder.iterdir():
            item_str = str(item)
            if item_str in seen:
                continue

            try:
                size = _item_size(item)
            except (PermissionError, OSError):
                continue

            if size > 0:
                results.append(FoundFile(path=item, size_bytes=size, category=category))
                seen.add(item_str)
    except PermissionError:
        # On recent macOS versions this directory can be protected unless the
        # app has Full Disk Access. Fallback to Finder to list visible Trash items.
        if category == "System Trash":
            _scan_trash_via_finder(category, results, seen)
    except OSError:
        pass


def _scan_trash_via_finder(category: str, results: list[FoundFile], seen: set[str]):
    """Fallback scan via Finder when direct Trash access is denied.

    Finder can often enumerate Trash items even when Python cannot access
    ~/.Trash directly due to TCC restrictions.
    """
    try:
        out = subprocess.check_output(
            [
                "osascript",
                "-e", 'tell application "Finder" to set itemNames to name of every item of trash',
                "-e", "set AppleScript's text item delimiters to linefeed",
                "-e", "set outText to itemNames as text",
                "-e", "set AppleScript's text item delimiters to \"\"",
                "-e", "return outText",
            ],
            stderr=subprocess.DEVNULL,
            timeout=12,
        ).decode(errors="ignore")
    except (subprocess.SubprocessError, OSError):
        return

    for line in out.splitlines():
        item_name = line.strip()
        if not item_name:
            continue

        # Most Finder trash entries correspond to ~/.Trash/<name>.
        p = Path.home() / ".Trash" / item_name
        p_str = str(p)
        if p_str in seen:
            continue

        try:
            size = _item_size(p)
        except (PermissionError, OSError):
            # Keep item visible even if precise size is blocked.
            size = 0

        results.append(FoundFile(path=p, size_bytes=size, category=category))
        seen.add(p_str)

def _scan_dir_top_level(folder: Path, category: str, results: list[FoundFile], seen: set[str]):
    """Scan top-level entries in a directory, skipping duplicates."""
    if not folder.exists() or not folder.is_dir():
        return
    try:
        for item in folder.iterdir():
            if item.name.startswith('.'):
                continue
            item_str = str(item)
            if item_str in seen:
                continue
            size = _item_size(item)
            if size > 0:
                results.append(FoundFile(path=item, size_bytes=size, category=category))
                seen.add(item_str)
    except (PermissionError, OSError):
        pass

def scan_large_files(min_size_mb: int = 250) -> list[FoundFile]:
    """Find files larger than `min_size_mb` in user's home directory."""
    large_files = []
    min_bytes = min_size_mb * 1024 * 1024
    
    home = Path.home()
    dirs_to_scan = [
        home / "Downloads",
        home / "Documents",
        home / "Desktop",
        home / "Movies"
    ]
    
    for d in dirs_to_scan:
        if d.exists() and d.is_dir():
            _find_large_in_dir(d, min_bytes, large_files)
            
    large_files.sort(key=lambda x: x.size_bytes, reverse=True)
    return large_files

def _find_large_in_dir(folder: Path, min_bytes: int, results: list[FoundFile], _depth: int = 0):
    """Find large files recursively with depth limit to prevent infinite loops."""
    if _depth > 15:
        return
    try:
        for entry in os.scandir(folder):
            # Skip hidden files
            if entry.name.startswith('.'):
                continue
                
            if entry.is_file(follow_symlinks=False):
                try:
                    size = entry.stat().st_size
                    if size >= min_bytes:
                        results.append(FoundFile(path=Path(entry.path), size_bytes=size, category="Large File"))
                except OSError:
                    pass
            elif entry.is_dir(follow_symlinks=False):
                # Treat .app or .dmg as files for cleaning purposes if large enough
                if entry.name.endswith(".app"):
                    try:
                        size = _item_size(Path(entry.path))
                        if size >= min_bytes:
                            results.append(FoundFile(path=Path(entry.path), size_bytes=size, category="Large App"))
                    except OSError:
                        pass
                else:
                    _find_large_in_dir(Path(entry.path), min_bytes, results, _depth + 1)
    except OSError:
        pass
