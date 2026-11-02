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
tot_dl = sum(p.get("total_downloads") or 0 for p in projects)
day_dl = sum(p.get("daily_downloads") or 0 for p in projects)
stars = sum(p.get("github_stars") or 0 for p in projects)
n_proj = len(projects)
by_eco = {}
for p in projects: by_eco[p["ecosystem"]] = by_eco.get(p["ecosystem"], 0) + 1
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
tiles = [("DOWNLOADS", human(tot_dl), "lifetime, all registries", TEAL),
         ("PER DAY", human(day_dl), "across every package", VIOLET),
         ("PROJECTS", str(n_proj), " · ".join(f"{v} {k}" for k, v in sorted(by_eco.items(), key=lambda x: -x[1]) if k != "none"), AMBER),
         ("STARS", human(stars), "on GitHub", TEAL)]
b = chrome("telemetry", 130); tw = (W-32-3*12)/4
for i, (k, v, sub, col) in enumerate(tiles):
    x = 16 + i*(tw+12)
    b += (f'<rect x="{x}" y="46" width="{tw}" height="72" rx="4" fill="{PANEL}" stroke="{EDGE}"/>'
          f'<rect x="{x}" y="46" width="3" height="72" fill="{col}"/>'
          f'<text x="{x+16}" y="66" font-size="10" class="m" letter-spacing="2">{k}</text>'
          f'<text x="{x+16}" y="96" class="s" font-size="28" font-weight="700" style="fill:{col}">{v}</text>'
          f'<text x="{x+16}" y="111" font-size="9" class="m">{esc(sub[:34])}</text>')
svg("stats", 130, b, f"{human(tot_dl)} lifetime downloads, {human(day_dl)} per day, {n_proj} projects, {human(stars)} stars")

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
CARD_EXCLUDE = {"bundler", "rexml", "rails", "hashie"}  # shown on galtzo.com, not featured here
ranked = sorted((p for p in projects if p["name"] not in CARD_EXCLUDE), key=lambda p: -(p.get("total_downloads") or 0))
TOP = 12
CW, CHT = (W-32-12)/2, 128
def card(i, p):
    col, row = i % 2, i//2
    x, y = 16 + col*(CW+12), 46 + row*(CHT+12)
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
    g += f'<text x="{x+CW-14}" y="{y+CHT-14}" font-size="10" class="m" text-anchor="end">{esc(str(p.get("role","")))}</text>'
    url = next((f["url"] for f in p.get("forges", []) if f["type"] == "GitHub"), None)
    return f'<a href="{esc(url)}">{g}</a>' if url else g
rows = math.ceil(TOP/2); H = 46 + rows*(CHT+12) + 28
b = chrome("projects · by lifetime downloads", H) + "".join(card(i, p) for i, p in enumerate(ranked[:TOP]))
lx = 16
for r, c in ROLE.items():
    b += f'<rect x="{lx}" y="{H-24}" width="10" height="10" fill="{c}"/><text x="{lx+16}" y="{H-15}" font-size="10" class="m">{r}</text>'; lx += 100
b += f'<text x="{W-16}" y="{H-15}" font-size="10" class="m" text-anchor="end">data: galtzo.com · scraped {scraped}</text>'
svg("projects", H, b, f"Top {TOP} projects by lifetime downloads, as cards")

# ---- footer
b = f'<rect x="1" y="0" width="{W-2}" height="56" fill="none" stroke="{EDGE}"/>'
b += (f'<text x="24" y="34" font-size="13" class="m">$ open <tspan style="fill:{TEAL}">galtzo.com</tspan> · <tspan style="fill:{VIOLET}">github.com/sponsors/pboling</tspan>'
      f' · connection closed.</text>')
svg("footer", 56, b, "Footer: galtzo.com and sponsors link")
print("ok", tot_dl, day_dl, stars, n_proj)
