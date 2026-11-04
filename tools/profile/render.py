#!/usr/bin/env python3
"""Render profile SVGs from data/*.yml + data/contributions.json -> assets/profile/*.svg.
Theme: galtzo.com card motif + sm-urb-design (StructuredMerge) palette. Deterministic."""
import json, math, pathlib, random, datetime, textwrap
from xml.sax.saxutils import escape as _esc
def esc(t): return _esc(str(t), {'"': "&quot;"})
import yaml, pngalpha, city

ROOT = pathlib.Path(__file__).resolve().parents[2]
OUT = ROOT / "assets" / "profile"; OUT.mkdir(parents=True, exist_ok=True)
import shutil
for _d in ("projects", "new", "feed", "contributors", "trending", "history", "banner", "sponsors", "phone"): shutil.rmtree(OUT/_d, ignore_errors=True)
for _f in ("projects.svg", "feed.svg", "contributors.svg"): (OUT/_f).unlink(missing_ok=True)
projects = yaml.safe_load((ROOT/"data/projects.yml").read_text())
person = yaml.safe_load((ROOT/"data/person.yml").read_text())
cal = json.loads((ROOT/"data/contributions.json").read_text())["days"]
def _load(n, default):
    f = ROOT/"data"/n
    return json.loads(f.read_text()) if f.exists() else default
posts, releases, first_release = _load("posts.json", []), _load("releases.json", []), _load("first_release.json", {})
trending = _load("trending.json", {"days": 365, "repos": []})
stars_cache = _load("stars.json", {})
def _sponsors():
    f = ROOT/"data"/"sponsors.yml"
    items = yaml.safe_load(f.read_text()) if f.exists() else []
    return [x for x in items if not x.get("until") or datetime.date.fromisoformat(str(x["until"])) >= datetime.date.today()]
sponsors = _sponsors()
def sponsor_uri(name):
    f = ROOT/"assets"/"sponsors"/name
    mime = {"svg": "image/svg+xml", "png": "image/png", "jpg": "image/jpeg"}.get(f.suffix.lstrip("."), "image/png")
    return f"data:{mime};base64," + base64.b64encode(f.read_bytes()).decode() if f.exists() else None
import base64
TODAY = datetime.date.today()
def owner_of(p):
    f = next((f for f in p.get("forges", []) if f["type"] == "GitHub"), None)
    return (f or {}).get("owner")
_logo_cache = {}
def logo_uri(owner):
    """data: URI for the cached org logo (assets/logos), or None. External images are blocked inside SVGs."""
    if owner not in _logo_cache:
        _logo_cache[owner] = None
        for ext, mime in (("png", "image/png"), ("jpg", "image/jpeg")):
            f = ROOT/"assets"/"logos"/f"{owner}.{ext}"
            if f.exists(): _logo_cache[owner] = f"data:{mime};base64," + base64.b64encode(f.read_bytes()).decode(); break
    return _logo_cache[owner]
# Neon: the glyph plus two blurred copies of itself, so numbers glow in their own color.
NGLOW = ('<filter id="nglow" x="-30%" y="-60%" width="160%" height="220%"><feGaussianBlur in="SourceGraphic" stdDeviation="1.1" result="a"/>'
         '<feGaussianBlur in="SourceGraphic" stdDeviation="2.8" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="a"/><feMergeNode in="SourceGraphic"/></feMerge></filter>')
def cov_color(pct):
    """Coverage badge colors (shields/coveralls style): green, yellow, orange, red as it gets worse."""
    return "#4cd964" if pct >= 90 else "#f2d12f" if pct >= 75 else "#ff9a2e" if pct >= 50 else "#ff5a4a"
def star_mark(x, y, size, c):
    """A real star shape (the ★ glyph was a tiny font character); x = left edge, y = text baseline."""
    cx, cy, ro = x + size*.54, y - size*.34, size*.54
    ri = ro*.42
    pts_ = " ".join(f"{cx + (ro if k % 2 == 0 else ri)*math.sin(k*math.pi/5):.1f},{cy - (ro if k % 2 == 0 else ri)*math.cos(k*math.pi/5):.1f}" for k in range(10))
    return f'<polygon points="{pts_}" fill="{c}" filter="url(#nglow)"/>'
def spark(p, n=25):
    """Cumulative stars at n evenly spaced days over the last year (summed over the card's repos), or None.
    From the star-event history in data/stars.json: the count a year ago plus each day's gains."""
    repos = p.get("_repos") or ([gh_repo(p)] if gh_repo(p) else [])
    dates = [(TODAY - datetime.timedelta(days=round(365*(n-1-i)/(n-1)))).isoformat() for i in range(n)]
    series, found = [0]*n, False
    for repo in repos:
        c = stars_cache.get(repo.replace("https://github.com/", ""))
        if not c: continue
        found = True
        start = max(0, c["total"] - c["gain"])
        for i, d in enumerate(dates): series[i] += start + sum(v for day, v in c["days"].items() if day <= d)
    return series if found else None
def spark_mark(p, x, y, w, h):
    """The star history as a tiny glowing line (y = text baseline of the row it sits in), or ''."""
    series = spark(p)
    if not series or len(series) < 2: return ""
    lo, hi = min(series), max(series)
    span = (hi - lo) or 1
    pts_ = [(x + i*w/(len(series)-1), y - 1 - (v - lo)/span*(h-2)) for i, v in enumerate(series)]
    line = " ".join(f"{a:.1f},{b:.1f}" for a, b in pts_)
    return (f'<polygon points="{pts_[0][0]:.1f},{y-1:.1f} {line} {pts_[-1][0]:.1f},{y-1:.1f}" fill="{AMBER}" fill-opacity=".14"/>'
            f'<g filter="url(#nglow)"><polyline points="{line}" fill="none" stroke="{AMBER}" stroke-width="1.2" stroke-linejoin="round"/>'
            f'<circle cx="{pts_[-1][0]:.1f}" cy="{pts_[-1][1]:.1f}" r="1.5" fill="{AMBER}"/></g>')   # grouped: a flat line alone has no height for the filter to use
def stat_text(sym, val, c, x, y, fs, gap=" "):
    """One bottom-row number: a drawn star or the symbol, then the value, all glowing."""
    if sym == "★":
        return star_mark(x, y, fs, c) + f'<text x="{x+fs*1.45:.1f}" y="{y}" font-size="{fs}" style="fill:{c}" filter="url(#nglow)">{val}</text>'
    return f'<text x="{x}" y="{y}" font-size="{fs}" style="fill:{c}" filter="url(#nglow)">{sym}{gap}{val}</text>'
def logo_defs(owners):
    return "<defs>" + NGLOW + "".join(f'<image id="lg-{esc(o)}" href="{logo_uri(o)}" width="64" height="64" preserveAspectRatio="xMidYMid slice"/>'
                              for o in sorted(set(owners)) if o and logo_uri(o)) + "</defs>"
_lang_cache = {}
LIGHT_TILE = {"Bash", "Rust"}          # dark artwork: sits on a light tile, like org logos on the dark card
def lang_uri(lang):
    if lang not in _lang_cache:
        f = ROOT/"assets"/"langs"/f"{lang}.svg"
        _lang_cache[lang] = "data:image/svg+xml;base64," + base64.b64encode(f.read_bytes()).decode() if f.exists() else None
    return _lang_cache[lang]
def lang_icon(lang, x, y, size):
    """galtzo.com's language mark at (x, y); "" when we have none."""
    uri = lang_uri(lang)
    if not uri: return ""
    if lang in LIGHT_TILE:
        pad = size*.14
        return (f'<rect x="{x:.1f}" y="{y:.1f}" width="{size}" height="{size}" rx="{size*.22:.1f}" fill="#e8eefc"/>'
                f'<image x="{x+pad:.1f}" y="{y+pad:.1f}" width="{size-2*pad:.1f}" height="{size-2*pad:.1f}" href="{uri}"/>')
    return f'<image x="{x:.1f}" y="{y:.1f}" width="{size}" height="{size}" href="{uri}"/>'
def lang_badge(p, xr, cy, size, text=True, fs=11):
    """Language mark(s) right-aligned at xr, vertically centred on cy: icon + minimum version for one language,
    a row of icons for a roll-up, a dot and the name for languages we have no mark for."""
    langs = p.get("_lang_list") or [p.get("language")]
    icons = [l for l in langs if lang_uri(l)]
    if not icons:
        return (f'<circle cx="{xr-60}" cy="{cy}" r="4" fill="{LANG.get(p.get("language"), MUTED)}"/>'
                f'<text x="{xr-50}" y="{cy+4}" font-size="{fs}" class="m">{esc(str(p.get("language") or "")[:10])}</text>') if text else ""
    out, x = "", xr
    mv = p.get("minimum_version") if text and len(icons) == 1 else None
    if mv:
        label = f"≥ {mv}"
        out += f'<text x="{x}" y="{cy+4}" font-size="{fs}" class="m" text-anchor="end">{esc(label)}</text>'
        x -= len(label)*fs*.62 + 6
    for l in reversed(icons[:4]):
        x -= size
        out += lang_icon(l, x, cy-size/2, size)
        x -= 4
    return out
_float_cache = {}
def logo_floats(owner):
    """Transparent PNGs (logos.galtzo.com art made for dark backgrounds) skip the white tile."""
    if owner not in _float_cache:
        f = ROOT/"assets"/"logos"/f"{owner}.png"
        _float_cache[owner] = f.exists() and pngalpha.floats_on_dark(f)
    return _float_cache[owner]
def logo_at(owner, x, y, size):
    if not owner or not logo_uri(owner): return ""
    k = size/64
    if logo_floats(owner):
        return f'<g transform="translate({x},{y}) scale({k:.4f})"><use href="#lg-{esc(owner)}"/></g>'
    return (f'<g transform="translate({x},{y}) scale({k:.4f})"><rect width="64" height="64" rx="12" fill="#fff"/>'
            f'<use href="#lg-{esc(owner)}"/></g><rect x="{x}" y="{y}" width="{size}" height="{size}" rx="{size*12/64:.1f}" fill="none" stroke="{EDGE}"/>')
def is_new(p):
    d = p.get("_first_release") or first_release.get(f"{p['ecosystem']}:{p['name']}")
    return bool(d) and (TODAY - datetime.date.fromisoformat(d)).days <= 365
def ago(d):
    n = (TODAY - datetime.date.fromisoformat(d)).days
    return "today" if n <= 0 else f"{n}d ago" if n < 60 else f"{n//30}mo ago"

# palette: sm-urb-design "sm" brand (teal primary, violet secondary, amber tertiary) on dark paper
BG, PANEL, EDGE = "#0e1718", "#14211f", "#25403c"
TEAL, VIOLET, AMBER, PAPER, MUTED = "#4fc3b3", "#a58bf5", "#e8b04a", "#f4efe4", "#8fa6a1"
# Role colors: no red/green (CI pass/fail connotation; collapse for deuteranopes). Orange/teal/lavender stay >=46 dE apart under deutan, protan and tritan simulation.
DLGREEN = "#16a34a"   # download figure on cards; roles no longer use green, so it is free
ROLE = {"author": "#ff8a1f", "maintainer": "#2dd4bf", "contributor": "#c084fc"}
LANG = {"Ruby": "#e0463c", "Rust": "#e8a15a", "Go": "#4fc3d9", "TypeScript": "#5b9bea", "JavaScript": "#e8d44a", "Bash": "#7fcf6a"}
W = 880
MONO = "ui-monospace,SFMono-Regular,Menlo,Consolas,monospace"
SANS = "system-ui,-apple-system,'Segoe UI',Roboto,sans-serif"

def human(n):
    n = float(n)
    for lim, s in ((1e9, "B"), (1e6, "M"), (1e3, "K")):
        if n >= lim: return f"{n/lim:.1f}".rstrip("0").rstrip(".") + s
    return str(int(n))

import shutil
README_ROWS = []   # filled as sections render; written to README.md at the end
def svg(name, h, body, title, vb=None):
    """Write assets/profile/<name>.svg. vb=(x, y, w, h) crops a window out of a full-layout drawing (used for tiles)."""
    css = f"""text{{font-family:{MONO};fill:{PAPER}}} .s{{font-family:{SANS}}} .m{{fill:{MUTED}}}
    @keyframes bl{{50%{{opacity:0}}}} .cur{{animation:bl 1.1s steps(1) infinite}}
    @keyframes fl{{0%,100%{{opacity:1}}50%{{opacity:.35}}}} .w{{animation:fl 3s ease-in-out infinite}}
    @media (prefers-reduced-motion:reduce){{.cur,.w{{animation:none}}}}"""
    x0, y0, w, hh = vb or (0, 0, W, h)
    path = OUT/f"{name}.svg"; path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w:g}" height="{hh:g}" viewBox="{x0:g} {y0:g} {w:g} {hh:g}" role="img" aria-label="{esc(title)}">'
        f'<title>{esc(title)}</title><style>{css}</style><rect x="{x0:g}" y="{y0:g}" width="{w:g}" height="{hh:g}" fill="{BG}"/>{body}</svg>')

README_ITEMS = []
def readme_row(*items):
    """items: (src, alt, width_pct, href|None). Composed into HTML at the end so phone variants can be detected."""
    README_ITEMS.append(items)
def img_html(src, alt, pct, href):
    desktop = f'<img src="./assets/profile/{src}.svg" width="{pct}%" align="top" alt="{esc(alt)}">'
    if (OUT/"phone"/f"{src}.svg").exists():
        desktop = (f'<picture><source media="(max-width: 600px)" srcset="./assets/profile/phone/{src}.svg">{desktop}</picture>')
    return f'<a href="{esc(href)}">{desktop}</a>' if href else desktop

def edges(y0, y1, x0=0, x1=W, color=EDGE, top=False, bottom=False):
    """Panel border pieces for a window: left/right sides when the window touches the page edge."""
    o = ""
    if x0 <= 0: o += f'<line x1="1" y1="{y0}" x2="1" y2="{y1}" stroke="{color}"/>'
    if x1 >= W: o += f'<line x1="{W-1}" y1="{y0}" x2="{W-1}" y2="{y1}" stroke="{color}"/>'
    if top: o += f'<line x1="1" y1="{y0+0.5}" x2="{W-1}" y2="{y0+0.5}" stroke="{color}"/>'
    if bottom: o += f'<line x1="1" y1="{y1-0.5}" x2="{W-1}" y2="{y1-0.5}" stroke="{color}"/>'
    return o
def head_bar(label, h, color=EDGE, right=""):
    return (edges(0, h, color=color, top=True) +
            f'<text x="16" y="22" font-size="11" class="m" letter-spacing="2">{esc(label.upper())}</text>{right}'
            f'<line x1="16" y1="32" x2="{W-16}" y2="32" stroke="{EDGE}"/>')

def chrome(label, h):
    """Console window frame segment label."""
    return (f'<rect x="1" y="0" width="{W-2}" height="{h}" fill="none" stroke="{EDGE}"/>'
            f'<text x="16" y="22" font-size="11" class="m" letter-spacing="2">{esc(label.upper())}</text>'
            f'<line x1="16" y1="32" x2="{W-16}" y2="32" stroke="{EDGE}"/>')

# ---- aggregates
owned = [p for p in projects if p.get("role") != "contributor"]      # author + maintainer
contrib = [p for p in projects if p.get("role") == "contributor"]  # work on other people's projects
def gh_repo(p):
    f = next((f for f in p.get("forges", []) if f["type"] == "GitHub"), None)
    return f["url"].rstrip("/").lower() if f else None
def gh_release_dl(p):
    f = next((f for f in p.get("forges", []) if f["type"] == "GitHub"), None)
    return (f or {}).get("total_downloads") or 0
seen_repos = set()
def tally(plist):
    """Downloads/stars for a set of package entries. One entry per package per registry, so
    registry downloads sum per entry, but anything repo-level (stars, GitHub release assets)
    is counted once per repository, and never again in a later group (seen_repos)."""
    dl = sum(p.get("total_downloads") or 0 for p in plist)
    day = sum(p.get("daily_downloads") or 0 for p in plist)
    stars = rel = 0; repos = set()
    for repo in {gh_repo(p) for p in plist if gh_repo(p)} - seen_repos:
        group = [p for p in plist if gh_repo(p) == repo]
        stars += max(p.get("github_stars") or 0 for p in group)
        rel += max(gh_release_dl(p) for p in group)
        repos.add(repo)
    seen_repos.update(repos)
    stars += sum(p.get("github_stars") or 0 for p in plist if not gh_repo(p))
    windows = sorted({p["downloads_basis"] for p in plist if p.get("downloads_basis") not in (None, "lifetime")})
    n_repos = len({gh_repo(p) or p["name"] for p in plist})
    return dict(dl=dl + rel, reg=dl, rel=rel, day=day, stars=stars, packages=len(plist), repos=n_repos, windows=windows)
owned = [p for p in projects if p.get("role") != "contributor"]      # author + maintainer
contrib = [p for p in projects if p.get("role") == "contributor"]  # work on other people's projects
T_OWN = tally(owned); T_CON = tally(contrib)
tot_dl, day_dl, stars, n_proj = T_OWN["dl"], T_OWN["day"], T_OWN["stars"], T_OWN["packages"]
WINDOW_NOTE = {"180d": "PyPI = last 180 days", "18mo": "npm = last 18 months"}
def basis_note(t):
    w = [WINDOW_NOTE.get(x, x) for x in t["windows"]]
    return "includes GitHub release assets" + ("; " + ", ".join(w) if w else "")
scraped = max((p.get("last_scrape_at") or "")[:10] for p in projects)
contrib_total = sum(d["count"] for d in cal)

# ---- header
b = f'<rect x="1" y="0" width="{W-2}" height="190" fill="none" stroke="{EDGE}"/>'
for i, c in enumerate(("#dc2626", "#e8b04a", "#16a34a")):
    b += f'<circle cx="{22+i*18}" cy="22" r="5" fill="{c}"/>'
b += f'<text x="{W-16}" y="26" font-size="11" class="m" text-anchor="end">pboling@galtzo ~ zsh</text>'
b += f'<line x1="0" y1="40" x2="{W}" y2="40" stroke="{EDGE}"/>'
b += f'<text x="24" y="72" font-size="14" fill="{TEAL}" style="fill:{TEAL}">$ whoami</text>'
b += f'<text x="24" y="118" class="s" font-size="40" font-weight="700" letter-spacing="-1">Hi, I am <tspan style="fill:{TEAL}">Peter Boling</tspan></text>'
b += f'<text x="24" y="146" font-size="14" class="m">team leader · web architect · security researcher · rubyist · building for web since 2004</text>'
b += f'<text x="24" y="172" font-size="14" style="fill:{AMBER}">$ <tspan class="cur" style="fill:{PAPER}">█</tspan></text>'
svg("header", 190, b, "Peter Boling: team leader, web architect, security researcher, rubyist")

# ---- stats
def tile_row(tiles, y=46, accent=None):
    out = ""; tw = (W-32-3*12)/4
    for i, (k, v, sub, col) in enumerate(tiles):
        x = 16 + i*(tw+12)
        out += (f'<rect x="{x}" y="{y}" width="{tw}" height="72" rx="4" fill="{PANEL}" stroke="{EDGE}"/>'
                f'<rect x="{x}" y="{y}" width="3" height="72" fill="{accent or col}"/>'
                f'<text x="{x+16}" y="{y+20}" font-size="10" class="m" letter-spacing="2">{k}</text>'
                f'<text x="{x+16}" y="{y+50}" class="s" font-size="28" font-weight="700" style="fill:{col}">{v}</text>'
                f'<text x="{x+16}" y="{y+65}" font-size="9" class="m">{esc(sub[:34])}</text>')
    return out
def eco_line(ps):
    c = {}
    for p in ps: c[p["ecosystem"]] = c.get(p["ecosystem"], 0) + 1
    return " · ".join(f"{v} {k}" for k, v in sorted(c.items(), key=lambda x: -x[1]) if k != "none")
tiles = [("DOWNLOADS", human(tot_dl), "registries + release assets", TEAL),
         ("PER DAY", human(day_dl), "per day, authored + maintained", VIOLET),
         ("PACKAGES", str(n_proj), eco_line(owned), AMBER),
         ("STARS", human(stars), "on GitHub", TEAL)]
b = chrome("telemetry · projects I author & maintain", 142) + tile_row(tiles) + f'<text x="16" y="134" font-size="9" class="m">{esc(basis_note(T_OWN))}</text>'
svg("stats", 142, b, f"Projects I author or maintain: {human(tot_dl)} lifetime downloads, {human(day_dl)} per day, {n_proj} projects, {human(stars)} stars")

# ---- contribution city (tools/profile/city.py)
CH = 470
city_body, city_alt = city.build(cal, W, CH, dict(PANEL=PANEL, EDGE=EDGE, TEAL=TEAL, AMBER=AMBER, PAPER=PAPER, MUTED=MUTED), contrib_total)
svg("city", CH, chrome(f"contribution city · {contrib_total:,} contributions · last 12 months", CH) + city_body, city_alt)

# ---- project cards (galtzo card motif)
def wrap(s, n, k):
    s = "".join(ch for ch in (s or "") if ord(ch) < 0x2000).strip()
    full = textwrap.wrap(" ".join(s.split()), n); lines = full[:k]
    if len(full) > k: lines[-1] = lines[-1][:n-1].rstrip(" ,.") + "…"
    return lines
# Featured cards: mine, still maintained (not archived) and not up for adoption. Totals above still count everything I own.
featured = [p for p in owned if not p.get("adoptable") and p.get("status") != "archived"]
def first_rel(q): return first_release.get(f"{q['ecosystem']}:{q['name']}")
def earliest(plist): return min((d for q in plist if (d := first_rel(q))), default=None)
def group_card(plist):
    """One card per upstream repo: all of its registry packages rolled up (alef, tree-sitter-language-pack, ...)."""
    g = dict(plist[0])
    seen_registry = {(p["ecosystem"]) for p in plist}
    rel = max(gh_release_dl(p) for p in plist)
    g["name"] = plist[0]["name"] if len(plist) == 1 else gh_repo(plist[0]).split("/")[-1]
    g["total_downloads"] = sum(p.get("total_downloads") or 0 for p in plist) + rel
    g["daily_downloads"] = sum(p.get("daily_downloads") or 0 for p in plist)
    g["github_stars"] = max(p.get("github_stars") or 0 for p in plist)
    g["language"] = plist[0]["language"] if len(plist) == 1 else plist[0]["language"]
    g["_regs"] = len(seen_registry) if len(plist) > 1 else 0
    g["_pkgs"] = len(plist)
    return g
# Cards that stand for several entries rank, and show, once: the same project on several registries
# (tree-sitter-language-pack) and the structuredmerge family (many gems/crates/packages across four
# languages). Downloads are summed; a group's first release is its earliest member's, so NEW is honest.
# Family roll-ups come from galtzo.com's families.yml: `rollup: <id>` groups every family sharing the id
# (structuredmerge spans four), `rollup_lead: <project>` names the member that supplies name/description/install.
FAMILIES = {f["id"]: f for f in yaml.safe_load((ROOT/"data/families.yml").read_text())}
def rollup_of(p):
    return (FAMILIES.get(p.get("family_id")) or {}).get("rollup")
def filter_tags(p):
    """The same filter tags galtzo.com puts on a card (its data-tags), so the site can reuse that filter UI."""
    year = str(p.get("first_commit_by_person_on") or "").split("/")[0]
    tags = list(p.get("tags") or []) + [p.get("role")] + ([year] if year else [])
    if p.get("minimum_version"): tags.append(f'{p["language"]} >= {p["minimum_version"]}')
    for key, lang in (("minimum_typescript_version", "TypeScript"), ("minimum_node_version", "Node.js")):
        if p.get(key): tags.append(f"{lang} >= {p[key]}")
    return sorted(set(t for t in tags if t))
COVERAGE_KEYS = ("coverage", "coverage_branch", "coverage_lines_covered", "coverage_lines_total", "coverage_release")
def rollup_card(rid, plist):
    fams = [FAMILIES[f] for f in dict.fromkeys(q.get("family_id") for q in plist) if f in FAMILIES]
    lead_name = next((f["rollup_lead"] for f in fams if f.get("rollup_lead")), None)
    lead = next((q for q in plist if q["name"] == lead_name), None)
    g = dict(lead or plist[0])
    langs = sorted({q.get("language") for q in plist if q.get("language")})
    if not lead: g.update(name=rid, ecosystem=None, language="multi-lang", description=f"{len(plist)} packages across {', '.join(langs)}")
    g.update(_rollup=True, _pkgs=len(plist), _langs=len(langs))
    if len(langs) > 1: g["_lang_list"] = [l for l, _ in __import__("collections").Counter(q.get("language") for q in plist).most_common()]
    g["_tag"] = (f"multi-language monorepos · {len(plist)} packages · {len(langs)} languages" if len(langs) > 1
                 else f"{fams[0]['name']} · {len(plist)} packages")
    g["_tag_phone"] = f"multi-language · {len(plist)} packages · {len(langs)} langs" if len(langs) > 1 else f"{len(plist)} pkgs"
    g["total_downloads"] = sum(q.get("total_downloads") or 0 for q in plist)
    g["daily_downloads"] = sum(q.get("daily_downloads") or 0 for q in plist)
    per_repo = {}
    for q in plist: per_repo[gh_repo(q)] = max(per_repo.get(gh_repo(q), 0), q.get("github_stars") or 0)
    g["github_stars"] = sum(per_repo.values())
    g["_first_release"] = earliest(plist)
    # Coverage rolls up as pooled lines over the members that report it; the rest are ignored.
    for k in COVERAGE_KEYS: g.pop(k, None)
    rep = [q for q in plist if q.get("coverage_lines_total")]
    if rep:
        cov, tot = sum(q["coverage_lines_covered"] for q in rep), sum(q["coverage_lines_total"] for q in rep)
        g.update(coverage=100.0*cov/tot, coverage_lines_covered=cov, coverage_lines_total=tot)
    g["owner"] = any(q.get("owner") for q in plist); g["releaser"] = any(q.get("releaser") for q in plist)
    g["_members"] = sorted(q["name"] for q in plist)
    g["_repos"] = sorted({gh_repo(q) for q in plist if gh_repo(q)})
    g["_tags"] = sorted({t for q in plist for t in filter_tags(q)})
    return g
def collapse(plists):
    out, poly, same = [], {}, {}
    for p in plists:
        key = rollup_of(p)
        if key: poly.setdefault(key, []).append(p)
        else: same.setdefault((gh_repo(p) or id(p), p["name"]), []).append(p)
    for v in same.values():
        if len({q["ecosystem"] for q in v}) > 1:
            g = group_card(v); g["_first_release"] = earliest(v)
            for k in COVERAGE_KEYS: g.pop(k, None)
            g["owner"] = any(q.get("owner") for q in v); g["releaser"] = any(q.get("releaser") for q in v)
            out.append(g)
        else: out.extend(v)
    return out + [rollup_card(k, v) for k, v in poly.items()]
featured = collapse(featured)
ranked = sorted(featured, key=lambda p: -(p.get("total_downloads") or 0))
TOP = 24
CW, CHT = (W-32-12)/2, 128
def mini_card(i, p, y0, cols=3, link=False):
    cw, ch = (W-32-(cols-1)*12)/cols, 84
    col, row = i % cols, i//cols
    x, y = 16 + col*(cw+12), y0 + row*(ch+10)
    lc = LANG.get(p.get("language"), MUTED)
    n = p.get("_pkgs", 1)
    g = (f'<rect x="{x}" y="{y}" width="{cw}" height="{ch}" rx="4" fill="{PANEL}" stroke="{EDGE}"/>'
         f'<rect x="{x}" y="{y}" width="4" height="{ch}" fill="{ROLE["contributor"]}"/>'
         + logo_at(owner_of(p), x+14, y+8, 22) +
         lang_badge(p, x+cw-12, y+20, 16, text=False) +
         f'<text x="{x+42}" y="{y+25}" class="s" font-size="14" font-weight="700">{esc(p["name"][:(14 if n > 1 else 22)])}{"…" if n > 1 and len(p["name"]) > 14 else ""}</text>')
    if n > 1:
        g += f'<text x="{x+cw-26}" y="{y+24}" font-size="9" class="m" text-anchor="end">{n} pkgs · {p["_regs"]} regs</text>'
    for k, line in enumerate(wrap(p.get("description"), 40, 1)):
        g += f'<text x="{x+18}" y="{y+44}" class="s m" font-size="10.5">{esc(line)}</text>'
    st = [("★", human(p.get("github_stars") or 0), AMBER), ("↓", human(p.get("total_downloads") or 0), DLGREEN), ("↓/d", human(p.get("daily_downloads") or 0), VIOLET)]
    sx = x+18
    for sym, val, c in st:
        g += stat_text(sym, val, c, sx, y+ch-12, 11); sx += 80
    url = next((f["url"] for f in p.get("forges", []) if f["type"] == "GitHub"), None)
    return f'<a href="{esc(url)}">{g}</a>' if url and link else g
def card(i, p, y0=46, link=False):
    col, row = i % 2, i//2
    x, y = 16 + col*(CW+12), y0 + row*(CHT+12)
    rc = ROLE.get(p.get("role"), MUTED); lc = LANG.get(p.get("language"), MUTED)
    nx0 = x + (48 if logo_uri(owner_of(p) or "") else 18)
    g = (f'<rect x="{x}" y="{y}" width="{CW}" height="{CHT}" rx="4" fill="{PANEL}" stroke="{EDGE}"/>'
         f'<rect x="{x}" y="{y}" width="4" height="{CHT}" fill="{rc}"/>'
         f'<text x="{nx0}" y="{y+26}" class="s" font-size="16" font-weight="700">{esc(p["name"][:24])}</text>'
         + logo_at(owner_of(p), x+16, y+8, 24) +
         lang_badge(p, x+CW-14, y+22, 18))
    if is_new(p) and p.get("role") != "contributor":
        nx = x + CW - 132 - (22*min(4, len(p['_lang_list'])) - 40 if p.get('_lang_list') else 0)
        g += (f'<rect x="{nx:.0f}" y="{y+12}" width="36" height="16" rx="8" fill="{AMBER}"/>'
              f'<text x="{nx+18:.0f}" y="{y+24}" font-size="9" font-weight="700" text-anchor="middle" style="fill:{BG}">NEW</text>')
    for k, line in enumerate(wrap(p.get("description"), 46, 3)):
        g += f'<text x="{x+18}" y="{y+48+k*15}" class="s m" font-size="11.5">{esc(line)}</text>'
    cmd = install_cmd(p, 52)
    if cmd:
        wpx = len(cmd)*6.2 + 24
        g += (f'<rect x="{x+18}" y="{y+85}" width="{wpx:.0f}" height="18" rx="3" fill="{BG}" stroke="{EDGE}"/>'
              f'<text x="{x+27}" y="{y+98}" font-size="10"><tspan style="fill:{MUTED}">$</tspan> {esc(cmd)}</text>')
    st = [("★", human(p.get("github_stars") or 0), AMBER), ("↓", human(p.get("total_downloads") or 0), DLGREEN),
          ("↓/d", human(p.get("daily_downloads") or 0), VIOLET)]
    sx = x+18
    for sym, val, c in st:
        g += stat_text(sym, val, c, sx, y+CHT-14, 12)
        sx += (17 + len(val)*7.2 if sym == "★" else len(sym + " " + val)*7.2) + 14
        if sym == "★":
            m = spark_mark(p, sx, y+CHT-14, 30, 12)
            if m: g += m; sx += 30 + 12
    if p.get("coverage") is not None:
        cc = cov_color(p["coverage"])
        g += (f'<text x="{sx}" y="{y+CHT-14}" font-size="12"><tspan style="fill:{MUTED}">cov</tspan> '
              f'<tspan style="fill:{cc}" filter="url(#nglow)">{p["coverage"]:.0f}%</tspan></text>')
    cy = y + 50
    for flag, label in (("owner", "OWNER"), ("releaser", "RELEASER")):
        if p.get(flag):
            wch = len(label)*6.4 + 12
            g += (f'<rect x="{x+CW-14-wch:.0f}" y="{cy}" width="{wch:.0f}" height="15" rx="7.5" fill="none" stroke="{rc}" stroke-opacity=".7"/>'
                  f'<text x="{x+CW-14-wch/2:.0f}" y="{cy+11}" font-size="8.5" font-weight="700" letter-spacing=".5" text-anchor="middle" style="fill:{rc}">{label}</text>')
            cy += 21
    if p.get("_rollup"):
        g += f'<text x="{x+CW-14}" y="{y+CHT-32}" font-size="9" class="m" text-anchor="end">{esc(p["_tag"])}</text>'
    elif p.get("_pkgs", 1) > 1:
        g += f'<text x="{x+CW-14}" y="{y+CHT-32}" font-size="9" class="m" text-anchor="end">{p["_pkgs"]} packages · {p["_regs"]} registries</text>'
    g += f'<text x="{x+CW-14}" y="{y+CHT-14}" font-size="10" font-weight="700" letter-spacing="1" text-anchor="end" style="fill:{rc}">{esc(str(p.get("role", "")).upper())}</text>'
    url = next((f["url"] for f in p.get("forges", []) if f["type"] == "GitHub"), None)
    return f'<a href="{esc(url)}">{g}</a>' if url and link else g
# ---- trending: stars gained (tools/profile/stars.py). 30 days is too quiet to show (+5 at best), so the headline is 12 months.
TR = trending["repos"][:6]
if TR:
    TW, TH = W/3, 90
    ttl = f"stars gained in the last {'12 months' if trending['days'] == 365 else str(trending['days']) + ' days'}"
    svg("trending/head", 0, head_bar("trending · " + ttl, 40), "Trending: " + ttl, vb=(0, 0, W, 40))
    readme_row(("trending/head", "Trending: " + ttl, 100, None))
    for r in range((len(TR)+2)//3):
        items = []
        for col in range(3):
            i = r*3 + col
            if i >= len(TR): break
            t = TR[i]; y = 46 + r*TH
            cx = col*TW; cw = (W-32-24)/3; lx0 = 16 + col*(cw+12)
            body = (f'<rect x="{lx0}" y="{y}" width="{cw}" height="{TH-8}" rx="4" fill="{PANEL}" stroke="{EDGE}"/>'
                    + logo_at(t["owner"], lx0+12, y+10, 22)
                    + f'<text x="{lx0+42}" y="{y+26}" class="s" font-size="14" font-weight="700">{esc(t["name"][:20])}</text>'
                    f'<text x="{lx0+12}" y="{y+62}" class="s" font-size="26" font-weight="700" style="fill:{TEAL}">+{t["gain"]}</text>'
                    f'<text x="{lx0+cw-12}" y="{y+52}" font-size="10" class="m" text-anchor="end">★ {human(t["total"])} total</text>'
                    f'<text x="{lx0+cw-12}" y="{y+66}" font-size="10" class="m" text-anchor="end">+{t["gain30"]} in 30 days</text>'
                    + edges(y-3, y+TH-3, cx, cx+TW))
            name = f"trending/{i+1:02d}"
            alt = f'{t["name"]}: +{t["gain"]} stars in the last year, {t["gain30"]} in the last 30 days, {t["total"]} total'
            svg(name, 0, logo_defs([t["owner"]]) + body, alt, vb=(cx, y-3, TW, TH))
            items.append((name, alt, 33.33, f'https://github.com/{t["repo"]}'))
        readme_row(*items)
    yb = 46 + ((len(TR)+2)//3)*TH - 3
    svg("trending/foot", 0, edges(yb, yb+10, bottom=True), "", vb=(0, yb, W, 10))
    readme_row(("trending/foot", "", 100, None))

# ---- stacked stars gained over the last 12 months (tools/profile/stars.py -> data/stars.json)
# Floor = total stars a year ago; each band is one repo's gain since then, stacked, labeled. Repos with a
# single star are never drawn on their own: they (and everything below the top-N) fold into a grey band.
STACK_DAYS, MAX_BANDS, BAND_MIN_GAIN = 365, 12, 2
STACK_COLORS = [TEAL, VIOLET, AMBER, "#e0463c", "#5b9bea", "#7fcf6a", "#d96fc0", "#4fc3d9", "#e8a15a", "#c6d95a", "#9b8cf5", "#f08c8c"]
REST_COLOR = "#6b7f7a"
def stack_model():
    rows = [(sl, v) for sl, v in stars_cache.items() if v.get("days") is not None]
    if not rows: return None
    start = TODAY - datetime.timedelta(days=STACK_DAYS)
    dates = [start + datetime.timedelta(days=7*i) for i in range(STACK_DAYS//7 + 1)]
    if dates[-1] != TODAY: dates.append(TODAY)
    gains = {sl: sum(v["days"].values()) for sl, v in rows}
    total_gain = sum(gains.values())
    if not total_gain: return None
    baseline = sum(v["total"] for _, v in rows) - total_gain
    cum = lambda v, d: sum(n for ds, n in v["days"].items() if ds <= d.isoformat())
    ranked_ = sorted(((sl, v) for sl, v in rows if gains[sl] >= BAND_MIN_GAIN), key=lambda t: -gains[t[0]])
    own = ranked_[:MAX_BANDS]; own_ids = {sl for sl, _ in own}
    rest = [(sl, v) for sl, v in rows if sl not in own_ids and gains[sl] >= 1]
    bands = []
    if rest:
        bands.append(dict(label=f"+{len(rest)} more", color=REST_COLOR, total=sum(gains[sl] for sl, _ in rest),
                          values=[sum(cum(v, d) for _, v in rest) for d in dates]))
    for i, (sl, v) in enumerate(own):
        bands.append(dict(label=sl.split("/")[1], color=STACK_COLORS[i % len(STACK_COLORS)], total=gains[sl], values=[cum(v, d) for d in dates]))
    return dict(dates=dates, bands=bands, total=total_gain, baseline=baseline, repos=len([1 for sl in gains if gains[sl]]), start=start)
stack = stack_model()
def nice_step(raw):
    p = 10 ** math.floor(math.log10(raw))
    return next(m * p for m in (1, 2, 2.5, 5, 10) if m * p >= raw)
def stack_alt():
    return (f"Stars gained by projects I author or maintain over the last 12 months, stacked by repo: +{stack['total']} on a base of "
            f"{stack['baseline']:,} a year ago. " + ", ".join(f'{b["label"]} +{b["total"]}' for b in reversed(stack["bands"])) + ".")
def stack_plot(px0, px1, py0, py1, big=True):
    st = stack; dates = st["dates"]
    step = nice_step(st["total"] / 4); ymax = math.ceil(st["total"] / step) * step
    t0 = dates[0].toordinal(); span = dates[-1].toordinal() - t0
    X = lambda d: px0 + (px1 - px0) * (d.toordinal() - t0) / span
    Y = lambda v: py1 - (py1 - py0) * v / ymax
    fs = 10 if big else 8.5
    o = ""
    for v in range(0, ymax + 1, step):
        o += (f'<line x1="{px0}" y1="{Y(v):.1f}" x2="{px1}" y2="{Y(v):.1f}" stroke="{EDGE}" stroke-opacity="{1 if v == 0 else .55}"/>'
              f'<text x="{px0-8}" y="{Y(v)+3:.1f}" font-size="{fs}" class="m" text-anchor="end">{"floor" if v == 0 else f"+{v}"}</text>')
    seen_m = set()
    for d in dates:
        if d.day <= 7 and (d.year, d.month) not in seen_m and d.month % (2 if big else 3) == 1 or (d.day <= 7 and d.month == 1 and (d.year, 1) not in seen_m):
            seen_m.add((d.year, d.month))
            lbl = d.strftime("%b") + (f" '{str(d.year)[2:]}" if d.month == 1 else "")
            o += f'<text x="{X(d):.1f}" y="{py1+16}" font-size="{fs}" class="m" text-anchor="middle">{lbl}</text>'
    lower = [0] * len(dates)
    for bi, b in enumerate(st["bands"]):
        top = [lower[i] + v for i, v in enumerate(b["values"])]
        up = " ".join(f"{X(d):.1f},{Y(top[i]):.1f}" for i, d in enumerate(dates))
        down = " ".join(f"{X(d):.1f},{Y(lower[i]):.1f}" for i, d in reversed(list(enumerate(dates))))
        o += (f'<polygon points="{up} {down}" fill="{b["color"]}" fill-opacity=".30"/>'
              f'<polyline points="{up}" fill="none" stroke="{b["color"]}" stroke-width="{1.6 if big else 1.3}" stroke-linejoin="round"/>')
        lower = top
    return o, Y, st
if stack:
    HS = 380
    px0, px1, py0, py1 = 64, 690, 92, 330
    plot, Y, st = stack_plot(px0, px1, py0, py1)
    body = head_bar("stars gained · last 12 months", 40) + plot + edges(40, HS, bottom=True)
    body += (f'<text x="16" y="64" font-size="12" class="m">stacked by repo · floor = {st["baseline"]:,} stars a year ago</text>'
             f'<text x="{W-16}" y="64" font-size="12" text-anchor="end"><tspan style="fill:{TEAL}" font-weight="700">+{st["total"]}★</tspan><tspan class="m"> across {st["repos"]} repos</tspan></text>')
    # right-gutter labels at each band's midpoint, at least 15px apart (jdx-style)
    base = 0; want = []
    for b in st["bands"]:
        want.append(Y(base + b["total"] / 2)); base += b["total"]
    placed = list(want)
    for i in range(1, len(placed)): placed[i] = min(placed[i], placed[i-1] - 15)
    shift_down = max(0, py0 - 4 - placed[-1])
    for i, b in enumerate(st["bands"]):
        y = placed[i] + shift_down
        body += (f'<path d="M{px1+2} {want[i]:.1f}L{px1+12} {y:.1f}" stroke="{b["color"]}" stroke-opacity=".6" fill="none"/>'
                 f'<text x="{px1+16}" y="{y+4:.1f}" font-size="11" style="fill:{b["color"]}">{esc(b["label"][:18])} <tspan class="m">+{b["total"]}</tspan></text>')
    svg("history/chart", 0, body, "Stars gained: " + stack_alt(), vb=(0, 0, W, HS))
    readme_row(("history/chart", "Stars gained: " + stack_alt(), 100, None))

rows = math.ceil(TOP/2)
def gh_url(p): return next((f["url"] for f in p.get("forges", []) if f["type"] == "GitHub"), None)
INSTALL = {"rubygems": "gem install {n}", "cargo": "cargo add {n}", "npm": "npm i {n}", "pypi": "pip install {n}",
           "nuget": "dotnet add package {n}", "packagist": "composer require {n}", "go": "go get {n}"}
def install_cmd(p, limit):
    t = INSTALL.get(p.get("ecosystem"))
    if not t: return None
    c = t.format(n=p["name"])
    return c if len(c) <= limit else c[:limit-1] + "…"
def card_alt(p):
    return (f'{p["name"]}, {p.get("role")}: {" ".join((p.get("description") or "").split())[:120]} '
            f'{human(p.get("github_stars") or 0)} stars, {human(p.get("total_downloads") or 0)} downloads')
def role_key(roles, x_end, y, fs, sw):
    out, x = "", x_end
    for role in reversed(roles):
        w = len(role)*fs*0.68 + sw + 8
        x -= w
        out += f'<rect x="{x:.0f}" y="{y-sw+1}" width="{sw}" height="{sw}" rx="1" fill="{ROLE[role]}"/><text x="{x+sw+6:.0f}" y="{y}" font-size="{fs}" font-weight="700" letter-spacing="1" style="fill:{ROLE[role]}">{role.upper()}</text>'
        x -= 14
    return out
svg("projects/head", 40, head_bar("projects I author & maintain · sort: lifetime downloads desc", 40, right=role_key(["author", "maintainer"], W-16, 22, 11, 10)), "Projects I author and maintain, sorted by lifetime downloads descending", vb=(0, 0, W, 40))
readme_row(("projects/head", "Projects I author and maintain, sorted by lifetime downloads descending", 100, None))
for r in range(rows):
    items = []
    for col in range(2):
        i = r*2 + col
        if i >= min(TOP, len(ranked)): break
        pr = ranked[i]; y = 46 + r*(CHT+12)
        body = logo_defs([owner_of(pr)]) + card(i, pr) + edges(y-6, y+CHT+6, col*W/2, (col+1)*W/2)
        name = f"projects/{i+1:02d}"
        svg(name, 0, body, card_alt(pr), vb=(col*W/2, y-6, W/2, CHT+12))
        items.append((name, card_alt(pr), 50, gh_url(pr)))
    readme_row(*items)
yf = 46 + rows*(CHT+12) - 6
foot = edges(yf, yf+34, bottom=True)
foot += f'<text x="{W-16}" y="{yf+21}" font-size="10" class="m" text-anchor="end">data: galtzo.com · scraped {scraped}</text>'
svg("projects/foot", 0, foot, "Data source and scrape date", vb=(0, yf, W, 34))
readme_row(("projects/foot", "Data source and scrape date", 100, None))

# ---- new projects: first released in the last 12 months, not already in the top list above.
NEW_TOP = 10
def new_candidates():
    in_top = {id(p) for p in ranked[:TOP]}
    fresh = [p for p in featured if id(p) not in in_top and is_new(p)]
    return sorted(fresh, key=lambda p: -(p.get("total_downloads") or 0))[:NEW_TOP]
newp = new_candidates()
NEW_LABEL = "new projects · first released in the last 12 months · not in the top 24"
if newp:
    svg("new/head", 40, head_bar(NEW_LABEL, 40), "New projects first released in the last 12 months, not in the top 24 list, by lifetime downloads", vb=(0, 0, W, 40))
    readme_row(("new/head", "New projects first released in the last 12 months, not in the top 24 list", 100, None))
    nrows = math.ceil(len(newp)/2)
    for r in range(nrows):
        items = []
        for col in range(2):
            i = r*2 + col
            if i >= len(newp): break
            pr = newp[i]; y = 46 + r*(CHT+12)
            body = logo_defs([owner_of(pr)]) + card(i, pr) + edges(y-6, y+CHT+6, col*W/2, (col+1)*W/2)
            name = f"new/{i+1:02d}"
            svg(name, 0, body, card_alt(pr), vb=(col*W/2, y-6, W/2, CHT+12))
            items.append((name, card_alt(pr), 50, gh_url(pr)))
        readme_row(*items)
    yf = 46 + nrows*(CHT+12) - 6
    svg("new/foot", 0, edges(yf, yf+10, bottom=True), "", vb=(0, yf, W, 10))
    readme_row(("new/foot", "", 100, None))

# ---- recent releases + writing (data: tools/profile/feeds.py)
seen = set(); latest = []
for r in releases:                       # newest release per gem, so one busy gem can't fill the panel
    if r["name"] not in seen: seen.add(r["name"]); latest.append(r)
PW = (W-32-12)/2; RN = 7
def fmt_rel(r, x, y, w):
    return (f'<text x="{x+12}" y="{y+19}" font-size="12" style="fill:{TEAL}">{esc(r["name"][:22])}</text>'
            f'<text x="{x+w-72}" y="{y+19}" font-size="11" text-anchor="end" style="fill:{VIOLET}">v{esc(r["version"][:14])}</text>'
            f'<text x="{x+w-12}" y="{y+19}" font-size="10" class="m" text-anchor="end">{ago(r["date"])}</text>')
def fmt_post(a, x, y, w):
    title = "".join(ch for ch in a["title"] if ord(ch) < 0x2000).strip()
    t = title if len(title) <= 44 else title[:43].rstrip() + "…"
    return (f'<text x="{x+12}" y="{y+13}" class="s" font-size="11.5" font-weight="600">{esc(t)}</text>'
            f'<text x="{x+12}" y="{y+25}" font-size="9" class="m">{a["date"]}' + (f' · {a["minutes"]} min read' if a.get("minutes") else '') + (f' · ♥ {a["reactions"]}' if a.get("reactions") is not None else '') + '</text>')
newest = posts[0]["date"] if posts else None
stale = f" · LATEST {ago(newest).upper()}" if newest and (TODAY - datetime.date.fromisoformat(newest)).days > 90 else ""
svg("feed/head", 0, head_bar("recent releases · rubygems", 40) +
    f'<text x="{16+PW+12}" y="22" font-size="11" class="m" letter-spacing="2">WRITING{stale}</text>', "Recent releases and writing", vb=(0, 0, W, 40))
readme_row(("feed/head", "Recent gem releases and recent writing", 100, None))
for i in range(RN):
    items = []; y = 46 + i*34
    for col, (src, fmt, kind) in enumerate(((latest, fmt_rel, "release"), (posts, fmt_post, "post"))):
        if i >= len(src): items.append(None); continue
        it = src[i]; x = 16 + col*(PW+12)
        body = (f'<rect x="{x}" y="{y}" width="{PW}" height="30" rx="3" fill="{PANEL}" stroke="{EDGE}"/>' + fmt(it, x, y, PW)
                + edges(y-2, y+32, col*W/2, (col+1)*W/2))
        name = f"feed/{kind}-{i+1:02d}"
        alt = f'{it["name"]} {it["version"]} released {it["date"]}' if kind == "release" else f'{it["title"]} ({it["date"]})'
        svg(name, 0, body, alt, vb=(col*W/2, y-2, W/2, 34))
        items.append((name, alt, 50, it["url"]))
    readme_row(*[i_ for i_ in items if i_])
yf = 46 + RN*34
svg("feed/foot", 0, edges(yf-2, yf+10, bottom=True), "", vb=(0, yf-2, W, 12))
readme_row(("feed/foot", "", 100, None))

# ---- contributor section (other people's projects; clearly separate)
by_repo = {}
for p in contrib: by_repo.setdefault(gh_repo(p) or p["name"], []).append(p)
cranked = sorted((group_card(v) for v in by_repo.values()), key=lambda p: -p["total_downloads"])
PURPLE = ROLE["contributor"]
ctiles = [("UPSTREAM DOWNLOADS", human(T_CON["dl"]), "registries + release assets", TEAL),
          ("UPSTREAM PER DAY", human(T_CON["day"]), "per day, whole projects", VIOLET),
          ("PACKAGES", str(T_CON["packages"]), f"{T_CON['repos']} repos", AMBER),
          ("UPSTREAM STARS", human(T_CON["stars"]), "on GitHub", TEAL)]
HCH = 148
hb = (head_bar("other people's projects I have contributed to", HCH, color=PURPLE,
               right=role_key(["contributor"], W-16, 22, 11, 10))
      + tile_row(ctiles, accent=PURPLE) + f'<text x="16" y="132" font-size="9" class="m">{esc(basis_note(T_CON))}</text>')
ct_alt = (f"Contributor totals: {human(T_CON['dl'])} upstream downloads, {human(T_CON['day'])} per day, "
          f"{T_CON['packages']} packages in {T_CON['repos']} repos, {human(T_CON['stars'])} stars. Not included in my totals.")
svg("contributors/head", 0, hb.replace(f'<line x1="1" y1="0.5"', '<line x1="1" y1="0.5"'), ct_alt, vb=(0, 0, W, HCH))
readme_row(("contributors/head", ct_alt, 100, None))
CWID = W/3
for r in range(math.ceil(len(cranked)/3)):
    items = []
    for col in range(3):
        i = r*3 + col
        if i >= len(cranked): break
        pr = cranked[i]; y = HCH + r*94
        body = logo_defs([owner_of(pr)]) + mini_card(i, pr, HCH) + edges(y-5, y+89, col*CWID, (col+1)*CWID, color=PURPLE)
        name = f"contributors/{i+1:02d}"
        alt = card_alt(pr)
        svg(name, 0, body, alt, vb=(col*CWID, y-5, CWID, 94))
        items.append((name, alt, 33.33, gh_url(pr)))
    for col in range(len(items), 3):     # pad the last row so <p align=center> doesn't center it
        svg(f"contributors/blank-{col+1}", 0, edges(HCH, HCH+94, col*CWID, (col+1)*CWID, color=PURPLE), "", vb=(col*CWID, HCH, CWID, 94))
        items.append((f"contributors/blank-{col+1}", "", 33.33, None))
    readme_row(*items)
yf = HCH + math.ceil(len(cranked)/3)*94 - 5
svg("contributors/foot", 0, edges(yf, yf+34, color=PURPLE, bottom=True) +
    f'<text x="16" y="{yf+20}" font-size="10" class="m">Contributor project tallies are separate from author / maintainer tallies.</text>',
    "Contributor tallies are separate from author / maintainer tallies", vb=(0, yf, W, 34))
readme_row(("contributors/foot", "Contributor project tallies are separate from author / maintainer tallies", 100, None))

# ---- sponsors (data/sponsors.yml): logos for sponsors who are already public, text names for minor donors
SPN = [x for x in sponsors if x["tier"] in ("personal", "project")]
MINOR = [x for x in sponsors if x["tier"] == "minor"]
def sponsor_tile_body(sp, x, y, w, h):
    uri = sponsor_uri(sp.get("logo", ""))
    o = f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="4" fill="{PANEL}" stroke="{EDGE}"/>'
    if uri:
        o += (f'<rect x="{x+12}" y="{y+12}" width="{w*0.36:.0f}" height="{h-24}" rx="8" fill="#fff"/>'
              f'<image href="{uri}" x="{x+20}" y="{y+18}" width="{w*0.36-16:.0f}" height="{h-36}" preserveAspectRatio="xMidYMid meet"/>')
    tx = x + 12 + w*0.36 + 16
    o += f'<text x="{tx:.0f}" y="{y+30}" class="s" font-size="15" font-weight="700">{esc(sp["name"])}</text>'
    lines = textwrap.wrap(sp.get("scope") or "", 34)[:2]
    sub = sp.get("via") and f"via {sp['via']}" or (sp.get("since") and f"since {str(sp['since'])[:7]}") or ""
    lines += [sub] if sub else []
    for k, ln in enumerate(lines[:3]):
        o += f'<text x="{tx:.0f}" y="{y+45+k*12}" font-size="10" class="m">{esc(ln)}</text>'
    return o
if sponsors:
    svg("sponsors/head", 0, head_bar("sponsors · thank you", 40), "Sponsors: thank you", vb=(0, 0, W, 40))
    readme_row(("sponsors/head", "Sponsors: thank you", 100, None))
    SH = 92
    for r in range((len(SPN)+1)//2):
        items = []
        for col in range(2):
            i = r*2 + col
            if i >= len(SPN): break
            sp = SPN[i]; y = 6
            body = sponsor_tile_body(sp, col*W/2 + (16 if col == 0 else 6), y, W/2 - 22 if col == 0 else W/2 - 22, SH-12) + edges(0, SH, col*W/2, (col+1)*W/2)
            name = f"sponsors/{i+1:02d}"
            alt = f'{sp["name"]}: {sp.get("scope", "")}' + (f' (via {sp["via"]})' if sp.get("via") else "")
            svg(name, 0, body, alt, vb=(col*W/2, 0, W/2, SH))
            items.append((name, alt, 50, sp["url"]))
        readme_row(*items)
    if MINOR:
        txt = " · ".join(f'{m["name"]}' for m in MINOR)
        via = ", ".join(sorted({m["via"] for m in MINOR if m.get("via")}))
        body = (edges(0, 40, bottom=True) + f'<text x="16" y="25" font-size="11" class="m">Also thank you: <tspan style="fill:{PAPER}">{esc(txt)}</tspan>  ({esc(via)})</text>')
        svg("sponsors/minor", 0, body, "Also thank you: " + txt, vb=(0, 0, W, 40))
        readme_row(("sponsors/minor", "Also thank you: " + txt, 100, None))

# ---- footer
b = f'<rect x="1" y="0" width="{W-2}" height="56" fill="none" stroke="{EDGE}"/>'
b += (f'<text x="24" y="34" font-size="13" class="m">$ open <tspan style="fill:{TEAL}">galtzo.com</tspan> · <tspan style="fill:{VIOLET}">github.com/sponsors/pboling</tspan>'
      f' · connection closed.</text>')
svg("footer", 56, b, "Footer: galtzo.com and sponsors link")
readme_row(("footer", "Connection closed. galtzo.com and github.com/sponsors/pboling", 100, None))
# sponsor banner copy + links (wording drafted from the old README; see #14)
BANNER_LINKS = [("SPONSOR", "GitHub Sponsors", "https://github.com/sponsors/pboling", AMBER),
                ("BACK IT", "Open Collective", "https://opencollective.com/galtzo-floss", TEAL),
                ("HIRE ME", "Available for work", "https://docs.google.com/document/d/1H9fYtkMFmnkQO1sucrFPt5E3dvhozgVtI31LgpNLmJ4/pub", VIOLET),
                ("CHAT", "Discord", "https://discord.gg/3qme4XHNKN", TEAL)]
n_projects = (len(owned) // 100) * 100     # packages I author/maintain, rounded down: "200+"
BANNER_TEXT = ("FLOSS maintenance is a full-time job.", f"Your sponsorship keeps {n_projects}+ libraries maintained, secure and released.")
# ---- phone variants (<= 600px): redesigned at device scale, not just shrunk. See #11.
PHW = 390
def psvg(name, w, h, body, alt):
    css = f"""text{{font-family:{MONO};fill:{PAPER}}} .s{{font-family:{SANS}}} .m{{fill:{MUTED}}}
    @keyframes bl{{50%{{opacity:0}}}} .cur{{animation:bl 1.1s steps(1) infinite}}
    @media (prefers-reduced-motion:reduce){{.cur{{animation:none}}}}"""
    path = OUT/"phone"/f"{name}.svg"; path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(f'<svg xmlns="http://www.w3.org/2000/svg" width="{w:g}" height="{h:g}" viewBox="0 0 {w:g} {h:g}" role="img" aria-label="{esc(alt)}">'
                    f'<title>{esc(alt)}</title><style>{css}</style><rect width="{w:g}" height="{h:g}" fill="{BG}"/>{body}</svg>')
def pedges(w, h, col=0, ncols=1, color=EDGE, top=False, bottom=False):
    o = ""
    if col == 0: o += f'<line x1="1" y1="0" x2="1" y2="{h}" stroke="{color}"/>'
    if col == ncols-1: o += f'<line x1="{w-1}" y1="0" x2="{w-1}" y2="{h}" stroke="{color}"/>'
    if top: o += f'<line x1="0" y1="0.5" x2="{w}" y2="0.5" stroke="{color}"/>'
    if bottom: o += f'<line x1="0" y1="{h-0.5}" x2="{w}" y2="{h-0.5}" stroke="{color}"/>'
    return o
def ptiles(tiles, y, accent=None):
    """2x2 stat tiles at phone scale."""
    o = ""; tw = (PHW-24-8)/2
    for i, (k, v, sub, col) in enumerate(tiles):
        x = 12 + (i % 2)*(tw+8); yy = y + (i//2)*64
        o += (f'<rect x="{x}" y="{yy}" width="{tw}" height="58" rx="4" fill="{PANEL}" stroke="{EDGE}"/>'
              f'<rect x="{x}" y="{yy}" width="3" height="58" fill="{accent or col}"/>'
              f'<text x="{x+12}" y="{yy+16}" font-size="8.5" class="m" letter-spacing="1.5">{k}</text>'
              f'<text x="{x+12}" y="{yy+42}" class="s" font-size="24" font-weight="700" style="fill:{col}">{v}</text>'
              f'<text x="{x+tw-8}" y="{yy+52}" font-size="8" class="m" text-anchor="end">{esc(sub[:26])}</text>')
    return o
def pbar(label, color=EDGE, h=34, right=""):
    return (pedges(PHW, h, color=color, top=True) +
            f'<text x="12" y="21" font-size="10" class="m" letter-spacing="1.5">{esc(label.upper())}</text>{right}')

# header + stats
hb = pedges(PHW, 150, top=True)
for i, c in enumerate(("#dc2626", "#e8b04a", "#16a34a")): hb += f'<circle cx="{16+i*14}" cy="18" r="4" fill="{c}"/>'
hb += (f'<text x="12" y="52" font-size="12" style="fill:{TEAL}">$ whoami</text>'
       f'<text x="12" y="88" class="s" font-size="27" font-weight="700" letter-spacing="-0.5">Hi, I am <tspan style="fill:{TEAL}">Peter Boling</tspan></text>'
       f'<text x="12" y="112" font-size="11" class="m">team leader · web architect</text>'
       f'<text x="12" y="127" font-size="11" class="m">security researcher · rubyist</text>'
       f'<text x="12" y="142" font-size="11" style="fill:{AMBER}">$ <tspan class="cur" style="fill:{PAPER}">█</tspan></text>')
psvg("header", PHW, 150, hb, "Peter Boling: team leader, web architect, security researcher, rubyist")
pst = [("DOWNLOADS", human(tot_dl), "registries + assets", TEAL), ("PER DAY", human(day_dl), "authored + maintained", VIOLET),
       ("PACKAGES", str(n_proj), f"{T_OWN['repos']} repos", AMBER), ("STARS", human(stars), "on GitHub", TEAL)]
psvg("stats", PHW, 172, pedges(PHW, 172) + f'<text x="12" y="22" font-size="10" class="m" letter-spacing="1.5">TELEMETRY · MINE</text>' + ptiles(pst, 32)
     + f'<text x="12" y="166" font-size="8" class="m">{esc(basis_note(T_OWN))}</text>',
     f"Telemetry: {human(tot_dl)} downloads, {human(day_dl)} per day, {n_proj} packages, {human(stars)} stars")

# projects: head, cards (195 wide, two per row), foot
psvg("projects/head", PHW, 34, pbar("projects I author & maintain", right=role_key(["author", "maintainer"], PHW-12, 21, 8, 8)) , "Projects I author and maintain")
def pcard(pr, col):
    w, h = PHW/2, 124
    rc = ROLE.get(pr.get("role"), MUTED)
    o = (pedges(w, h, col, 2) + f'<rect x="6" y="6" width="{w-12}" height="{h-8}" rx="4" fill="{PANEL}" stroke="{EDGE}"/>'
         f'<rect x="6" y="6" width="3" height="{h-8}" fill="{rc}"/>')
    has = bool(logo_uri(owner_of(pr) or ""))
    o += logo_at(owner_of(pr), 16, 14, 20)
    nx = 42 if has else 16
    o += f'<text x="{nx}" y="29" class="s" font-size="12.5" font-weight="700">{esc(pr["name"][:(13 if has else 17)])}</text>'
    if is_new(pr) and pr.get("role") != "contributor":
        o += f'<rect x="{w-40}" y="12" width="28" height="13" rx="6" fill="{AMBER}"/><text x="{w-26}" y="22" font-size="7.5" font-weight="700" text-anchor="middle" style="fill:{BG}">NEW</text>'
    o += lang_badge(pr, w-12, 36, 13, text=False)
    for k, line in enumerate(wrap(pr.get("description"), 31, 2 if install_cmd(pr, 27) else 3)):
        o += f'<text x="16" y="{50+k*12}" class="s m" font-size="9.5">{esc(line)}</text>'
    cmd = install_cmd(pr, 27)
    if cmd:
        o += (f'<rect x="14" y="{h-40}" width="{len(cmd)*5.2+18:.0f}" height="14" rx="3" fill="{BG}" stroke="{EDGE}"/>'
              f'<text x="21" y="{h-30}" font-size="8.5"><tspan style="fill:{MUTED}">$</tspan> {esc(cmd)}</text>')
    st = [("★", human(pr.get("github_stars") or 0), AMBER), ("↓", human(pr.get("total_downloads") or 0), DLGREEN), ("/d", human(pr.get("daily_downloads") or 0), VIOLET)]
    sx = 16
    for sym, val, c in st:
        o += stat_text(sym, val, c, sx, h-14, 9.5, gap="")
        sx += (14 + len(val)*5.7 if sym == "★" else len(sym + val)*5.7) + 9
        if sym == "★":
            m = spark_mark(pr, sx, h-14, 18, 9)
            if m: o += m; sx += 18 + 8
    o += f'<text x="{w-12}" y="{h-23}" font-size="7.5" font-weight="700" letter-spacing="0.5" text-anchor="end" style="fill:{rc}">{esc(str(pr.get("role", "")).upper())}</text>'
    facts = [t for t, on in (("OWNER", pr.get("owner")), ("RELEASER", pr.get("releaser"))) if on]
    if pr.get("coverage") is not None: facts.append(f'cov <tspan style="fill:{cov_color(pr["coverage"])}">{pr["coverage"]:.0f}%</tspan>')
    if facts:
        o += f'<text x="{w-12}" y="{h-6}" font-size="7.5" class="m" text-anchor="end">{" · ".join(facts)}</text>'
    if pr.get("_rollup"):
        o += f'<text x="{w-12}" y="{h-33}" font-size="7.5" class="m" text-anchor="end">{esc(pr["_tag_phone"])}</text>'
    return o, w, h
for i, pr in enumerate(ranked[:TOP]):
    col = i % 2
    body, w, h = pcard(pr, col)
    psvg(f"projects/{i+1:02d}", w, h, logo_defs([owner_of(pr)]) + body, card_alt(pr))
fb = pedges(PHW, 30, bottom=True) + f'<text x="{PHW-12}" y="17" font-size="8" class="m" text-anchor="end">data: galtzo.com · {scraped}</text>'
psvg("projects/foot", PHW, 30, fb, "Data source and scrape date")
if newp:
    psvg("new/head", PHW, 34, pbar("new projects · last 12 months · not in top 24"), "New projects first released in the last 12 months, not in the top 24 list")
    for i, pr in enumerate(newp):
        body, w, h = pcard(pr, i % 2)
        psvg(f"new/{i+1:02d}", w, h, logo_defs([owner_of(pr)]) + body, card_alt(pr))
    psvg("new/foot", PHW, 10, pedges(PHW, 10, bottom=True), "")

# feed: head, release rows, post rows (195 wide, two per row)
psvg("feed/head", PHW, 34, pbar("releases") + f'<text x="{PHW/2+8}" y="21" font-size="10" class="m" letter-spacing="1.5">WRITING{esc(stale.replace(" · LATEST", " ·"))}</text>', "Recent releases and writing")
for i in range(RN):
    if i < len(latest):
        r = latest[i]; w, h = PHW/2, 38
        b_ = (pedges(w, h, 0, 2) + f'<rect x="6" y="2" width="{w-8}" height="34" rx="3" fill="{PANEL}" stroke="{EDGE}"/>'
              f'<text x="14" y="17" font-size="11" style="fill:{TEAL}">{esc(r["name"][:19])}</text>'
              f'<text x="14" y="30" font-size="9" style="fill:{VIOLET}">v{esc(r["version"][:12])}<tspan class="m"> · {ago(r["date"])}</tspan></text>')
        psvg(f"feed/release-{i+1:02d}", w, h, b_, f'{r["name"]} {r["version"]} released {r["date"]}')
    if i < len(posts):
        a_ = posts[i]; w, h = PHW/2, 38
        title = "".join(ch for ch in a_["title"] if ord(ch) < 0x2000).strip()
        t = title if len(title) <= 30 else title[:29].rstrip() + "…"
        b_ = (pedges(w, h, 1, 2) + f'<rect x="2" y="2" width="{w-8}" height="34" rx="3" fill="{PANEL}" stroke="{EDGE}"/>'
              f'<text x="10" y="17" class="s" font-size="10" font-weight="600">{esc(t)}</text>'
              f'<text x="10" y="30" font-size="8.5" class="m">{a_["date"]}</text>')
        psvg(f"feed/post-{i+1:02d}", w, h, b_, f'{a_["title"]} ({a_["date"]})')
psvg("feed/foot", PHW, 10, pedges(PHW, 10, bottom=True), "")

# trending (phone): head + three-up 130px tiles
if TR:
    psvg("trending/head", PHW, 34, pbar("trending · stars, 12 months"), "Trending stars")
    for i, t in enumerate(TR):
        col = i % 3; w, h = PHW/3, 66
        o = (pedges(w, h, col, 3) + f'<rect x="{5 if col == 0 else 2}" y="3" width="{w-8}" height="{h-6}" rx="3" fill="{PANEL}" stroke="{EDGE}"/>'
             + logo_at(t["owner"], 10 if col == 0 else 7, 9, 16)
             + f'<text x="{32 if col == 0 else 29}" y="21" class="s" font-size="10" font-weight="700">{esc(t["name"][:11])}</text>'
             f'<text x="{10 if col == 0 else 7}" y="48" class="s" font-size="19" font-weight="700" style="fill:{TEAL}">+{t["gain"]}</text>'
             f'<text x="{w-8}" y="57" font-size="7.5" class="m" text-anchor="end">★{human(t["total"])}</text>')
        psvg(f"trending/{i+1:02d}", w, h, logo_defs([t["owner"]]) + o, f'{t["name"]}: +{t["gain"]} stars in the last year')
    psvg("trending/foot", PHW, 10, pedges(PHW, 10, bottom=True), "")

# stars gained, stacked (phone): plot on top, two-column legend underneath (top of the stack first)
if stack:
    plot, Y, st = stack_plot(44, PHW-14, 74, 214, big=False)
    legend = list(reversed(st["bands"])); rows_n = (len(legend) + 1) // 2
    PHH = 244 + rows_n * 15 + 12
    o = pedges(PHW, PHH, top=True, bottom=True) + plot
    o += (f'<text x="12" y="21" font-size="10" class="m" letter-spacing="1.5">STARS GAINED · 12 MONTHS</text>'
          f'<text x="12" y="40" font-size="11" style="fill:{TEAL}" font-weight="700">+{st["total"]}★ <tspan class="m" font-weight="400">across {st["repos"]} repos</tspan></text>'
          f'<text x="12" y="55" font-size="8.5" class="m">stacked · floor = {st["baseline"]:,} a year ago</text>')
    for i, b in enumerate(legend):
        cx = 12 + (i % 2) * (PHW/2); cy = 250 + (i // 2) * 15
        o += (f'<rect x="{cx}" y="{cy-8}" width="8" height="8" fill="{b["color"]}"/>'
              f'<text x="{cx+13}" y="{cy}" font-size="9.5">{esc(b["label"][:16])} <tspan class="m">+{b["total"]}</tspan></text>')
    psvg("history/chart", PHW, PHH, o, "Stars gained: " + stack_alt())

# contributors: head (2x2 tiles), mini cards (130 wide, three per row), foot
pct = [("UPSTREAM DL", human(T_CON["dl"]), "registries + assets", TEAL), ("UPSTREAM /DAY", human(T_CON["day"]), "whole projects", VIOLET),
       ("PACKAGES", str(T_CON["packages"]), f"{T_CON['repos']} repos", AMBER), ("UPSTREAM STARS", human(T_CON["stars"]), "on GitHub", TEAL)]
psvg("contributors/head", PHW, 180, pedges(PHW, 180, color=PURPLE, top=True) +
     f'<text x="12" y="21" font-size="9" class="m" letter-spacing="0.8">OTHER PEOPLE’S PROJECTS I’VE CONTRIBUTED TO</text>'
     + role_key(["contributor"], PHW-12, 21, 8, 8) + ptiles(pct, 40, accent=PURPLE) +
     f'<text x="12" y="172" font-size="8" class="m">{esc(basis_note(T_CON))}</text>', ct_alt)
for i, pr in enumerate(cranked):
    col = i % 3; w, h = PHW/3, 64
    n_ = pr.get("_pkgs", 1)
    o = (pedges(w, h, col, 3, color=PURPLE) + f'<rect x="{5 if col == 0 else 2}" y="3" width="{w-8}" height="{h-6}" rx="3" fill="{PANEL}" stroke="{EDGE}"/>'
         + logo_at(owner_of(pr), 10 if col == 0 else 7, 9, 16)
         + f'<text x="{32 if col == 0 else 29}" y="21" class="s" font-size="10.5" font-weight="700">{esc(pr["name"][:14])}</text>'
         f'<text x="{10 if col == 0 else 7}" y="40" font-size="9" style="fill:{TEAL}">↓{human(pr.get("total_downloads") or 0)}</text>'
         f'<text x="{10 if col == 0 else 7}" y="53" font-size="9" style="fill:{AMBER}">★{human(pr.get("github_stars") or 0)}</text>'
         + (f'<text x="{w-8}" y="53" font-size="8" class="m" text-anchor="end">{n_}pkg</text>' if n_ > 1 else ""))
    psvg(f"contributors/{i+1:02d}", w, h, logo_defs([owner_of(pr)]) + o, card_alt(pr))
for col in (range(len(cranked) % 3, 3) if len(cranked) % 3 else []):
    psvg(f"contributors/blank-{col+1}", PHW/3, 64, pedges(PHW/3, 64, col, 3, color=PURPLE), "")
psvg("contributors/foot", PHW, 30, pedges(PHW, 30, color=PURPLE, bottom=True) +
     f'<text x="12" y="18" font-size="8" class="m">Contributor tallies are separate from author / maintainer tallies.</text>', "Contributor tallies are separate from author / maintainer tallies")
# banner (phone): copy + 2x2 buttons
psvg("banner/banner", PHW, 92, pedges(PHW, 92, top=True) + f'<rect x="12" y="14" width="3" height="62" fill="{AMBER}"/>'
     f'<text x="24" y="34" class="s" font-size="15" font-weight="700">FLOSS maintenance is my</text>'
     f'<text x="24" y="52" class="s" font-size="15" font-weight="700">full-time job.</text>'
     f'<text x="24" y="72" font-size="9.5" class="m">Sponsorship keeps {n_projects}+ libraries</text>'
     f'<text x="24" y="85" font-size="9.5" class="m">maintained, secure and released.</text>', BANNER_TEXT[0] + " " + BANNER_TEXT[1])
for i, (k, sub, url, col) in enumerate(BANNER_LINKS):
    bw = PHW/2; c = i % 2
    body = (pedges(bw, 50, c, 2, bottom=(i >= 2)) +
            f'<rect x="{12 if c == 0 else 4}" y="4" width="{bw-16}" height="42" rx="6" fill="{PANEL}" stroke="{col}" stroke-opacity=".7"/>'
            f'<text x="{24 if c == 0 else 16}" y="21" font-size="8.5" letter-spacing="1.5" style="fill:{col}">{k}</text>'
            f'<text x="{24 if c == 0 else 16}" y="37" class="s" font-size="11" font-weight="600">{esc(sub[:18])}</text>')
    psvg(f"banner/link-{i+1}", bw, 50, body, f"{k.title()}: {sub}")
# city on a phone: the same skyline, scaled to the screen width, with its numbers and legend set at a readable size below it
_scene, _ = city.build(cal, W, 460, dict(PANEL=PANEL, EDGE=EDGE, TEAL=TEAL, AMBER=AMBER, PAPER=PAPER, MUTED=MUTED), contrib_total, text=False)
_k = (PHW - 2)/W
_sh = 440*_k
_active = sum(1 for d in cal if d["count"]); _best = max(cal, key=lambda d: d["count"])
_phase, _event, _at = city.sky()
_ly = _sh + 128
_t = (f'<text x="12" y="{_sh+34:.0f}" font-size="28" font-weight="700" class="s" style="fill:{TEAL}">{contrib_total:,}</text>'
      f'<text x="12" y="{_sh+50:.0f}" font-size="9.5" class="m">contributions · last 12 months</text>'
      f'<text x="12" y="{_sh+66:.0f}" font-size="9.5" class="m">{_active} active days · busiest {_best["date"]}: {_best["count"]}</text>'
      f'<text x="12" y="{_sh+82:.0f}" font-size="9.5" class="m"><tspan style="fill:{city.PHASE_COLOR[_phase]}" font-weight="700">{_phase}</tspan> in New York · {_event} {_at}</text>'
      f'<text x="12" y="{_ly-6:.0f}" font-size="9" class="m">quiet</text>'
      + "".join(f'<rect x="{42+i*14}" y="{_ly-14:.0f}" width="10" height="10" fill="{c[0]}"/>' for i, c in enumerate(city.RAMP))
      + f'<text x="{42+5*14+4}" y="{_ly-6:.0f}" font-size="9" class="m">top 10% of days</text>'
      + "".join(f'<polygon points="{14+i*13},{_ly+6:.0f} {20+i*13},{_ly+9:.0f} {14+i*13},{_ly+12:.0f} {8+i*13},{_ly+9:.0f}" fill="none" stroke="{col}" stroke-width="1.2"/>' for i, col in enumerate(city.NEON[:4]))
      + f'<text x="66" y="{_ly+12:.0f}" font-size="9" class="m">neon ring: the 10 busiest days</text>'
      f'<text x="12" y="{_ly+28:.0f}" font-size="9" class="m">height ranks the day · one building per day</text>')
_h = _ly + 40
psvg("city", PHW, _h, pedges(PHW, _h, top=True, bottom=True)
     + f'<text x="12" y="21" font-size="10" class="m" letter-spacing="1.5">CONTRIBUTION CITY</text>'
     + f'<g transform="translate(1 24) scale({_k:.4f})">{_scene}</g>' + _t, city_alt)
psvg("footer", PHW, 52, pedges(PHW, 52, top=True, bottom=True) + f'<text x="12" y="30" font-size="10" class="m">$ open <tspan style="fill:{TEAL}">galtzo.com</tspan> · <tspan style="fill:{VIOLET}">sponsors/pboling</tspan></text>', "galtzo.com and sponsors link")

# ---- sponsor banner: full-time on FLOSS + call to action (wording drafted from the old README; see #14)
svg("banner/banner", 0, edges(0, 74, top=True) +
    f'<rect x="12" y="14" width="4" height="46" fill="{AMBER}"/>'
    f'<text x="28" y="34" class="s" font-size="20" font-weight="700">{esc(BANNER_TEXT[0])}</text>'
    f'<text x="28" y="56" font-size="12" class="m">{esc(BANNER_TEXT[1])}</text>', BANNER_TEXT[0] + " " + BANNER_TEXT[1], vb=(0, 0, W, 74))
for i, (k, sub, url, col) in enumerate(BANNER_LINKS):
    bw = W/4
    body = (edges(0, 56, i*bw, (i+1)*bw, bottom=True) +
            f'<rect x="{i*bw+(16 if i == 0 else 6):.0f}" y="4" width="{bw-(22 if i in (0, 3) else 12):.0f}" height="44" rx="6" fill="{PANEL}" stroke="{col}" stroke-opacity=".7"/>'
            f'<text x="{i*bw+(30 if i == 0 else 20):.0f}" y="24" font-size="10" letter-spacing="2" style="fill:{col}">{k}</text>'
            f'<text x="{i*bw+(30 if i == 0 else 20):.0f}" y="40" class="s" font-size="12" font-weight="600">{esc(sub)}</text>')
    svg(f"banner/link-{i+1}", 0, body, f"{k.title()}: {sub}", vb=(i*bw, 0, bw, 56))
HEAD_ROWS = [("header", "Peter Boling: team leader, web architect, security researcher, rubyist. Building for web since 2004."),
             ("stats", "Telemetry for projects I author and maintain: downloads, downloads per day, packages, stars."),
             ("city", "Contribution city: an isometric skyline, one building per day of the last year.")]
banner_rows = [img_html("banner/banner", BANNER_TEXT[0] + " " + BANNER_TEXT[1], 100, None),
               "".join(img_html(f"banner/link-{i+1}", f"{k.title()}: {sub}", 25 if True else 50, url) for i, (k, sub, url, col) in enumerate(BANNER_LINKS))]
_top = [img_html(n, a, 100, None) for n, a in HEAD_ROWS]
top = "\n".join([_top[0]] + banner_rows + _top[1:])
README_ROWS = ["".join(img_html(*it) for it in row) for row in README_ITEMS]
(ROOT/"README.md").write_text(f"""<!-- Generated by tools/profile/render.py (see tools/profile/). Edit that, not this file or the SVGs. -->
<p align="center">
{top}
{chr(10).join(README_ROWS)}
</p>

<p align="center">
Browse all 200+ projects at <a href="https://galtzo.com">galtzo.com</a> ·
<a href="https://github.com/sponsors/pboling">Sponsor</a> ·
<a href="https://discord.gg/3qme4XHNKN">Discord</a> ·
<a href="./docs/README.legacy.md">previous profile</a>
</p>

<p align="center"><sub>Updated automatically by my pet robot <a href="https://github.com/autobolt">@autobolt</a>. Data from <a href="https://github.com/galtzo-floss/galtzo.com">galtzo.com</a> project YAML. Console and city idea by <a href="https://github.com/georgekobaidze/georgekobaidze">Giorgi Kobaidze</a> (MIT). Inspired by <a href="https://github.com/jdx/jdx">Jeff Dickey's profile</a> (trending strip, day/night sky, plane, legend); ideas only, no code taken. Palette from sm-urb-design.</sub></p>
""")
# ---- cards.json: the collapsed, ordered cards (roll-ups included) for peterboling.com to render as HTML.
# Same selection as the profile's top list without the cap: mine, maintained, not adoptable, not archived.
def site_card(p):
    cov = p.get("coverage")
    return {
        "name": p["name"], "description": " ".join((p.get("description") or "").split()), "role": p.get("role"),
        "ecosystem": p.get("ecosystem"), "language": p.get("language"), "languages": p.get("_lang_list") or [p.get("language")],
        "minimum_version": str(p["minimum_version"]) if p.get("minimum_version") else None,
        "owner": bool(p.get("owner")), "releaser": bool(p.get("releaser")),
        "stars": p.get("github_stars") or 0, "downloads": p.get("total_downloads") or 0, "daily": p.get("daily_downloads") or 0,
        "coverage": round(cov, 1) if cov is not None else None,
        "new": bool(is_new(p)), "install": install_cmd(p, 80), "logo": owner_of(p) if logo_uri(owner_of(p) or "") else None,
        "url": gh_url(p), "docs": p.get("docs_site"), "family": p.get("family_id"),
        "rollup": bool(p.get("_rollup")), "members": p.get("_members"), "pkgs": p.get("_pkgs", 1) if p.get("_rollup") else None,
        "tags": sorted(set((p.get("_tags") or filter_tags(p)) + [t for t, on in (("owner", p.get("owner")), ("releaser", p.get("releaser"))) if on])),
        "spark": spark(p),
    }
(ROOT/"data"/"cards.json").write_text(json.dumps({"cards": [site_card(p) for p in ranked]}, indent=1, ensure_ascii=False) + "\n")
print("ok", tot_dl, day_dl, stars, n_proj)
