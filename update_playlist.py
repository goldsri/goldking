#!/usr/bin/env python3
"""Fetch and publish an authorized, non-DRM M3U playlist.

The script deliberately refuses playlists containing DRM license keys,
license metadata, or per-stream authentication cookies.
"""
import os
import sys
import urllib.request
from pathlib import Path

SOURCE_URL = os.environ.get("SOURCE_M3U_URL_3", "").strip()
OUTPUT = Path("playlist.m3u")
MAX_BYTES = 25 * 1024 * 1024

BLOCKED_MARKERS = (
    "#KODIPROP:inputstream.adaptive.license_key",
    "#KODIPROP:inputstream.adaptive.license_type",
    "#EXTHTTP:",
    "clearkey",
    "widevine",
)

def main():
    if not SOURCE_URL:
        sys.exit("ERROR: SOURCE_M3U_URL_3 secret is empty or missing.")

    req = urllib.request.Request(
        SOURCE_URL,
        headers={"User-Agent": "Authorized-M3U-AutoUpdater/1.0"},
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as response:
            data = response.read(MAX_BYTES + 1)
    except Exception as exc:
        sys.exit(f"ERROR: Could not download source playlist: {exc}")

    if len(data) > MAX_BYTES:
        sys.exit("ERROR: Playlist exceeds 25 MB limit.")

    try:
        content = data.decode("utf-8-sig")
    except UnicodeDecodeError:
        sys.exit("ERROR: Source is not valid UTF-8 text.")

    if not content.lstrip().startswith("#EXTM3U"):
        sys.exit("ERROR: Source does not begin with #EXTM3U.")

    lowered = content.lower()
    found = [marker for marker in BLOCKED_MARKERS if marker.lower() in lowered]
    if found:
        sys.exit(
            "STOPPED: This source contains DRM/license or cookie-authentication "
            "metadata. This workflow only publishes authorized, non-DRM M3U "
            "playlists. No output was written."
        )

    OUTPUT.write_text(content.rstrip() + "\n", encoding="utf-8")
    print(f"Updated {OUTPUT} ({len(content.splitlines())} lines).")

if __name__ == "__main__":
    main()
