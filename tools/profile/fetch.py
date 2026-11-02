#!/usr/bin/env python3
"""Fetch public contribution calendar for a user (no token needed) -> data/contributions.json.
Keeps previous file on failure."""
import json, re, sys, urllib.request, pathlib
USER = sys.argv[1] if len(sys.argv) > 1 else "pboling"
OUT = pathlib.Path(__file__).resolve().parents[2] / "data" / "contributions.json"
try:
    html = urllib.request.urlopen(urllib.request.Request(
        f"https://github.com/users/{USER}/contributions", headers={"User-Agent": "profile-gen"}), timeout=30).read().decode()
    counts = {}
    for m in re.finditer(r'for="(contribution-day-component-\d+-\d+)"[^>]*>(No|\d+) contributions? on', html):
        counts[m[1]] = 0 if m[2] == "No" else int(m[2])
    days = []
    for m in re.finditer(r'data-date="([\d-]+)" id="(contribution-day-component-\d+-\d+)"', html):
        days.append({"date": m[1], "count": counts.get(m[2], 0)})
    days.sort(key=lambda d: d["date"])
    assert len(days) > 300, "too few days"
    OUT.write_text(json.dumps({"user": USER, "days": days}, indent=0))
    print(f"{len(days)} days, {sum(d['count'] for d in days)} contributions")
except Exception as e:
    print("fetch failed, keeping previous:", e); sys.exit(0 if OUT.exists() else 1)
