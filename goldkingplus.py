
import os
import requests
from pathlib import Path

SOURCE_URL = os.environ.get("SOURCE_M3U_URL_2")
OUTPUT = "goldkingplus.m3u"

def main():
    if not SOURCE_URL:
        raise ValueError("SOURCE_M3U_URL_2 is missing")

    response = requests.get(
        SOURCE_URL,
        timeout=60,
        headers={"User-Agent": "Mozilla/5.0"}
    )
    response.raise_for_status()

    lines = response.text.splitlines()

    if not any(line.strip() == "#EXTM3U" for line in lines):
        raise ValueError("Invalid M3U playlist")

    header = []
    entries = []
    current = []

    for line in lines:
        if line.startswith("#EXTINF"):
            if current:
                entries.append(current)
            current = [line]
        elif current:
            current.append(line)
        else:
            header.append(line)

    if current:
        entries.append(current)

    safe_entries = []

    for entry in entries:
        block = "\n".join(entry).upper()

        if "#KODIPROP" in block:
            continue

        safe_entries.append(entry)

    if not safe_entries:
        raise ValueError("No DRM-free entries found")

    output = header[:]

    for entry in safe_entries:
        output.extend(entry)

    Path(OUTPUT).write_text(
        "\n".join(output) + "\n",
        encoding="utf-8"
    )

    print("Total entries:", len(entries))
    print("DRM-free entries:", len(safe_entries))
    print("Playlist saved:", OUTPUT)

if __name__ == "__main__":
    main()
