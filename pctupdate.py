import urllib.request

URL = "https://raw.githubusercontent.com/Babuperumana/IN_IptV/refs/heads/main/pocket.m3u"

req = urllib.request.Request(
    URL,
    headers={"User-Agent": "Mozilla/5.0"}
)

with urllib.request.urlopen(req, timeout=60) as response:
    data = response.read()

with open("Goldpct.m3u", "wb") as file:
    file.write(data)

print("Goldpct.m3u update completed")
