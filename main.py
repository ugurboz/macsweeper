"""MacSweeper — entry point."""

import sys
from scanner import scan_app, list_installed_apps


def main():
    # CLI mode: --cli flag or passing an app path
    if "--cli" in sys.argv:
        _cli_mode()
        return

    if len(sys.argv) > 1 and sys.argv[1].endswith(".app"):
        result = scan_app(sys.argv[1])
        _print_result(result)
        return

    # Default: launch GUI
    from ui.web_app import run_web_app
    run_web_app()


def _cli_mode():
    """Fallback CLI for testing without GUI."""
    args = [a for a in sys.argv[1:] if a != "--cli"]

    if args and args[0].endswith(".app"):
        result = scan_app(args[0])
        _print_result(result)
    else:
        print("\n📦  Installed apps in /Applications:\n")
        apps = list_installed_apps()
        for i, app in enumerate(apps, 1):
            bid = app["bundle_id"] or "N/A"
            print(f"  {i:3}. {app['name']:<30} {bid}")
        print(f"\n  Total: {len(apps)} apps")
        print("\n💡  Usage: python main.py /Applications/SomeApp.app")


def _print_result(result):
    print(f"\n🔍  App Name  : {result.app_name}")
    print(f"📦  Bundle ID : {result.bundle_id}")
    print(f"📂  Found     : {len(result.files)} leftover item(s)")
    print(f"💾  Total Size: {result.total_display_size}\n")

    if not result.files:
        print("  ✅ No leftover files found!")
        return

    for f in result.files:
        print(f"  [{f.category:<14}] {f.display_size:>10}  {f.path}")


if __name__ == "__main__":
    main()
