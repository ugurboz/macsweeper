"""Scanner engine — finds leftover files for a given app or bundle ID."""

from __future__ import annotations

import os
import subprocess
from dataclasses import dataclass, field
from pathlib import Path

from utils.bundle import get_bundle_id, get_app_name
from utils.formatting import format_bytes

# ── Category definitions ────────────────────────────────────────────
CATEGORY_MAP: dict[str, str] = {
    "Application Support": "App Support",
    "Preferences": "Preferences",
    "Caches": "Cache",
    "Logs": "Log",
    "Group Containers": "Group Container",
    "Saved Application State": "Saved State",
    "LaunchAgents": "Launch Agent",
    "LaunchDaemons": "Launch Daemon",
    "Cookies": "Cookie",
    "HTTPStorages": "HTTP Storage",
    "WebKit": "WebKit",
    "Application Scripts": "App Script",
}

HOME = Path.home()

SEARCH_LOCATIONS: list[tuple[Path, str]] = [
    (HOME / "Library" / loc, cat) for loc, cat in CATEGORY_MAP.items()
]

# Host-specific preferences (separate subdir)
SEARCH_LOCATIONS.append((HOME / "Library" / "Preferences" / "ByHost", "Preferences"))

# Additional user Library locations
EXTRA_USER_SEARCH: list[tuple[Path, str]] = [
    (HOME / "Library" / "Internet Plug-Ins", "Internet Plug-In"),
    (HOME / "Library" / "Input Methods", "Input Method"),
    (HOME / "Library" / "Screen Savers", "Screen Saver"),
    (HOME / "Library" / "Services", "Service"),
    (HOME / "Library" / "PreferencePanes", "Preference Pane"),
    (HOME / "Library" / "ColorPickers", "Color Picker"),
]

# CrashReporter directory (per-app crash logs)
CRASH_REPORTER_DIR = HOME / "Library" / "Application Support" / "CrashReporter"

# Additional system-level locations
SYSTEM_SEARCH: list[tuple[Path, str]] = [
    (Path("/Library/Application Support"), "System App Support"),
    (Path("/Library/Preferences"), "System Preferences"),
    (Path("/Library/Caches"), "System Cache"),
    (Path("/Library/LaunchDaemons"), "System Launch Daemon"),
    (Path("/Library/LaunchAgents"), "System Launch Agent"),
    (Path("/Library/Logs"), "System Log"),
    (Path("/Library/Internet Plug-Ins"), "System Internet Plug-In"),
    (Path("/Library/Frameworks"), "System Framework"),
    (Path("/Library/PrivilegedHelperTools"), "Privileged Helper"),
    (Path("/Library/StartupItems"), "Startup Item"),
]

# Package receipts (installer records)
RECEIPTS_DIR = Path("/private/var/db/receipts")

# macOS user cache/temp dirs (/private/var/folders/xx/yyyy/C/ and T/)
def _get_var_folders_dirs() -> tuple[Path | None, Path | None]:
    """Get the user's /var/folders cache and temp directories."""
    try:
        cache = subprocess.check_output(
            ["getconf", "DARWIN_USER_CACHE_DIR"], timeout=2
        ).decode().strip()
        temp = subprocess.check_output(
            ["getconf", "DARWIN_USER_TEMP_DIR"], timeout=2
        ).decode().strip()
        cache_p = Path(cache) if cache and Path(cache).exists() else None
        temp_p = Path(temp) if temp and Path(temp).exists() else None
        return cache_p, temp_p
    except Exception:
        return None, None

_VAR_DIRS_CACHE: tuple[Path | None, Path | None] | None = None


def _get_cached_var_dirs() -> tuple[Path | None, Path | None]:
    """Resolve /var/folders paths lazily so imports stay fast."""
    global _VAR_DIRS_CACHE
    if _VAR_DIRS_CACHE is None:
        _VAR_DIRS_CACHE = _get_var_folders_dirs()
    return _VAR_DIRS_CACHE


# ── Data models ─────────────────────────────────────────────────────
@dataclass
class FoundFile:
    """A single leftover file/folder found on disk."""

    path: Path
    size_bytes: int
    category: str

    @property
    def size_mb(self) -> float:
        return round(self.size_bytes / 1_000_000, 2)

    @property
    def display_size(self) -> str:
        return format_bytes(self.size_bytes)


@dataclass
class ScanResult:
    """Aggregated scan results for one application."""

    app_name: str
    bundle_id: str | None
    files: list[FoundFile] = field(default_factory=list)

    @property
    def total_size_bytes(self) -> int:
        return sum(f.size_bytes for f in self.files)

    @property
    def total_display_size(self) -> str:
        return format_bytes(self.total_size_bytes)


# ── Helpers ─────────────────────────────────────────────────────────
def _dir_size(path: Path) -> int:
    """Recursively calculate total size of a directory."""
    total = 0
    try:
        for entry in path.rglob("*"):
            if entry.is_file() and not entry.is_symlink():
                total += entry.stat().st_size
    except PermissionError:
        pass
    return total


def _item_size(path: Path) -> int:
    """Size in bytes — works for both files and directories."""
    try:
        if path.is_file():
            return path.stat().st_size
        return _dir_size(path)
    except OSError:
        return 0


def _extract_vendor_and_product(bundle_id: str | None, app_name: str) -> tuple[list[str], list[str]]:
    """Extract vendor and product name candidates from bundle ID and app name.

    For com.google.Chrome with app_name "Google Chrome":
      vendors  = ["google"]
      products = ["chrome", "google chrome"]
    """
    vendors: list[str] = []
    products: list[str] = []

    if bundle_id:
        parts = bundle_id.lower().split(".")
        # com.google.Chrome → vendor="google", product="chrome"
        if len(parts) >= 3:
            vendors.append(parts[1])  # "google"
            products.append(parts[2])  # "chrome"

    if app_name and len(app_name) >= 3:
        products.append(app_name.lower())  # "google chrome"
        # If multi-word, also add individual words >= 3 chars as product candidates
        words = app_name.lower().split()
        if len(words) > 1:
            for w in words:
                if len(w) >= 3 and w not in vendors:
                    products.append(w)

    # Deduplicate while preserving order
    seen_v: set[str] = set()
    vendors = [v for v in vendors if not (v in seen_v or seen_v.add(v))]
    seen_p: set[str] = set()
    products = [p for p in products if not (p in seen_p or seen_p.add(p))]

    return vendors, products


def _matches(name: str, bundle_id: str | None, app_name: str) -> bool:
    """Check if a file/folder name matches the app's bundle ID or name.

    Matching strategy (strict to loose):
      1. Full bundle ID substring match (com.docker.docker in name)
      2. Vendor+product match (com.docker in name)
      3. App display name match (Docker in name, min 3 chars)
    """
    lower = name.lower()

    if bundle_id:
        bid = bundle_id.lower()
        parts = bid.split(".")

        # Full bundle ID match — most reliable
        if bid in lower:
            return True

        # Vendor+product prefix — use full bundle ID as prefix
        # com.docker.docker → matches com.docker.docker.helper
        if lower.startswith(bid):
            return True

        # For 3+ part IDs, also check the first 3 parts as prefix
        # com.google.Chrome → com.google.chrome matches com.google.chrome.helper
        if len(parts) >= 3:
            product_prefix = ".".join(parts[:3])
            if lower.startswith(product_prefix):
                return True

        # Group containers: group.com.docker.docker
        if lower.startswith(f"group.{bid}") or f"group.{bid}" == lower:
            return True
        if len(parts) >= 3:
            product_prefix = ".".join(parts[:3])
            if lower.startswith(f"group.{product_prefix}"):
                return True

    # Match by app display name (case-insensitive, min 3 chars to avoid noise)
    if app_name and len(app_name) >= 3:
        aname = app_name.lower()
        # Require word-boundary-like match to avoid "or" matching "doctor"
        if aname in lower:
            # Extra check: the match should be at a word boundary
            idx = lower.find(aname)
            before_ok = idx == 0 or not lower[idx - 1].isalpha()
            after_idx = idx + len(aname)
            after_ok = after_idx >= len(lower) or not lower[after_idx].isalpha()
            if before_ok and after_ok:
                return True

    return False


# ── Public API ──────────────────────────────────────────────────────
def scan_app(app_path: str, include_app_bundle: bool = True) -> ScanResult:
    """Scan for leftover files of a specific .app bundle.

    Args:
        app_path: Absolute path to the .app (e.g. /Applications/Slack.app)
        include_app_bundle: If True, include the .app itself as a removable item.

    Returns:
        ScanResult with all discovered leftover items.
    """
    bundle_id = get_bundle_id(app_path)
    app_name = get_app_name(app_path)
    app_p = Path(app_path)

    result = ScanResult(app_name=app_name, bundle_id=bundle_id)
    seen_paths: set[str] = set()

    # 1) Include the .app bundle itself
    if include_app_bundle and app_p.exists():
        size = _item_size(app_p)
        result.files.append(
            FoundFile(path=app_p, size_bytes=size, category="Application")
        )
        seen_paths.add(str(app_p))

    # 2) Scan user ~/Library locations
    for search_dir, category in SEARCH_LOCATIONS:
        _scan_directory(search_dir, category, bundle_id, app_name, result, seen_paths)

    # 3) Extra user ~/Library locations
    for search_dir, category in EXTRA_USER_SEARCH:
        _scan_directory(search_dir, category, bundle_id, app_name, result, seen_paths)

    # 4) Scan system /Library locations
    for search_dir, category in SYSTEM_SEARCH:
        _scan_directory(search_dir, category, bundle_id, app_name, result, seen_paths)

    # 5) Scan ~/Library/Preferences for .plist files matching bundle ID
    if bundle_id:
        _scan_preferences_deep(bundle_id, app_name, result, seen_paths)

    # 6) Scan home directory for dotfiles/dotfolders (.appname)
    _scan_home_dotfiles(bundle_id, app_name, result, seen_paths)

    # 7) Scan /private/var/folders/ caches and temp
    _scan_var_folders(bundle_id, app_name, result, seen_paths)

    # 8) Scan installer receipts (/private/var/db/receipts/)
    _scan_receipts(bundle_id, app_name, result, seen_paths)

    # 9) Scan CrashReporter per-app plists
    _scan_crashreporter(bundle_id, app_name, result, seen_paths)

    # 10) Deep scan inside Containers — each container has its own Library
    _scan_containers_deep(bundle_id, app_name, result, seen_paths)

    # 11) Scan vendor subdirectories (e.g. AppSupport/Google/Chrome, Caches/Google/Chrome)
    _scan_vendor_subdirs(bundle_id, app_name, result, seen_paths)

    return result


def _scan_directory(
    search_dir: Path,
    category: str,
    bundle_id: str | None,
    app_name: str,
    result: ScanResult,
    seen: set[str],
):
    """Scan a single directory for matching entries."""
    if not search_dir.exists():
        return

    try:
        for entry in search_dir.iterdir():
            entry_str = str(entry)
            if entry_str in seen:
                continue
            if _matches(entry.name, bundle_id, app_name):
                size = _item_size(entry)
                result.files.append(
                    FoundFile(path=entry, size_bytes=size, category=category)
                )
                seen.add(entry_str)
    except PermissionError:
        pass


def _scan_vendor_subdirs(
    bundle_id: str | None,
    app_name: str,
    result: ScanResult,
    seen: set[str],
):
    """Scan vendor subdirectories inside each Library location.

    Many apps store data under vendor-named directories, e.g.:
      ~/Library/Application Support/Google/Chrome/
      ~/Library/Caches/Google/Chrome/
      ~/Library/Application Support/Microsoft/Teams/

    This function finds those nested entries the top-level scan misses.
    """
    vendors, products = _extract_vendor_and_product(bundle_id, app_name)
    if not vendors:
        return

    # All standard Library locations + system locations to check for vendor subdirs
    all_locations = list(SEARCH_LOCATIONS) + list(EXTRA_USER_SEARCH) + list(SYSTEM_SEARCH)

    for search_dir, category in all_locations:
        if not search_dir.exists():
            continue

        try:
            for entry in search_dir.iterdir():
                if not entry.is_dir():
                    continue

                # Check if this is a vendor directory
                entry_lower = entry.name.lower()
                is_vendor = any(v == entry_lower for v in vendors)
                if not is_vendor:
                    continue

                # Inside the vendor directory, look for product matches
                try:
                    for sub_entry in entry.iterdir():
                        sub_str = str(sub_entry)
                        if sub_str in seen:
                            continue

                        sub_lower = sub_entry.name.lower()
                        matched = False
                        for prod in products:
                            if prod in sub_lower:
                                idx = sub_lower.find(prod)
                                before_ok = idx == 0 or not sub_lower[idx - 1].isalpha()
                                after_idx = idx + len(prod)
                                after_ok = after_idx >= len(sub_lower) or not sub_lower[after_idx].isalpha()
                                if before_ok and after_ok:
                                    matched = True
                                    break

                        if matched:
                            size = _item_size(sub_entry)
                            result.files.append(
                                FoundFile(path=sub_entry, size_bytes=size, category=category)
                            )
                            seen.add(sub_str)
                except PermissionError:
                    pass
        except PermissionError:
            pass


def _scan_preferences_deep(
    bundle_id: str,
    app_name: str,
    result: ScanResult,
    seen: set[str],
):
    """Find .plist files in Preferences that match bundle ID patterns."""
    prefs_dir = HOME / "Library" / "Preferences"
    if not prefs_dir.exists():
        return

    bid_lower = bundle_id.lower()
    parts = bid_lower.split(".")

    try:
        for entry in prefs_dir.iterdir():
            entry_str = str(entry)
            if entry_str in seen:
                continue
            if not entry.name.endswith(".plist"):
                continue

            name_lower = entry.name.lower()
            # Match by full bundle ID or significant prefix
            # Match by full bundle ID or product prefix
            if bid_lower in name_lower:
                size = _item_size(entry)
                result.files.append(
                    FoundFile(path=entry, size_bytes=size, category="Preferences")
                )
                seen.add(entry_str)
            # Also match by product prefix for 3+ part IDs
            # com.google.Chrome → com.google.chrome.helper.plist
            elif len(parts) >= 3:
                product_prefix = ".".join(parts[:3])
                if name_lower.startswith(product_prefix):
                    size = _item_size(entry)
                    result.files.append(
                        FoundFile(path=entry, size_bytes=size, category="Preferences")
                    )
                    seen.add(entry_str)
    except PermissionError:
        pass


# Skip these well-known system/dev dotfiles/folders
_SKIP_DOTFILES = frozenset({
    ".ds_store", ".localized", ".trash", ".spotlight-v100",
    ".fseventsd", ".cfusertextencoding", ".file",
    ".gitconfig", ".gitignore_global", ".git",
    ".ssh", ".gnupg", ".bash_history", ".bash_profile",
    ".bashrc", ".zshrc", ".zsh_history", ".zprofile",
    ".profile", ".inputrc", ".vimrc", ".viminfo",
    ".lesshst", ".wget-hsts",
    ".local", ".cache", ".config",  # XDG dirs — too generic
})


def _scan_home_dotfiles(
    bundle_id: str | None,
    app_name: str,
    result: ScanResult,
    seen: set[str],
):
    """Scan ~ for hidden files/folders matching the app (e.g. ~/.docker)."""
    if not app_name or len(app_name) < 3:
        return

    try:
        for entry in HOME.iterdir():
            if not entry.name.startswith("."):
                continue
            if entry.name.lower() in _SKIP_DOTFILES:
                continue

            entry_str = str(entry)
            if entry_str in seen:
                continue

            # Strip leading dot for matching:  .docker → docker
            bare = entry.name[1:]
            if _matches(bare, bundle_id, app_name):
                size = _item_size(entry)
                result.files.append(
                    FoundFile(path=entry, size_bytes=size, category="Home Dotfile")
                )
                seen.add(entry_str)
    except PermissionError:
        pass


def _scan_var_folders(
    bundle_id: str | None,
    app_name: str,
    result: ScanResult,
    seen: set[str],
):
    """Scan /private/var/folders/ user cache and temp for matching entries."""
    var_cache_dir, var_temp_dir = _get_cached_var_dirs()
    for var_dir, category in [
        (var_cache_dir, "Temp Cache"),
        (var_temp_dir, "Temp Data"),
    ]:
        if not var_dir or not var_dir.exists():
            continue
        try:
            for entry in var_dir.iterdir():
                entry_str = str(entry)
                if entry_str in seen:
                    continue
                if _matches(entry.name, bundle_id, app_name):
                    size = _item_size(entry)
                    result.files.append(
                        FoundFile(path=entry, size_bytes=size, category=category)
                    )
                    seen.add(entry_str)
        except PermissionError:
            pass


def _scan_receipts(
    bundle_id: str | None,
    app_name: str,
    result: ScanResult,
    seen: set[str],
):
    """Scan /private/var/db/receipts/ for installer receipt .bom and .plist files."""
    if not RECEIPTS_DIR.exists():
        return

    bid_lower = bundle_id.lower() if bundle_id else ""
    aname_lower = app_name.lower() if app_name else ""

    try:
        for entry in RECEIPTS_DIR.iterdir():
            entry_str = str(entry)
            if entry_str in seen:
                continue
            if not entry.is_file():
                continue

            name_lower = entry.name.lower()

            matched = False
            # Match by bundle ID
            if bid_lower and bid_lower in name_lower:
                matched = True
            # Match by app name (word-boundary, min 3 chars)
            elif aname_lower and len(aname_lower) >= 3 and aname_lower in name_lower:
                idx = name_lower.find(aname_lower)
                before_ok = idx == 0 or not name_lower[idx - 1].isalpha()
                after_idx = idx + len(aname_lower)
                after_ok = after_idx >= len(name_lower) or not name_lower[after_idx].isalpha()
                if before_ok and after_ok:
                    matched = True

            if matched:
                size = entry.stat().st_size
                result.files.append(
                    FoundFile(path=entry, size_bytes=size, category="Receipt")
                )
                seen.add(entry_str)
    except PermissionError:
        pass


def _scan_crashreporter(
    bundle_id: str | None,
    app_name: str,
    result: ScanResult,
    seen: set[str],
):
    """Scan ~/Library/Application Support/CrashReporter/ for crash log plists."""
    if not CRASH_REPORTER_DIR.exists():
        return

    try:
        for entry in CRASH_REPORTER_DIR.iterdir():
            entry_str = str(entry)
            if entry_str in seen:
                continue
            if not entry.is_file():
                continue

            # CrashReporter files are named "AppName_UUID.plist"
            name = entry.name
            # Strip the UUID suffix to get the app name part
            # e.g. "Google Chrome_2357F845-75C5-5745-B152-0D9DF1AC3D5D.plist"
            underscore_idx = name.rfind("_")
            if underscore_idx > 0:
                name_part = name[:underscore_idx]
            else:
                name_part = name.replace(".plist", "")

            if _matches(name_part, bundle_id, app_name):
                size = entry.stat().st_size
                result.files.append(
                    FoundFile(path=entry, size_bytes=size, category="Crash Report")
                )
                seen.add(entry_str)
    except PermissionError:
        pass


def _scan_containers_deep(
    bundle_id: str | None,
    app_name: str,
    result: ScanResult,
    seen: set[str],
):
    """Deep scan inside matching Containers — find nested Library data.

    Each ~/Library/Containers/<bundle-id>/Data/Library/ has its own
    Caches, Preferences, Application Support, etc. that the normal
    top-level scan misses.
    """
    containers_dir = HOME / "Library" / "Containers"
    if not containers_dir.exists():
        return

    # First find containers that match this app
    matching_containers: list[Path] = []
    try:
        for entry in containers_dir.iterdir():
            if not entry.is_dir():
                continue
            if str(entry) in seen:
                continue
            if _matches(entry.name, bundle_id, app_name):
                matching_containers.append(entry)
    except PermissionError:
        return

    # For each matching container, scan its Data/Library subdirectories
    container_subcats = {
        "Caches": "Container Cache",
        "Preferences": "Container Preferences",
        "Application Support": "Container App Support",
        "Logs": "Container Log",
        "HTTPStorages": "Container HTTP Storage",
        "Cookies": "Container Cookie",
        "Saved Application State": "Container Saved State",
        "WebKit": "Container WebKit",
    }

    for container in matching_containers:
        data_lib = container / "Data" / "Library"
        if not data_lib.exists():
            continue

        try:
            for subdir in data_lib.iterdir():
                if not subdir.is_dir():
                    continue
                entry_str = str(subdir)
                if entry_str in seen:
                    continue

                category = container_subcats.get(subdir.name)
                if not category:
                    continue

                size = _item_size(subdir)
                if size > 0:
                    result.files.append(
                        FoundFile(path=subdir, size_bytes=size, category=category)
                    )
                    seen.add(entry_str)
        except PermissionError:
            pass


def scan_by_bundle_id(bundle_id: str, app_name: str = "") -> ScanResult:
    """Scan by a known bundle ID (for already-deleted apps)."""
    result = ScanResult(app_name=app_name or bundle_id, bundle_id=bundle_id)
    seen: set[str] = set()

    for search_dir, category in SEARCH_LOCATIONS:
        _scan_directory(search_dir, category, bundle_id, app_name, result, seen)

    for search_dir, category in EXTRA_USER_SEARCH:
        _scan_directory(search_dir, category, bundle_id, app_name, result, seen)

    for search_dir, category in SYSTEM_SEARCH:
        _scan_directory(search_dir, category, bundle_id, app_name, result, seen)

    if bundle_id:
        _scan_preferences_deep(bundle_id, app_name, result, seen)

    _scan_home_dotfiles(bundle_id, app_name, result, seen)
    _scan_var_folders(bundle_id, app_name, result, seen)
    _scan_receipts(bundle_id, app_name, result, seen)
    _scan_crashreporter(bundle_id, app_name, result, seen)
    _scan_containers_deep(bundle_id, app_name, result, seen)
    _scan_vendor_subdirs(bundle_id, app_name, result, seen)

    return result


def _iter_app_bundles(base_dir: Path):
    """Yield .app bundles recursively without descending into app contents."""
    if not base_dir.exists() or not base_dir.is_dir():
        return

    try:
        for root, dirs, _ in os.walk(base_dir, topdown=True):
            root_p = Path(root)

            # If root itself is an app bundle, return it and stop descending.
            if root_p.suffix == ".app":
                yield root_p
                dirs[:] = []
                continue

            # Yield app bundles in this level and prune them from recursion.
            for d in list(dirs):
                if d.endswith(".app"):
                    app_p = root_p / d
                    yield app_p
                    dirs.remove(d)
    except OSError:
        return


def list_installed_apps(apps_dir: str = "/Applications", fast_mode: bool = False) -> list[dict]:
    """List .app bundles from common macOS application directories.

    Args:
        apps_dir: Primary directory to scan. Also scans ~/Applications and
            /System/Applications for better coverage.
        fast_mode: If True, skip Info.plist parsing for startup speed and use
            folder name as app name. Bundle IDs are returned as None.

    Returns:
        List of dicts with keys: path, name, bundle_id
    """
    apps: list[dict] = []
    seen_paths: set[str] = set()

    search_roots = [
        Path(apps_dir),
        HOME / "Applications",
        Path("/System/Applications"),
    ]

    for root in search_roots:
        for entry in _iter_app_bundles(root):
            try:
                resolved = str(entry.resolve())
            except OSError:
                resolved = str(entry)

            if resolved in seen_paths:
                continue
            seen_paths.add(resolved)

            if fast_mode:
                bundle_id = None
                name = entry.stem
            else:
                bundle_id = get_bundle_id(str(entry))
                name = get_app_name(str(entry))
            apps.append({
                "path": str(entry),
                "name": name,
                "bundle_id": bundle_id,
            })

    apps.sort(key=lambda a: a["name"].lower())
    return apps


# ── Orphan detection ────────────────────────────────────────────────
def _infer_app_name(entry_name: str) -> str:
    """Try to infer a human-readable app name from a file/folder name.

    Examples:
        com.openai.chatgpt → ChatGPT
        com.apple.garageband10 → Garageband10
        Docker → Docker
    """
    name = entry_name
    # Strip common extensions
    for ext in (".plist", ".bom", ".savedState"):
        if name.endswith(ext):
            name = name[: -len(ext)]

    # Well-known bundle ID → friendly name mappings
    known = {
        "com.openai.chat": "ChatGPT",
        "com.openai.atlas": "ChatGPT (Atlas)",
        "com.microsoft.vscode": "Visual Studio Code",
        "dev.warp.warp-stable": "Warp Terminal",
    }
    for k, v in known.items():
        if name.lower().startswith(k):
            return v

    # If it looks like a bundle ID (has dots), extract the last component
    if "." in name and name.count(".") >= 2:
        parts = name.split(".")
        candidate = parts[-1]
        # Capitalize nicely
        if candidate and candidate[0].islower():
            candidate = candidate.capitalize()
        return candidate

    return name


@dataclass
class OrphanGroup:
    """A group of orphan files that belong to the same (deleted) app."""
    inferred_name: str
    bundle_id_guess: str  # best-guess bundle ID from file names
    files: list[FoundFile] = field(default_factory=list)

    @property
    def total_size_bytes(self) -> int:
        return sum(f.size_bytes for f in self.files)

    @property
    def total_display_size(self) -> str:
        return format_bytes(self.total_size_bytes)


def _entry_belongs_to_installed(
    name: str,
    installed_ids: set[str],
    installed_names: set[str],
) -> bool:
    """Check if a Library entry belongs to any currently installed app."""
    lower = name.lower()

    # Apple system entries — skip (not orphans)
    if lower.startswith("com.apple.") or lower.startswith("apple"):
        return True

    # Check against all installed bundle IDs (both directions)
    for bid in installed_ids:
        bid_l = bid.lower()
        # Bundle ID in entry name: com.google.chrome in "com.google.chrome.helper"
        if bid_l in lower or lower.startswith(bid_l):
            return True
        # Entry name in bundle ID: "google" in "com.google.chrome"
        if len(lower) >= 3 and lower in bid_l:
            return True
        # Prefix match: com.google.chrome → com.google.chrome
        parts = bid_l.split(".")
        if len(parts) >= 3:
            prefix = ".".join(parts[:3])
            if lower.startswith(prefix):
                return True

    # Check against installed app names (both directions)
    for aname in installed_names:
        if len(aname) < 3:
            continue
        al = aname.lower()

        # App name in entry name: "docker" in "com.docker.vmnetd"
        if al in lower:
            idx = lower.find(al)
            before_ok = idx == 0 or not lower[idx - 1].isalpha()
            after_idx = idx + len(al)
            after_ok = after_idx >= len(lower) or not lower[after_idx].isalpha()
            if before_ok and after_ok:
                return True

        # Entry name in app name: "google" in "google chrome"
        if len(lower) >= 3 and lower in al:
            idx = al.find(lower)
            before_ok = idx == 0 or not al[idx - 1].isalpha()
            after_idx = idx + len(lower)
            after_ok = after_idx >= len(al) or not al[after_idx].isalpha()
            if before_ok and after_ok:
                return True

    return False


def _extract_bundle_id(name: str) -> str:
    """Try to extract a bundle-ID-like string from a file/folder name."""
    # Strip extensions
    clean = name
    for ext in (".plist", ".bom", ".savedState"):
        if clean.endswith(ext):
            clean = clean[: -len(ext)]

    # If it has dots, it probably IS a bundle ID
    if "." in clean and clean.count(".") >= 2:
        return clean

    return name


def find_orphaned_files() -> list[OrphanGroup]:
    """Find leftover files from apps that are no longer installed.

    Scans all Library directories and returns files that don't match
    any currently installed application.
    """
    # Known system/macOS components and dev tools — never flag as orphans
    system_prefixes = {
        "com.apple.", "com.microsoft.identity", "com.crashlytics",
        "group.com.apple.",
    }
    system_names = {
        # macOS system components
        "crashreporter", "geoservices", "icloudmailagent",
        "icloudmcckit", "homekit", "siri", "spotlight",
        "cloudkit", "coreaudio", "coremedia", "coredata",
        "metal", "gamekit", "mapkit", "storekit",
        "webkit", "networkextension", "fileprovider",
        "diagnosticreports", "passkit", "networkserviceproxy",
        "ilifemedabrowser", "animoji", "btserver",
        "askpermissiond", "familycircled", "sharingd",
        "identityservicesd", "callhistory", "knowledge",
        "biomeagent", "dataaccess", "contactsd",
        "accountsd", "parsecd", "suggestd", "nsurlsessiond",
        "mediaremoted", "itunescloudd", "imtransferagent",
        "imagent", "quicklookd", "mds", "mdworker",
        "cloudd", "bird", "assistantd",
        "rapportd", "remindd", "calaccessd",
        "usernoted", "statuskit", "translationd",
        "ilifemedabrowser", "ilifemediabrowser",
        "podcasts", "script editor",
        "itunescloud", "ituneslibrary.framework",
        # Developer tools & runtimes
        "homebrew", "pip", "npm", "node-gyp", "yarn",
        "python.framework", "node_modules", "go", "cargo",
        "typescript", "ms-playwright-go", "cocoapods", "pods",
        "ruby", "gem", "gradle", "maven",
        # Common generic dirs
        "caches", "socket", "logs",
    }

    # 1) Gather all installed apps' bundle IDs and names
    apps = list_installed_apps()
    installed_ids: set[str] = set()
    installed_names: set[str] = set()

    for app in apps:
        if app["bundle_id"]:
            installed_ids.add(app["bundle_id"])
        if app["name"]:
            installed_names.add(app["name"])

    # 2) Scan all Library directories and collect unmatched entries
    orphan_map: dict[str, OrphanGroup] = {}  # keyed by inferred bundle ID

    all_locations = SEARCH_LOCATIONS + EXTRA_USER_SEARCH + SYSTEM_SEARCH

    for search_dir, category in all_locations:
        if not search_dir.exists():
            continue
        try:
            for entry in search_dir.iterdir():
                name = entry.name
                if name.startswith(".") or name == "__pycache__":
                    continue

                # Skip known system/dev entries
                name_l = name.lower()
                if any(name_l.startswith(sp) for sp in system_prefixes):
                    continue
                if name_l in system_names:
                    continue
                # Skip Apple frameworks, profile pictures, random files
                if name_l.endswith(".framework"):
                    continue
                if name_l.startswith("aaprofilepicture"):
                    continue

                if _entry_belongs_to_installed(name, installed_ids, installed_names):
                    continue

                # This is an orphan!
                bid_guess = _extract_bundle_id(name)
                key = bid_guess.lower()

                size = _item_size(entry)
                found = FoundFile(path=entry, size_bytes=size, category=category)

                if key not in orphan_map:
                    orphan_map[key] = OrphanGroup(
                        inferred_name=_infer_app_name(name),
                        bundle_id_guess=bid_guess,
                    )
                orphan_map[key].files.append(found)
        except PermissionError:
            continue

    # 3) Also scan Preferences for orphan .plist files
    prefs_dir = HOME / "Library" / "Preferences"
    if prefs_dir.exists():
        seen_in_locations = set()
        for loc, _ in all_locations:
            if "Preferences" in str(loc):
                try:
                    seen_in_locations.update(str(e) for e in loc.iterdir())
                except PermissionError:
                    pass

        try:
            for entry in prefs_dir.iterdir():
                if str(entry) in seen_in_locations:
                    continue
                if not entry.name.endswith(".plist"):
                    continue
                name = entry.name

                # Skip known system entries
                name_l = name.lower()
                if any(name_l.startswith(sp) for sp in system_prefixes):
                    continue

                if _entry_belongs_to_installed(name, installed_ids, installed_names):
                    continue

                bid_guess = _extract_bundle_id(name)
                key = bid_guess.lower()

                size = _item_size(entry)
                found = FoundFile(path=entry, size_bytes=size, category="Preferences")

                if key not in orphan_map:
                    orphan_map[key] = OrphanGroup(
                        inferred_name=_infer_app_name(name),
                        bundle_id_guess=bid_guess,
                    )
                orphan_map[key].files.append(found)
        except PermissionError:
            pass

    # 4) Sort by total size, descending
    groups = sorted(orphan_map.values(), key=lambda g: g.total_size_bytes, reverse=True)

    # Filter out empty groups and groups with names too short to be meaningful
    return [
        g for g in groups
        if g.total_size_bytes > 0 and len(g.inferred_name) >= 2
    ]


# ── CLI quick test ──────────────────────────────────────────────────
if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        target = sys.argv[1]
        print(f"\n🔍  Scanning: {target}\n")
        res = scan_app(target)
    else:
        # Demo: pick first app in /Applications
        apps = list_installed_apps()
        if not apps:
            print("No apps found.")
            sys.exit(0)
        target = apps[0]["path"]
        print(f"\n🔍  Demo scan — {apps[0]['name']} ({target})\n")
        res = scan_app(target)

    print(f"App Name  : {res.app_name}")
    print(f"Bundle ID : {res.bundle_id}")
    print(f"Found     : {len(res.files)} item(s)")
    print(f"Total Size: {res.total_display_size}\n")

    for f in res.files:
        print(f"  [{f.category:<14}] {f.display_size:>10}  {f.path}")
