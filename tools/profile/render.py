#!/usr/bin/env python3
"""Render profile SVGs from data/*.yml + data/contributions.json -> assets/profile/*.svg.
Theme: galtzo.com card motif + sm-urb-design (StructuredMerge) palette. Deterministic."""
import json, math, pathlib, random, datetime, textwrap
from xml.sax.saxutils import escape as esc
import yaml

ROOT = pathlib.Path(__file__).resolve().parents[2]
OUT = ROOT / "assets" / "profile"; OUT.mkdir(parents=True, exist_ok=True)
projects = yaml.safe_load((ROOT/"data/projects.yml").read_text())
person = yaml.safe_load((ROOT/"data/person.yml").read_text())
cal = json.loads((ROOT/"data/contributions.json").read_text())["days"]

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

def svg(name, h, body, title):
    css = f"""text{{font-family:{MONO};fill:{PAPER}}} .s{{font-family:{SANS}}} .m{{fill:{MUTED}}}
    @keyframes bl{{50%{{opacity:0}}}} .cur{{animation:bl 1.1s steps(1) infinite}}
    @keyframes fl{{0%,100%{{opacity:1}}50%{{opacity:.35}}}} .w{{animation:fl 3s ease-in-out infinite}}
    @media (prefers-reduced-motion:reduce){{.cur,.w{{animation:none}}}}"""
    (OUT/f"{name}.svg").write_text(
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{h}" viewBox="0 0 {W} {h}" role="img" aria-label="{esc(title)}">'
        f'<title>{esc(title)}</title><style>{css}</style><rect width="{W}" height="{h}" fill="{BG}"/>{body}</svg>')

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
def mini_card(i, p, y0, cols=3):
    cw, ch = (W-32-(cols-1)*12)/cols, 84
    col, row = i % cols, i//cols
    x, y = 16 + col*(cw+12), y0 + row*(ch+10)
    lc = LANG.get(p.get("language"), MUTED)
    n = p.get("_pkgs", 1)
    g = (f'<rect x="{x}" y="{y}" width="{cw}" height="{ch}" rx="4" fill="{PANEL}" stroke="{EDGE}"/>'
         f'<rect x="{x}" y="{y}" width="4" height="{ch}" fill="{ROLE["contributor"]}"/>'
         f'<circle cx="{x+18}" cy="{y+20}" r="4" fill="{lc}"/>'
         f'<text x="{x+28}" y="{y+25}" class="s" font-size="14" font-weight="700">{esc(p["name"][:(17 if n > 1 else 24)])}{"…" if n > 1 and len(p["name"]) > 17 else ""}</text>')
    if n > 1:
        g += f'<text x="{x+cw-12}" y="{y+24}" font-size="9" class="m" text-anchor="end">{n} pkgs · {p["_regs"]} regs</text>'
    for k, line in enumerate(wrap(p.get("description"), 40, 1)):
        g += f'<text x="{x+18}" y="{y+44}" class="s m" font-size="10.5">{esc(line)}</text>'
    st = [("★", human(p.get("github_stars") or 0), AMBER), ("↓", human(p.get("total_downloads") or 0), TEAL), ("↓/d", human(p.get("daily_downloads") or 0), VIOLET)]
    sx = x+18
    for sym, val, c in st:
        g += f'<text x="{sx}" y="{y+ch-12}" font-size="11" style="fill:{c}">{sym} {val}</text>'; sx += 80
    url = next((f["url"] for f in p.get("forges", []) if f["type"] == "GitHub"), None)
    return f'<a href="{esc(url)}">{g}</a>' if url else g
def card(i, p, y0=46):
    col, row = i % 2, i//2
    x, y = 16 + col*(CW+12), y0 + row*(CHT+12)
    rc = ROLE.get(p.get("role"), MUTED); lc = LANG.get(p.get("language"), MUTED)
    g = (f'<rect x="{x}" y="{y}" width="{CW}" height="{CHT}" rx="4" fill="{PANEL}" stroke="{EDGE}"/>'
         f'<rect x="{x}" y="{y}" width="4" height="{CHT}" fill="{rc}"/>'
         f'<text x="{x+18}" y="{y+26}" class="s" font-size="16" font-weight="700">{esc(p["name"][:30])}</text>'
         f'<circle cx="{x+CW-86}" cy="{y+22}" r="4" fill="{lc}"/>'
         f'<text x="{x+CW-76}" y="{y+26}" font-size="11" class="m">{esc(str(p.get("language") or "")[:10])}</text>')
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
    return f'<a href="{esc(url)}">{g}</a>' if url else g
rows = math.ceil(TOP/2); H = 46 + rows*(CHT+12) + 28
b = chrome("projects I author & maintain · by lifetime downloads", H) + "".join(card(i, p) for i, p in enumerate(ranked[:TOP]))
lx = 16
for r, c in ((k, v) for k, v in ROLE.items() if k != "contributor"):
    b += f'<rect x="{lx}" y="{H-24}" width="10" height="10" fill="{c}"/><text x="{lx+16}" y="{H-15}" font-size="10" class="m">{r}</text>'; lx += 100
b += f'<text x="{W-16}" y="{H-15}" font-size="10" class="m" text-anchor="end">data: galtzo.com · scraped {scraped}</text>'
svg("projects", H, b, f"Top {TOP} projects I author or maintain, by lifetime downloads, as cards")

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
HC = 46 + 84 + 18 + math.ceil(len(cranked)/3)*94 + 34
b = chrome("contributions to other people's projects · not my projects", HC)
b += f'<rect x="1" y="0" width="{W-2}" height="{HC}" fill="none" stroke="{ROLE["contributor"]}" stroke-opacity=".5"/>'
b += f'<text x="{W-16}" y="22" font-size="11" text-anchor="end" style="fill:{ROLE["contributor"]}">ROLE: CONTRIBUTOR</text>'
ctiles = [("UPSTREAM DOWNLOADS", human(T_CON["dl"]), "registries + release assets", TEAL),
          ("UPSTREAM PER DAY", human(T_CON["day"]), "per day, whole projects", VIOLET),
          ("PACKAGES", str(T_CON["packages"]), f"{T_CON['repos']} repos", AMBER),
          ("UPSTREAM STARS", human(T_CON["stars"]), "on GitHub", TEAL)]
b += tile_row(ctiles, accent=ROLE["contributor"])
b += f'<text x="16" y="132" font-size="9" class="m">{esc(basis_note(T_CON))}</text>'
b += "".join(mini_card(i, p, 148) for i, p in enumerate(cranked))
b += f'<text x="16" y="{HC-14}" font-size="10" class="m">Counts belong to the upstream projects and are tallied only here, never in the totals above.</text>'
svg("contributors", HC, b, "Contributions to other people's projects, shown separately from the projects I author and maintain")

# ---- footer
b = f'<rect x="1" y="0" width="{W-2}" height="56" fill="none" stroke="{EDGE}"/>'
b += (f'<text x="24" y="34" font-size="13" class="m">$ open <tspan style="fill:{TEAL}">galtzo.com</tspan> · <tspan style="fill:{VIOLET}">github.com/sponsors/pboling</tspan>'
      f' · connection closed.</text>')
svg("footer", 56, b, "Footer: galtzo.com and sponsors link")
print("ok", tot_dl, day_dl, stars, n_proj)
