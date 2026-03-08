"""Bundle ID extraction from .app bundles."""

import plistlib
from pathlib import Path


def get_bundle_id(app_path: str) -> str | None:
    """Read CFBundleIdentifier from an .app's Info.plist.

    Args:
        app_path: Path to the .app bundle (e.g. /Applications/Slack.app)

    Returns:
        Bundle identifier string or None if not found.
    """
    plist_path = Path(app_path) / "Contents" / "Info.plist"
    if not plist_path.exists():
        return None

    try:
        with open(plist_path, "rb") as f:
            plist = plistlib.load(f)
        return plist.get("CFBundleIdentifier")
    except Exception:
        return None


def get_app_name(app_path: str) -> str:
    """Extract the display name from an .app bundle.

    Falls back to the .app folder name if plist read fails.
    """
    plist_path = Path(app_path) / "Contents" / "Info.plist"
    if plist_path.exists():
        try:
            with open(plist_path, "rb") as f:
                plist = plistlib.load(f)
            name = plist.get("CFBundleName") or plist.get("CFBundleDisplayName")
            if name:
                return name
        except Exception:
            pass

    return Path(app_path).stem
