
import os
import requests
from pathlib import Path

SOURCE_URL = os.getenv("SOURCE_M3U_URL_2")
OUTPUT_FILE = "goldkingplus.m3u"

def main():
    if not SOURCE_URL:
        raise ValueError("SOURCE_M3U_URL_2 secret is missing")

    response = requests.get(SOURCE_URL, timeout=60)
    response.raise_for_status()

    content = response.text

    if not content.lstrip().startswith("#EXTM3U"):
        raise ValueError("Invalid M3U playlist")

    if "#KODIPROP" in content:
        raise ValueError("DRM-protected playlist is not supported")

    Path(OUTPUT_FILE).write_text(
        content, encoding="utf-8"
    )

    print("Playlist updated successfully")

if __name__ == "__main__":
    main()
