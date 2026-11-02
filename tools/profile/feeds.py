#!/usr/bin/env python3
"""Fetch recent posts (dev.to), recent releases and first-release dates -> data/posts.json,
data/releases.json, data/first_release.json. Keyless public APIs only. Failures keep previous files."""
import datetime, json, pathlib, sys, time, urllib.parse, urllib.request
import yaml

ROOT = pathlib.Path(__file__).resolve().parents[2]
D = ROOT / "data"
UA = {"User-Agent": "profile-gen (github.com/pboling/pboling)"}
USER_DEVTO = "galtzo"

def get(url):
    for attempt in range(3):
        try:
            return json.load(urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=30))
        except urllib.error.HTTPError as e:
            if e.code == 404: return None
            time.sleep(2 * (attempt + 1))
        except Exception:
            time.sleep(2 * (attempt + 1))
    raise RuntimeError(url)

def save(name, obj):
    (D / name).write_text(json.dumps(obj, indent=1, ensure_ascii=False) + "\n")

# --- posts
try:
    arts = get(f"https://dev.to/api/articles?username={USER_DEVTO}&per_page=10")
    posts = [dict(title=a["title"], url=a["url"], date=a["published_at"][:10], minutes=a["reading_time_minutes"],
                  reactions=a["public_reactions_count"], tags=a["tag_list"] if isinstance(a["tag_list"], list) else []) for a in arts]
    save("posts.json", posts); print(f"posts: {len(posts)}")
except Exception as e:
    print("posts failed, keeping previous:", e)

# --- releases + first releases
projects = yaml.safe_load((D / "projects.yml").read_text())
first_path = D / "first_release.json"
first = json.loads(first_path.read_text()) if first_path.exists() else {}
mine = [p for p in projects if p.get("role") != "contributor"]
releases, errors = [], 0
for p in mine:
    if p["ecosystem"] != "rubygems": continue
    try:
        vs = get(f"https://rubygems.org/api/v1/versions/{p['name']}.json")
    except Exception:
        errors += 1; continue
    if not vs: continue
    for v in vs[:3]:
        releases.append(dict(name=p["name"], version=v["number"], date=v["created_at"][:10], at=v["created_at"],
                             url=f"https://rubygems.org/gems/{p['name']}/versions/{v['number']}", registry="rubygems"))
    first[f"rubygems:{p['name']}"] = min(v["created_at"] for v in vs)[:10]
for p in projects:           # first release for registries where it's cheap and immutable
    key = f"{p['ecosystem']}:{p['name']}"
    if key in first or p["ecosystem"] not in ("cargo", "npm"): continue
    try:
        if p["ecosystem"] == "cargo":
            d = get(f"https://crates.io/api/v1/crates/{p['name']}"); first[key] = d["crate"]["created_at"][:10] if d else None
        else:
            d = get(f"https://registry.npmjs.org/{urllib.parse.quote(p['name'], safe='@')}"); first[key] = d["time"]["created"][:10] if d else None
    except Exception:
        errors += 1
if releases:
    releases.sort(key=lambda r: r["at"], reverse=True)
    save("releases.json", releases[:30]); save("first_release.json", first)
    print(f"releases: {len(releases)} found, first-release dates: {len(first)}, errors: {errors}")
else:
    print("no releases fetched, keeping previous"); sys.exit(0 if (D / "releases.json").exists() else 1)
