#!/usr/bin/env python3
"""Copy the project data the profile renders from galtzo.com (updated piecemeal by its own scheduled jobs).
Keeps the previous copy if a download fails or does not parse."""
import pathlib, sys, urllib.request, yaml
BASE = "https://raw.githubusercontent.com/galtzo-floss/galtzo.com/main/src/_data/"
D = pathlib.Path(__file__).resolve().parents[2] / "data"
ok = True
for f in ("projects.yml", "person.yml", "families.yml"):
    try:
        text = urllib.request.urlopen(urllib.request.Request(BASE + f, headers={"User-Agent": "profile-gen"}), timeout=30).read().decode()
        yaml.safe_load(text)
        (D / f).write_text(text); print("synced", f, len(text))
    except Exception as e:
        ok = False; print("sync failed, keeping previous", f, e)
sys.exit(0)
