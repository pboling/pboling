#!/usr/bin/env python3
"""Cumulative star history for the flagship repo -> data/star-history.json (monthly points).
Reads every stargazer's starred_at (about 22 requests for oauth2). Keeps the previous file on failure."""
import datetime, json, os, pathlib, re, subprocess, sys, urllib.request

REPO = "ruby-oauth/oauth2"            # flagship; change here (render.py reads whatever this file says)
OUT = pathlib.Path(__file__).resolve().parents[2] / "data" / "star-history.json"
token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
if not token:
    try: token = subprocess.check_output(["gh", "auth", "token"], text=True, stderr=subprocess.DEVNULL).strip()
    except Exception: token = None
if not token:
    print("no GitHub token, keeping previous star-history.json"); sys.exit(0 if OUT.exists() else 1)

def api(path):
    req = urllib.request.Request(f"https://api.github.com{path}", headers={
        "Authorization": f"Bearer {token}", "Accept": "application/vnd.github.star+json", "User-Agent": "profile-gen"})
    r = urllib.request.urlopen(req, timeout=30)
    return json.load(r), r.headers.get("Link", "")

try:
    first, link = api(f"/repos/{REPO}/stargazers?per_page=100&page=1")
    m = re.search(r'[?&]page=(\d+)>; rel="last"', link)
    pages = [first] + [api(f"/repos/{REPO}/stargazers?per_page=100&page={p}")[0] for p in range(2, (int(m[1]) if m else 1) + 1)]
    times = sorted(s["starred_at"][:7] for page in pages for s in page)      # YYYY-MM, ascending
    if not times: raise RuntimeError("no stargazers")
    start = datetime.date.fromisoformat(times[0] + "-01")
    today = datetime.date.today()
    months, y, mo = [], start.year, start.month
    while (y, mo) <= (today.year, today.month):
        months.append(f"{y:04d}-{mo:02d}"); mo += 1
        if mo == 13: y, mo = y + 1, 1
    per = {}
    for t in times: per[t] = per.get(t, 0) + 1
    cum, series = 0, []
    for mth in months:
        cum += per.get(mth, 0); series.append([mth, cum])
    OUT.write_text(json.dumps(dict(repo=REPO, total=cum, series=series), separators=(",", ":")) + "\n")
    print(f"{REPO}: {cum} stars, {len(series)} monthly points, first {times[0]}")
except Exception as e:
    print("star history failed, keeping previous:", e); sys.exit(0 if OUT.exists() else 1)
