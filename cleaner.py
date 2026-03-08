"""Cleaner — moves selected files to Trash safely via send2trash."""

from __future__ import annotations

import os
import shutil
import subprocess
from dataclasses import dataclass
from pathlib import Path

from send2trash import send2trash

from scanner import FoundFile
from utils.formatting import format_bytes


@dataclass
class CleanResult:
    """Summary of a cleaning operation."""

    success: list[FoundFile]
    failed: list[tuple[FoundFile, str]]  # (file, error message)

    @property
    def freed_bytes(self) -> int:
        return sum(f.size_bytes for f in self.success)

    @property
    def freed_display(self) -> str:
        return format_bytes(self.freed_bytes)


def _is_trash_path(path: Path) -> bool:
    """Check if the file is inside a Trash directory."""
    path_str = str(path)
    home_trash = str(Path.home() / ".Trash")
    return path_str.startswith(home_trash) or "/.Trashes/" in path_str


def _permanently_delete(path: Path) -> bool:
    """Permanently delete a file or directory."""
    try:
        if path.is_dir():
            shutil.rmtree(str(path))
        else:
            os.remove(str(path))
        return not path.exists()
    except (OSError, PermissionError):
        return False


def trash_files(files: list[FoundFile]) -> CleanResult:
    """Send a list of FoundFile items to the macOS Trash.

    Uses send2trash so files are recoverable from Trash.
    Falls back to osascript (Finder) for stubborn files.
    For items already in Trash, permanently deletes them.
    """
    result = CleanResult(success=[], failed=[])

    for item in files:
        path = item.path
        if not path.exists():
            result.failed.append((item, "Path no longer exists"))
            continue

        # Items already in Trash need permanent deletion
        if _is_trash_path(path):
            if _permanently_delete(path):
                result.success.append(item)
            else:
                result.failed.append((item, "Permission denied — grant Full Disk Access in System Settings"))
            continue

        # Try send2trash first
        try:
            send2trash(str(path))
            if not path.exists():
                result.success.append(item)
                continue
        except Exception:
            pass

        # Fallback: use macOS Finder via osascript
        try:
            _trash_via_finder(str(path))
            if not path.exists():
                result.success.append(item)
                continue
        except Exception:
            pass

        # If path still exists, report failure
        if path.exists():
            result.failed.append((item, "Permission denied — try closing the app first"))
        else:
            result.success.append(item)

    return result


def _trash_via_finder(path: str):
    """Move a file to Trash using macOS Finder via AppleScript."""
    script = (
        'on run argv\n'
        'tell application "Finder" to delete (POSIX file (item 1 of argv) as alias)\n'
        'end run'
    )
    try:
        subprocess.run(
            ["osascript", "-e", script, str(path)],
            capture_output=True,
            timeout=30,
        )
    except subprocess.TimeoutExpired:
        raise OSError(f"Finder timed out moving '{path}' to Trash")
