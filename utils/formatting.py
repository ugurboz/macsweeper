"""Centralized size formatting — SI/decimal units (1000-based)."""

from __future__ import annotations


def format_bytes(b: int) -> str:
    """Format byte count using SI/decimal units (matches Finder/Nektony)."""
    if b < 1_000:
        return f"{b} B"
    if b < 1_000_000:
        return f"{b / 1_000:.1f} KB"
    if b < 1_000_000_000:
        return f"{b / 1_000_000:.1f} MB"
    return f"{b / 1_000_000_000:.2f} GB"
