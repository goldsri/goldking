# M3U Auto Update (authorized, non-DRM playlist)

This template refreshes a playlist you own or are authorized to redistribute. Do not use it to mirror protected streams, DRM keys, cookies, or private session data.


## Setup
1. Create a GitHub repository and upload `update.py`, `playlist.m3u` (optional initial file), and `.github/workflows/auto-update.yml`.
2. In your repository, open **Settings → Secrets and variables → Actions → New repository secret**.
3. Create secret name `SOURCE_M3U_URL`; value is your authorized, non-DRM M3U source URL.
4. Open **Actions → Auto Update M3U Playlist → Run workflow** to test.
5. The workflow runs every 6 hours (UTC) and commits only if the playlist changes.


## Output
The refreshed file is `playlist.m3u` in the repository root.
