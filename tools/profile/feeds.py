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

# --- posts: dev.to plus any extra RSS/Atom feeds listed in EXTRA_FEEDS, merged and sorted by date
import email.utils, re, xml.etree.ElementTree as ET
EXTRA_FEEDS = ["https://railsbling.com/index.xml"]   # stale since 2023 today, but picks up new posts if revived

def rss_posts(url):
    root = ET.fromstring(urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=30).read())
    out = []
    for it in root.iter("item"):
        try:
            d = email.utils.parsedate_to_datetime(it.findtext("pubDate")).date().isoformat()
        except Exception:
            continue
        out.append(dict(title=(it.findtext("title") or "").strip(), url=(it.findtext("link") or "").strip(), date=d,
                        minutes=None, reactions=None, tags=[]))
    return out

posts = []
try:
    arts = get(f"https://dev.to/api/articles?username={USER_DEVTO}&per_page=10")
    posts += [dict(title=a["title"], url=a["url"], date=a["published_at"][:10], minutes=a["reading_time_minutes"],
                   reactions=a["public_reactions_count"], tags=a["tag_list"] if isinstance(a["tag_list"], list) else []) for a in arts]
except Exception as e:
    print("dev.to failed:", e)
for feed in EXTRA_FEEDS:
    try: posts += rss_posts(feed)
    except Exception as e: print("feed failed:", feed, e)
if posts:
    seen_urls = set(); merged = []
    for p_ in sorted(posts, key=lambda x: x["date"], reverse=True):
        if p_["url"] not in seen_urls: seen_urls.add(p_["url"]); merged.append(p_)
    save("posts.json", merged[:10]); print(f"posts: {len(merged[:10])}, newest {merged[0]['date']}")
else:
    print("no posts fetched, keeping previous")

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
