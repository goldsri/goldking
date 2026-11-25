#!/usr/bin/env python3
"""
Fetch an authorized M3U playlist from SOURCE_M3U_URL_2 and save it locally.
The source URL is supplied through a GitHub Actions secret; do not hard-code
private playlist URLs or credentials in this file.
"""
import os
import sys
from pathlib import Path

import requests

OUTPUT_FILE = Path("premiumiptv23.m3u")
SOURCE_ENV = "SOURCE_M3U_URL_2"


def main() -> int:
    url = os.environ.get(SOURCE_ENV, "").strip()
    if not url:
        print(f"ERROR: GitHub Secret {SOURCE_ENV} is empty or missing.", file=sys.stderr)
        return 1

    try:
        response = requests.get(
            url,
            timeout=(20, 90),
            headers={"User-Agent": "Mozilla/5.0 M3U-AutoUpdater/1.0"},
        )
        response.raise_for_status()
    except requests.RequestException as exc:
        print(f"ERROR: Could not download playlist: {exc}", file=sys.stderr)
        return 1

    content = response.content
    if not content or b"#EXTM3U" not in content[:4096]:
        print(
            "ERROR: The response does not look like an M3U playlist "
            "(#EXTM3U header not found). Existing output was left unchanged.",
            file=sys.stderr,
        )
        return 1

    # Preserve the source bytes; do not rewrite stream URLs or keys.
    OUTPUT_FILE.write_bytes(content)
    print(f"Updated {OUTPUT_FILE} ({len(content)} bytes).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
