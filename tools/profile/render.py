#!/usr/bin/env python3
"""Render profile SVGs from data/*.yml + data/contributions.json -> assets/profile/*.svg.
Theme: galtzo.com card motif + sm-urb-design (StructuredMerge) palette. Deterministic."""
import json, math, pathlib, random, datetime, textwrap
from xml.sax.saxutils import escape as _esc
def esc(t): return _esc(str(t), {'"': "&quot;"})
import yaml

ROOT = pathlib.Path(__file__).resolve().parents[2]
OUT = ROOT / "assets" / "profile"; OUT.mkdir(parents=True, exist_ok=True)
import shutil
for _d in ("projects", "feed", "contributors", "phone"): shutil.rmtree(OUT/_d, ignore_errors=True)
for _f in ("projects.svg", "feed.svg", "contributors.svg"): (OUT/_f).unlink(missing_ok=True)
projects = yaml.safe_load((ROOT/"data/projects.yml").read_text())
person = yaml.safe_load((ROOT/"data/person.yml").read_text())
cal = json.loads((ROOT/"data/contributions.json").read_text())["days"]
def _load(n, default):
    f = ROOT/"data"/n
    return json.loads(f.read_text()) if f.exists() else default
posts, releases, first_release = _load("posts.json", []), _load("releases.json", []), _load("first_release.json", {})
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
def logo_defs(owners):
    return "<defs>" + "".join(f'<image id="lg-{esc(o)}" href="{logo_uri(o)}" width="64" height="64" preserveAspectRatio="xMidYMid slice"/>'
                              for o in sorted(set(owners)) if o and logo_uri(o)) + "</defs>"
def logo_at(owner, x, y, size):
    if not owner or not logo_uri(owner): return ""
    k = size/64
    return (f'<g transform="translate({x},{y}) scale({k:.4f})"><rect width="64" height="64" rx="12" fill="#fff"/>'
            f'<use href="#lg-{esc(owner)}"/></g><rect x="{x}" y="{y}" width="{size}" height="{size}" rx="{size*12/64:.1f}" fill="none" stroke="{EDGE}"/>')
def is_new(p):
    d = first_release.get(f"{p['ecosystem']}:{p['name']}")
    return bool(d) and (TODAY - datetime.date.fromisoformat(d)).days <= 365
def ago(d):
    n = (TODAY - datetime.date.fromisoformat(d)).days
    return "today" if n <= 0 else f"{n}d ago" if n < 60 else f"{n//30}mo ago"

# palette: sm-urb-design "sm" brand (teal primary, violet secondary, amber tertiary) on dark paper
BG, PANEL, EDGE = "#0e1718", "#14211f", "#25403c"
TEAL, VIOLET, AMBER, PAPER, MUTED = "#4fc3b3", "#a58bf5", "#e8b04a", "#f4efe4", "#8fa6a1"
ROLE = {"author": "#dc2626", "maintainer": "#16a34a", "contributor": "#8b5cf6"}
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

# ---- contribution city (isometric, painter's algorithm)
start = datetime.date.fromisoformat(cal[0]["date"])
cells = []
for d in cal:
    dt = datetime.date.fromisoformat(d["date"])
    idx = (dt - start).days
    cells.append((idx//7, (dt.weekday()+1) % 7, d["count"]))   # week col, weekday row (Sun=0)
cols = max(c for c, _, _ in cells)+1
tw_, th_ = 24.0, 9.5
mx = max(n for *_, n in cells) or 1
CH = 400
ox = W/2 - ((cols-7)/2)*tw_/2
oy = 105
def P(c, r, z=0): return (ox + (c-r)*tw_/2, oy + (c+r)*th_/2 - z)
rng = random.Random(7)
b = chrome(f"contribution city · {contrib_total:,} contributions · last 12 months", CH)
# stars in sky
for _ in range(40):
    b += f'<circle cx="{rng.randint(16,W-16)}" cy="{rng.randint(40,110)}" r="{rng.choice([.6,.9,1.2])}" fill="{PAPER}" opacity="{rng.choice([.3,.5,.7])}"/>'
ramp = [("#1c3330", "#162a27", "#112220"), ("#2a6f66", "#215850", "#1a4640"), ("#3aa395", "#2c8075", "#23665d"),
        ("#4fc3b3", "#3a9d90", "#2e7f74"), ("#a58bf5", "#8369d6", "#6a52b5")]
for c, r, n in sorted(cells, key=lambda t: (t[0]+t[1], t[1])):
    lvl = 0 if n == 0 else 1 if n < mx*.15 else 2 if n < mx*.4 else 3 if n < mx*.7 else 4
    hgt = 2 + (math.sqrt(n)/math.sqrt(mx))*105 if n else 1.5
    top, left, right = ramp[lvl]
    a, bb, cc, dd = P(c, r, hgt), P(c+1, r, hgt), P(c+1, r+1, hgt), P(c, r+1, hgt)
    g0, g1, g2 = P(c, r+1), P(c+1, r+1), P(c+1, r)
    pts = lambda *ps: " ".join(f"{x:.1f},{y:.1f}" for x, y in ps)
    b += (f'<polygon points="{pts(dd,cc,g1,g0)}" fill="{left}"/><polygon points="{pts(cc,bb,g2,g1)}" fill="{right}"/>'
          f'<polygon points="{pts(a,bb,cc,dd)}" fill="{top}"/>')
    if hgt > 22 and rng.random() < .8:
        wx, wy = P(c+.5, r+1, hgt*.5)
        b += f'<rect x="{wx-1.5:.1f}" y="{wy:.1f}" width="3" height="2.5" fill="{AMBER}" class="w" style="animation-delay:{rng.random()*3:.1f}s"/>'
busiest = max(cal, key=lambda d: d["count"])
b += f'<text x="{W-16}" y="{CH-12}" font-size="10" class="m" text-anchor="end">busiest day {busiest["date"]}: {busiest["count"]} · one building per day, height ∝ √contributions</text>'
svg("city", CH, b, f"Isometric night skyline, one building per day. {contrib_total} contributions in the last year; busiest day {busiest['date']} with {busiest['count']}.")

# ---- project cards (galtzo card motif)
def wrap(s, n, k):
    s = "".join(ch for ch in (s or "") if ord(ch) < 0x2000).strip()
    full = textwrap.wrap(" ".join(s.split()), n); lines = full[:k]
    if len(full) > k: lines[-1] = lines[-1][:n-1].rstrip(" ,.") + "…"
    return lines
ranked = sorted(owned, key=lambda p: -(p.get("total_downloads") or 0))
TOP = 12
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
         f'<circle cx="{x+cw-14}" cy="{y+20}" r="4" fill="{lc}"/>'
         f'<text x="{x+42}" y="{y+25}" class="s" font-size="14" font-weight="700">{esc(p["name"][:(14 if n > 1 else 22)])}{"…" if n > 1 and len(p["name"]) > 14 else ""}</text>')
    if n > 1:
        g += f'<text x="{x+cw-26}" y="{y+24}" font-size="9" class="m" text-anchor="end">{n} pkgs · {p["_regs"]} regs</text>'
    for k, line in enumerate(wrap(p.get("description"), 40, 1)):
        g += f'<text x="{x+18}" y="{y+44}" class="s m" font-size="10.5">{esc(line)}</text>'
    st = [("★", human(p.get("github_stars") or 0), AMBER), ("↓", human(p.get("total_downloads") or 0), TEAL), ("↓/d", human(p.get("daily_downloads") or 0), VIOLET)]
    sx = x+18
    for sym, val, c in st:
        g += f'<text x="{sx}" y="{y+ch-12}" font-size="11" style="fill:{c}">{sym} {val}</text>'; sx += 80
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
         f'<circle cx="{x+CW-86}" cy="{y+22}" r="4" fill="{lc}"/>'
         f'<text x="{x+CW-76}" y="{y+26}" font-size="11" class="m">{esc(str(p.get("language") or "")[:10])}</text>')
    if is_new(p) and p.get("role") != "contributor":
        nx = x + CW - 132
        g += (f'<rect x="{nx:.0f}" y="{y+12}" width="36" height="16" rx="8" fill="{AMBER}"/>'
              f'<text x="{nx+18:.0f}" y="{y+24}" font-size="9" font-weight="700" text-anchor="middle" style="fill:{BG}">NEW</text>')
    for k, line in enumerate(wrap(p.get("description"), 52, 3)):
        g += f'<text x="{x+18}" y="{y+48+k*15}" class="s m" font-size="11.5">{esc(line)}</text>'
    st = [("★", human(p.get("github_stars") or 0), AMBER), ("↓", human(p.get("total_downloads") or 0), TEAL),
          ("↓/d", human(p.get("daily_downloads") or 0), VIOLET)]
    sx = x+18
    for sym, val, c in st:
        g += f'<text x="{sx}" y="{y+CHT-14}" font-size="12" style="fill:{c}">{sym} {val}</text>'; sx += 86
    tag = f'{p["_pkgs"]} packages · {p["_regs"]} registries' if p.get("_pkgs", 1) > 1 else str(p.get("role", ""))
    g += f'<text x="{x+CW-14}" y="{y+CHT-14}" font-size="10" class="m" text-anchor="end">{esc(tag)}</text>'
    url = next((f["url"] for f in p.get("forges", []) if f["type"] == "GitHub"), None)
    return f'<a href="{esc(url)}">{g}</a>' if url and link else g
rows = math.ceil(TOP/2)
def gh_url(p): return next((f["url"] for f in p.get("forges", []) if f["type"] == "GitHub"), None)
def card_alt(p):
    return (f'{p["name"]}, {p.get("role")}: {" ".join((p.get("description") or "").split())[:120]} '
            f'{human(p.get("github_stars") or 0)} stars, {human(p.get("total_downloads") or 0)} downloads')
svg("projects/head", 40, head_bar("projects I author & maintain · by lifetime downloads", 40), "Projects I author and maintain, by lifetime downloads", vb=(0, 0, W, 40))
readme_row(("projects/head", "Projects I author and maintain, by lifetime downloads", 100, None))
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
foot = edges(yf, yf+34, bottom=True); lx = 16
for r_, c in ((k, v) for k, v in ROLE.items() if k != "contributor"):
    foot += f'<rect x="{lx}" y="{yf+12}" width="10" height="10" fill="{c}"/><text x="{lx+16}" y="{yf+21}" font-size="10" class="m">{r_}</text>'; lx += 100
foot += f'<text x="{W-16}" y="{yf+21}" font-size="10" class="m" text-anchor="end">data: galtzo.com · scraped {scraped}</text>'
svg("projects/foot", 0, foot, "Legend: author, maintainer", vb=(0, yf, W, 34))
readme_row(("projects/foot", "Legend: red is author, green is maintainer", 100, None))

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
by_repo = {}
for p in contrib: by_repo.setdefault(gh_repo(p) or p["name"], []).append(p)
cranked = sorted((group_card(v) for v in by_repo.values()), key=lambda p: -p["total_downloads"])
PURPLE = ROLE["contributor"]
ctiles = [("UPSTREAM DOWNLOADS", human(T_CON["dl"]), "registries + release assets", TEAL),
          ("UPSTREAM PER DAY", human(T_CON["day"]), "per day, whole projects", VIOLET),
          ("PACKAGES", str(T_CON["packages"]), f"{T_CON['repos']} repos", AMBER),
          ("UPSTREAM STARS", human(T_CON["stars"]), "on GitHub", TEAL)]
HCH = 148
hb = (head_bar("contributions to other people's projects · not my projects", HCH, color=PURPLE,
               right=f'<text x="{W-16}" y="22" font-size="11" text-anchor="end" style="fill:{PURPLE}">ROLE: CONTRIBUTOR</text>')
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
    f'<text x="16" y="{yf+20}" font-size="10" class="m">Counts belong to the upstream projects and are tallied only here, never in the totals above.</text>',
    "Contributor counts belong to upstream projects", vb=(0, yf, W, 34))
readme_row(("contributors/foot", "Contributor counts belong to upstream projects and are not in my totals", 100, None))

# ---- footer
b = f'<rect x="1" y="0" width="{W-2}" height="56" fill="none" stroke="{EDGE}"/>'
b += (f'<text x="24" y="34" font-size="13" class="m">$ open <tspan style="fill:{TEAL}">galtzo.com</tspan> · <tspan style="fill:{VIOLET}">github.com/sponsors/pboling</tspan>'
      f' · connection closed.</text>')
svg("footer", 56, b, "Footer: galtzo.com and sponsors link")
readme_row(("footer", "Connection closed. galtzo.com and github.com/sponsors/pboling", 100, None))
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
psvg("projects/head", PHW, 34, pbar("projects I author & maintain") , "Projects I author and maintain")
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
    for k, line in enumerate(wrap(pr.get("description"), 31, 3)):
        o += f'<text x="16" y="{50+k*12}" class="s m" font-size="9.5">{esc(line)}</text>'
    st = [("★", human(pr.get("github_stars") or 0), AMBER), ("↓", human(pr.get("total_downloads") or 0), TEAL), ("/d", human(pr.get("daily_downloads") or 0), VIOLET)]
    sx = 16
    for sym, val, c in st:
        o += f'<text x="{sx}" y="{h-14}" font-size="9.5" style="fill:{c}">{sym}{val}</text>'; sx += 56
    return o, w, h
for i, pr in enumerate(ranked[:TOP]):
    col = i % 2
    body, w, h = pcard(pr, col)
    psvg(f"projects/{i+1:02d}", w, h, logo_defs([owner_of(pr)]) + body, card_alt(pr))
fb = pedges(PHW, 30, bottom=True) + f'<rect x="12" y="10" width="8" height="8" fill="{ROLE["author"]}"/><text x="25" y="17" font-size="9" class="m">author</text>' \
     f'<rect x="80" y="10" width="8" height="8" fill="{ROLE["maintainer"]}"/><text x="93" y="17" font-size="9" class="m">maintainer</text>' \
     f'<text x="{PHW-12}" y="17" font-size="8" class="m" text-anchor="end">data: galtzo.com · {scraped}</text>'
psvg("projects/foot", PHW, 30, fb, "Legend: author, maintainer")

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

# contributors: head (2x2 tiles), mini cards (130 wide, three per row), foot
pct = [("UPSTREAM DL", human(T_CON["dl"]), "registries + assets", TEAL), ("UPSTREAM /DAY", human(T_CON["day"]), "whole projects", VIOLET),
       ("PACKAGES", str(T_CON["packages"]), f"{T_CON['repos']} repos", AMBER), ("UPSTREAM STARS", human(T_CON["stars"]), "on GitHub", TEAL)]
psvg("contributors/head", PHW, 180, pedges(PHW, 180, color=PURPLE, top=True) +
     f'<text x="12" y="21" font-size="10" class="m" letter-spacing="1.5">CONTRIBUTIONS · NOT MINE</text>'
     f'<text x="{PHW-12}" y="21" font-size="9" text-anchor="end" style="fill:{PURPLE}">CONTRIBUTOR</text>' + ptiles(pct, 40, accent=PURPLE) +
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
     f'<text x="12" y="18" font-size="8" class="m">Upstream counts; never in my totals above.</text>', "Contributor counts belong to upstream projects")
psvg("footer", PHW, 52, pedges(PHW, 52, top=True, bottom=True) + f'<text x="12" y="30" font-size="10" class="m">$ open <tspan style="fill:{TEAL}">galtzo.com</tspan> · <tspan style="fill:{VIOLET}">sponsors/pboling</tspan></text>', "galtzo.com and sponsors link")

HEAD_ROWS = [("header", "Peter Boling: team leader, web architect, security researcher, rubyist. Building for web since 2004."),
             ("stats", "Telemetry for projects I author and maintain: downloads, downloads per day, packages, stars."),
             ("city", "Contribution city: an isometric skyline, one building per day of the last year.")]
top = "\n".join(img_html(n, a, 100, None) for n, a in HEAD_ROWS)
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

<p align="center"><sub>Data from <a href="https://github.com/galtzo-floss/galtzo.com">galtzo.com</a> project YAML. Console and city idea by <a href="https://github.com/georgekobaidze/georgekobaidze">Giorgi Kobaidze</a> (MIT). Palette from sm-urb-design.</sub></p>
""")
print("ok", tot_dl, day_dl, stars, n_proj)
