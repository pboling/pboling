#!/usr/bin/env python3
"""Cache org logos in assets/logos/<owner>.<ext> so render.py can embed them (GitHub blocks external
images inside SVGs). Owned projects: logos.galtzo.com (PNG), falling back to the GitHub avatar.
Contributor projects: the GitHub org/user avatar. Existing files are kept; pass --refresh to refetch."""
import pathlib, sys, urllib.request, yaml

ROOT = pathlib.Path(__file__).resolve().parents[2]
OUT = ROOT / "assets" / "logos"; OUT.mkdir(parents=True, exist_ok=True)
refresh = "--refresh" in sys.argv

def fetch(url):
    try:
        r = urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "profile-gen"}), timeout=30)
        return r.read()
    except Exception:
        return None

def ext_of(b):
    return "png" if b[:4] == b"\x89PNG" else "jpg" if b[:2] == b"\xff\xd8" else None

projects = yaml.safe_load((ROOT / "data/projects.yml").read_text())
want = {}   # owner -> contributor?   (owned wins if an owner appears in both)
for p in projects:
    f = next((f for f in p.get("forges", []) if f["type"] == "GitHub"), None)
    if not f or not f.get("owner"): continue
    want[f["owner"]] = want.get(f["owner"], True) and p.get("role") == "contributor"
for owner, contributor in sorted(want.items()):
    if not refresh and any((OUT / f"{owner}.{e}").exists() for e in ("png", "jpg")): continue
    blob = None
    if not contributor:
        blob = fetch(f"https://logos.galtzo.com/assets/images/{owner}/avatar-128px.png")
    blob = blob if blob and ext_of(blob) else fetch(f"https://github.com/{owner}.png?size=96")
    if blob and ext_of(blob):
        (OUT / f"{owner}.{ext_of(blob)}").write_bytes(blob); print("logo", owner, len(blob))
    else:
        print("no logo for", owner)
