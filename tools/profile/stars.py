#!/usr/bin/env python3
"""Stars gained per featured repo -> data/stars.json and data/trending.json (top 12).
No network: reads the star-event history that galtzo.com keeps per repo (data/star_history/<owner>--<repo>.yml,
copied by sync_data.py). Each file maps day -> list of star times; `observed` holds GitHub's count by day."""
import datetime, json, pathlib
import yaml

ROOT = pathlib.Path(__file__).resolve().parents[2]
HIST = ROOT / "data" / "star_history"
DAYS = 365
today = datetime.date.today()
cut = (today - datetime.timedelta(days=DAYS)).isoformat()
cut30 = (today - datetime.timedelta(days=30)).isoformat()
projects = yaml.safe_load((ROOT / "data/projects.yml").read_text())
owners = {}
for p in projects:
    f = next((f for f in p.get("forges", []) if f["type"] == "GitHub"), None)
    if f and f.get("owner"):
        owners.setdefault(f["url"].rstrip("/").lower().replace("https://github.com/", ""), f["owner"])

cache = {}
for path in sorted(HIST.glob("*.yml")):
    d = yaml.safe_load(path.read_text())
    repo = d["repo"]
    days = {day: len(times) for day, times in d["stars"].items() if day >= cut}
    obs = d.get("observed") or {}
    total = obs[max(obs)] if obs else sum(len(t) for t in d["stars"].values())
    cache[repo.lower()] = dict(gain=sum(days.values()), gain30=sum(n for day, n in days.items() if day >= cut30),
                               days=days, total=total, owner=owners.get(repo.lower(), repo.split("/")[0]), at=d["synced_through"])
(ROOT / "data" / "stars.json").write_text(json.dumps(cache, separators=(",", ":"), sort_keys=True) + "\n")
out = [dict(repo=sl, name=sl.split("/")[1], owner=v["owner"], gain=v["gain"], gain30=v["gain30"], total=v["total"])
       for sl, v in cache.items() if v["gain"]]
out.sort(key=lambda r: -r["gain"])
(ROOT / "data" / "trending.json").write_text(json.dumps(dict(days=DAYS, generated=today.isoformat(), repos=out[:12]), indent=1) + "\n")
print(f"{len(cache)} repos from star history; top:", [(r["name"], r["gain"]) for r in out[:4]])
