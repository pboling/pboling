#!/usr/bin/env python3
"""Stars gained per owned repo -> data/stars.json (cache) and data/trending.json (top 12).
Uses the stargazers API (starred_at timestamps) from the last page(s) backwards, so no history file is needed.
Needs GITHUB_TOKEN (Actions provides one) or a logged-in `gh`; without a token it keeps the previous file."""
import datetime, json, os, pathlib, re, subprocess, sys, urllib.request
import yaml

ROOT = pathlib.Path(__file__).resolve().parents[2]
OUT = ROOT / "data" / "trending.json"
DAYS = 365   # headline window; 30d is recorded too
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

# Incremental: refresh only the stalest LIMIT repos per run (cached in data/stars.json) so a run never
# spends more than a small slice of the API budget. `--limit 999` seeds everything.
LIMIT = int(sys.argv[sys.argv.index("--limit") + 1]) if "--limit" in sys.argv else 12
CACHE = ROOT / "data" / "stars.json"
cache = json.loads(CACHE.read_text()) if CACHE.exists() else {}
order = sorted(repos, key=lambda sl: cache.get(sl, {}).get("at", ""))
fails = 0; done = 0
for slug in order[:LIMIT]:
    p, owner = repos[slug]
    try:
        g, g30 = gain(slug)
    except Exception:
        fails += 1; continue
    cache[slug] = dict(gain=g, gain30=g30, total=p.get("github_stars") or 0, owner=owner or slug.split("/")[0],
                       at=datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds"))
    done += 1
cache = {k: v for k, v in cache.items() if k in repos}      # drop repos that are no longer tracked
CACHE.write_text(json.dumps(cache, indent=1, sort_keys=True) + "\n")
out = [dict(repo=sl, name=sl.split("/")[1], owner=v["owner"], gain=v["gain"], gain30=v["gain30"], total=v["total"])
       for sl, v in cache.items() if v["gain"]]
out.sort(key=lambda r: -r["gain"])
OUT.write_text(json.dumps(dict(days=DAYS, generated=datetime.date.today().isoformat(), repos=out[:12]), indent=1) + "\n")
print(f"refreshed {done}/{min(LIMIT, len(order))} (fails {fails}); {len(cache)}/{len(repos)} cached; top:", [(r['name'], r['gain']) for r in out[:4]])
