#!/usr/bin/env python3
"""Stars gained in the last 30 days per owned repo -> data/trending.json.
Uses the stargazers API (starred_at timestamps) from the last page(s) backwards, so no history file is needed.
Needs GITHUB_TOKEN (Actions provides one) or a logged-in `gh`; without a token it keeps the previous file."""
import datetime, json, os, pathlib, re, subprocess, sys, urllib.request
import yaml

ROOT = pathlib.Path(__file__).resolve().parents[2]
OUT = ROOT / "data" / "trending.json"
DAYS = int(sys.argv[1]) if len(sys.argv) > 1 else 365   # headline window; 30d is recorded too
token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
if not token:
    try: token = subprocess.check_output(["gh", "auth", "token"], text=True, stderr=subprocess.DEVNULL).strip()
    except Exception: token = None
if not token:
    print("no GitHub token, keeping previous trending.json"); sys.exit(0 if OUT.exists() else 1)

def api(path):
    req = urllib.request.Request(f"https://api.github.com{path}", headers={
        "Authorization": f"Bearer {token}", "Accept": "application/vnd.github.star+json", "User-Agent": "profile-gen"})
    r = urllib.request.urlopen(req, timeout=30)
    return json.load(r), r.headers.get("Link", "")

NOW = datetime.datetime.now(datetime.timezone.utc)
cutoff = NOW - datetime.timedelta(days=DAYS)
cut30 = NOW - datetime.timedelta(days=30)
projects = yaml.safe_load((ROOT / "data/projects.yml").read_text())
repos = {}
for p in projects:
    if p.get("role") == "contributor": continue
    f = next((f for f in p.get("forges", []) if f["type"] == "GitHub"), None)
    if not f or not (p.get("github_stars") or 0): continue
    repos.setdefault(f["url"].rstrip("/").lower().replace("https://github.com/", ""), (p, f.get("owner")))

def gain(slug):
    data, link = api(f"/repos/{slug}/stargazers?per_page=100")
    m = re.search(r'[?&]page=(\d+)>; rel="last"', link)
    last = int(m[1]) if m else 1
    n = n30 = 0; page = last
    while page >= 1:
        rows = data if page == 1 and last == 1 else api(f"/repos/{slug}/stargazers?per_page=100&page={page}")[0]
        times = [datetime.datetime.fromisoformat(r["starred_at"].replace("Z", "+00:00")) for r in rows]
        n += sum(t >= cutoff for t in times); n30 += sum(t >= cut30 for t in times)
        if not times or min(times) < cutoff: break
        page -= 1
    return n, n30

out, fails = [], 0
for slug, (p, owner) in sorted(repos.items()):
    try:
        g, g30 = gain(slug)
    except Exception as e:
        fails += 1; continue
    if g: out.append(dict(repo=slug, name=slug.split("/")[1], owner=owner or slug.split("/")[0], gain=g, gain30=g30, total=p.get("github_stars") or 0))
out.sort(key=lambda r: -r["gain"])
if out or not fails:
    OUT.write_text(json.dumps(dict(days=DAYS, generated=datetime.date.today().isoformat(), repos=out[:12]), indent=1) + "\n")
    print(f"{len(out)} repos gained stars in {DAYS}d, fails {fails}; top:", [(r['name'], r['gain']) for r in out[:5]])
else:
    print("all failed, keeping previous"); sys.exit(1)
