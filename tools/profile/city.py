"""Contribution city: isometric skyline, one building per day (the card motif and painter's algorithm are
Giorgi Kobaidze's, MIT). Heights and colors follow each day's *rank* among active days (as GitHub's graph
shades by quartile), so one huge day can't flatten the skyline and the legend means something.

Ours: neon rings on the ten busiest days, a subway train that rides the near-left edge from tunnel to
tunnel, a moon, a plane crossing behind the skyline, and seeded stars/windows (same data, same city)."""
import datetime, math, random

# quiet -> busy roof/left/right shades; the last is the top decile
RAMP = [("#1c3330", "#162a27", "#112220"), ("#2a6f66", "#215850", "#1a4640"), ("#3aa395", "#2c8075", "#23665d"),
        ("#4fc3b3", "#3a9d90", "#2e7f74"), ("#a58bf5", "#8369d6", "#6a52b5")]
CUTS = (.25, .5, .75, .9)            # rank thresholds between the five levels
# Rings, busiest first. No red/green pair; spread over hue and lightness so neighbours stay apart.
NEON = ["#ff2bd6", "#22d3ee", "#ffb000", "#a3e635", "#818cf8", "#fb923c", "#f472b6", "#facc15", "#60a5fa", "#e879f9"]
WARM, COOL = "#f6d68a", "#8fe9ff"


def build(cal, W, CH, pal, total):
    PANEL, EDGE, TEAL, AMBER, PAPER, MUTED = (pal[k] for k in ("PANEL", "EDGE", "TEAL", "AMBER", "PAPER", "MUTED"))
    tw, th, oy, HMAX = 24.0, 10.0, 150, 108
    start = datetime.date.fromisoformat(cal[0]["date"])
    cells = []
    for d in cal:
        dt = datetime.date.fromisoformat(d["date"])
        cells.append(((dt - start).days // 7, (dt.weekday() + 1) % 7, d["count"], d["date"]))
    cols = max(c for c, *_ in cells) + 1
    ox = W/2 - ((cols - 7)/2)*tw/2

    def P(c, r, z=0): return (ox + (c - r)*tw/2, oy + (c + r)*th/2 - z)
    def pts(*ps): return " ".join(f"{x:.1f},{y:.1f}" for x, y in ps)

    nz = sorted(c[2] for c in cells if c[2])
    def rank(n):
        if len(nz) < 2: return 1.0
        lo, hi = nz.index(n), len(nz) - 1 - nz[::-1].index(n)
        return (lo + hi)/2/(len(nz) - 1)
    top = sorted((c for c in cells if c[2]), key=lambda c: (-c[2], c[3]))[:10]
    ring_of = {c[3]: NEON[i] for i, c in enumerate(top)}

    rng = random.Random(7)
    out = ['<defs>'
           '<filter id="glow" x="-60%" y="-60%" width="220%" height="220%"><feGaussianBlur stdDeviation="2.4"/></filter>'
           '<radialGradient id="moonglow"><stop offset="0" stop-color="#e8eefc" stop-opacity=".28"/><stop offset="1" stop-color="#e8eefc" stop-opacity="0"/></radialGradient>'
           f'<clipPath id="track"><polygon points="{pts(P(0, 6.9, 40), P(cols, 6.9, 40), P(cols, 8.2, -6), P(0, 8.2, -6))}"/></clipPath>'
           f'<clipPath id="skyclip"><rect x="2" y="34" width="{W-4}" height="{CH-36}"/></clipPath>'
           '</defs>']
    T, TA = tw/2, th/2                                      # screen step per week along the track
    train_len = 5*2.4 + 4*0.2
    c_mid = cols/2 - train_len/2
    a, b = c_mid + train_len + .5, cols + .5 - c_mid        # travel before / after the base position
    out.append(
        '<style>'
        '.tw{animation:twk 4s ease-in-out infinite}.fk{animation:fk 2.6s steps(1) infinite}.rg{animation:rg 3s ease-in-out infinite}'
        '.pl{animation:fly 34s linear infinite}.bk{animation:bk 1.4s steps(1) infinite}'
        f'.tr{{animation:ride 30s linear infinite}}'
        '@keyframes twk{50%{opacity:.25}}@keyframes fk{50%{opacity:0}}@keyframes rg{50%{opacity:.55}}@keyframes bk{50%{opacity:0}}'
        f'@keyframes fly{{from{{transform:translate(0,0)}}to{{transform:translate({W+80},-26px)}}}}'
        f'@keyframes ride{{from{{transform:translate({-a*T:.1f}px,{-a*TA:.1f}px)}}to{{transform:translate({b*T:.1f}px,{b*TA:.1f}px)}}}}'
        '@media (prefers-reduced-motion:reduce){.tw,.fk,.rg,.pl,.bk,.tr{animation:none}}'
        '</style>')

    # --- sky: stars above the skyline, a moon with craters, a plane crossing behind the buildings
    def skyline_y(x): return oy + (x - ox)*th/tw - HMAX - 6          # top of the tallest possible building at x
    stars = ""
    for _ in range(140):
        x, y = rng.uniform(14, W - 14), rng.uniform(40, 330)
        r_, o_, tw_ = rng.choice([.5, .7, .9, 1.2]), rng.choice([.3, .45, .6, .8]), rng.random() < .18
        if y < skyline_y(x) - 4 and not (W - 150 < x < W - 40 and y < 130):
            stars += (f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r_}" fill="{PAPER}" opacity="{o_}"'
                      + (f' class="tw" style="animation-delay:{rng.random()*4:.1f}s"' if tw_ else "") + '/>')
    mx_, my_ = W - 95, 92
    out.append(stars +
               f'<circle cx="{mx_}" cy="{my_}" r="42" fill="url(#moonglow)"/><circle cx="{mx_}" cy="{my_}" r="15" fill="#e8eefc"/>'
               f'<circle cx="{mx_-5}" cy="{my_-3}" r="3.2" fill="#c3cce4"/><circle cx="{mx_+5}" cy="{my_+5}" r="2.2" fill="#c3cce4"/><circle cx="{mx_+3}" cy="{my_-7}" r="1.6" fill="#c3cce4"/>'
               f'<g clip-path="url(#skyclip)"><g class="pl"><g transform="translate(-60 74)">'
               f'<line x1="-46" y1="1" x2="0" y2="1" stroke="{PAPER}" stroke-opacity=".12" stroke-width="2"/>'
               f'<rect x="0" y="0" width="16" height="2.4" rx="1.2" fill="#9fb4af"/><polygon points="6,1 1,-4.5 3.5,-4.5 10,1" fill="#9fb4af"/>'
               f'<polygon points="6,2 1,6.5 3.5,6.5 10,2" fill="#9fb4af"/><polygon points="0,1 -3,-4 -1,-4 2,1" fill="#9fb4af"/>'
               f'<circle cx="16" cy="1.2" r="1.1" fill="{PAPER}"/><circle cx="-1" cy="-3.6" r="1.1" fill="{AMBER}" class="bk"/></g></g></g>')

    # --- buildings, back to front
    for c, r, n, date in sorted(cells, key=lambda t: (t[0] + t[1], t[1])):
        if n == 0:
            out.append(f'<polygon points="{pts(P(c, r), P(c+1, r), P(c+1, r+1), P(c, r+1))}" fill="#0f1b1b" stroke="#1a2b2a" stroke-width=".5"/>')
            continue
        rk = rank(n)
        h = 8 + (HMAX - 8)*rk**1.3
        lvl = sum(rk >= cut for cut in CUTS)
        roof, left, right = RAMP[lvl]
        a_, b_, c_, d_ = P(c, r, h), P(c+1, r, h), P(c+1, r+1, h), P(c, r+1, h)
        g0, g1, g2 = P(c, r+1), P(c+1, r+1), P(c+1, r)
        out.append(f'<polygon points="{pts(d_, c_, g1, g0)}" fill="{left}"/><polygon points="{pts(c_, b_, g2, g1)}" fill="{right}"/>'
                   f'<polygon points="{pts(a_, b_, c_, d_)}" fill="{roof}"/>')
        lit, dark, flick = [], [], []
        for (p0, p1), faceoff in (((g0, g1), 0), ((g1, g2), 1)):
            for row in range(int((h - 7)//8)):
                v0 = 5 + row*8
                for u0 in (.16, .58):
                    u = rng.random()
                    q = [(p0[0] + (p1[0] - p0[0])*uu, p0[1] + (p1[1] - p0[1])*uu - vv)
                         for uu, vv in ((u0, v0), (u0 + .25, v0), (u0 + .25, v0 + 3.6), (u0, v0 + 3.6))]
                    seg = "M" + "L".join(f"{x:.1f},{y:.1f}" for x, y in q) + "Z"
                    if u < .55: (flick if rng.random() < .04 else lit).append((seg, rng.random() < .12))
                    else: dark.append(seg)
        if dark: out.append(f'<path d="{"".join(dark)}" fill="#0c1717"/>')
        for group, cls in ((lit, ""), (flick, ' class="fk" style="animation-delay:%.1fs"' % (rng.random()*2.6))):
            for color, warm in ((WARM, False), (COOL, True)):
                segs = "".join(s for s, cool in group if cool == warm)
                if segs: out.append(f'<path d="{segs}" fill="{color if not warm else COOL}"{cls}/>')
        if date in ring_of:
            col = ring_of[date]
            z2 = h - 6
            band = pts(P(c, r+1, z2), P(c+1, r+1, z2), P(c+1, r, z2))
            roofpoly = pts(a_, b_, c_, d_)
            delay = (list(ring_of).index(date))*.3
            out.append(f'<g class="rg" style="animation-delay:{delay:.1f}s">'
                       f'<polygon points="{roofpoly}" fill="none" stroke="{col}" stroke-width="3" filter="url(#glow)" opacity=".9"/>'
                       f'<polyline points="{band}" fill="none" stroke="{col}" stroke-width="2.4" filter="url(#glow)" opacity=".7"/>'
                       f'<polygon points="{roofpoly}" fill="none" stroke="{col}" stroke-width="1.5"/>'
                       f'<polyline points="{band}" fill="none" stroke="{col}" stroke-width="1.1"/></g>')

    # --- subway along the long near-left edge: track bed, a train that rides tunnel to tunnel, tunnel mouths
    def box(c0, c1, r0, r1, z0, z1, top_f, left_f, right_f, extra=""):
        return (f'<polygon points="{pts(P(c0, r1, z1), P(c1, r1, z1), P(c1, r1, z0), P(c0, r1, z0))}" fill="{left_f}"/>'
                f'<polygon points="{pts(P(c1, r1, z1), P(c1, r0, z1), P(c1, r0, z0), P(c1, r1, z0))}" fill="{right_f}"/>'
                f'<polygon points="{pts(P(c0, r0, z1), P(c1, r0, z1), P(c1, r1, z1), P(c0, r1, z1))}" fill="{top_f}"/>' + extra)
    r0, r1 = 7.3, 7.65
    out.append(f'<polygon points="{pts(P(-.9, 7.12), P(cols+.9, 7.12), P(cols+.9, 7.85), P(-.9, 7.85))}" fill="#0a1112" stroke="#1d3330" stroke-width=".6"/>')
    for rr in (7.33, 7.62):
        out.append(f'<line x1="{P(0, rr)[0]:.1f}" y1="{P(0, rr)[1]:.1f}" x2="{P(cols, rr)[0]:.1f}" y2="{P(cols, rr)[1]:.1f}" stroke="#3b5a55" stroke-width=".8"/>')
    ties = "".join(f'M{P(k, 7.25)[0]:.1f},{P(k, 7.25)[1]:.1f}L{P(k, 7.7)[0]:.1f},{P(k, 7.7)[1]:.1f}' for k in range(0, cols + 1))
    out.append(f'<path d="{ties}" stroke="#18302d" stroke-width="1" fill="none"/>')
    car = []
    for i in range(5):
        c0 = c_mid + i*2.6
        c1 = c0 + 2.4
        wins = "".join(
            f'<polygon points="{pts(P(c0+.2+k*.37, r1, 7.4), P(c0+.2+k*.37+.26, r1, 7.4), P(c0+.2+k*.37+.26, r1, 3.8), P(c0+.2+k*.37, r1, 3.8))}" fill="{COOL}"/>'
            for k in range(6))
        stripe = f'<polygon points="{pts(P(c0, r1, 2.4), P(c1, r1, 2.4), P(c1, r1, 1.4), P(c0, r1, 1.4))}" fill="{NEON[1]}" opacity=".9"/>'
        car.append(box(c0, c1, r0, r1, .6, 9.4, "#35514d", "#26403c", "#1c302d", wins + stripe))
    car.append(f'<ellipse cx="{P(c_mid+train_len, 7.47, 5)[0]:.1f}" cy="{P(c_mid+train_len, 7.47, 5)[1]:.1f}" rx="2.2" ry="1.6" fill="#ffffff"/>'
               f'<ellipse cx="{P(c_mid+train_len, 7.47, 5)[0]:.1f}" cy="{P(c_mid+train_len, 7.47, 5)[1]:.1f}" rx="6" ry="4" fill="#ffffff" opacity=".35" filter="url(#glow)"/>')
    out.append(f'<g clip-path="url(#track)"><g class="tr">{"".join(car)}</g></g>')
    for cc0, cc1, portal in ((-1.2, -.05, True), (cols + .05, cols + 1.2, False)):
        hole = ""
        if portal:
            hole = (f'<polygon points="{pts(P(cc1, 7.42, 6.4), P(cc1, 7.0, 6.4), P(cc1, 7.0, .4), P(cc1, 7.42, .4))}" fill="#05090a" transform="translate(0 0)"/>')
        out.append(box(cc0, cc1, 6.95, 7.78, 0, 8.5, "#1a2a28", "#10201e", "#142523", hole))

    # --- text in the empty bottom-left, clear of the skyline, and the legend
    active = sum(1 for c in cells if c[2])
    best = max(cells, key=lambda c: c[2])
    ty = CH - 118
    out.append(f'<text x="16" y="{ty}" font-size="30" font-weight="700" class="s" style="fill:{TEAL}">{total:,}</text>'
               f'<text x="16" y="{ty+18}" font-size="11" class="m">contributions · last 12 months</text>'
               f'<text x="16" y="{ty+38}" font-size="11" class="m">{active} active days · busiest {best[3]}: {best[2]}</text>')
    lx = 16
    ly = CH - 52
    out.append(f'<text x="{lx}" y="{ly+9}" font-size="10" class="m">quiet</text>')
    for i, (roof, *_) in enumerate(RAMP):
        out.append(f'<rect x="{lx+36+i*16}" y="{ly}" width="11" height="11" fill="{roof}"/>')
    out.append(f'<text x="{lx+36+5*16+4}" y="{ly+9}" font-size="10" class="m">top 10% of days</text>')
    for i, col in enumerate(NEON[:4]):
        out.append(f'<polygon points="{lx+8+i*0:.0f},{ly+27} {lx+14},{ly+30} {lx+8},{ly+33} {lx+2},{ly+30}" fill="none" stroke="{col}" stroke-width="1.3" transform="translate({i*13} 0)"/>')
    out.append(f'<text x="{lx+60}" y="{ly+33}" font-size="10" class="m">neon ring: the 10 busiest days</text>'
               f'<text x="{lx}" y="{ly+50}" font-size="10" class="m">height ranks the day · one building per day</text>')
    alt = (f"Isometric night skyline, one building per day, with a subway train under the near edge. {total} contributions in the last year; "
           f"busiest day {best[3]} with {best[2]}. The ten busiest days wear neon rings: " + ", ".join(f"{c[3]} ({c[2]})" for c in top) + ".")
    return "".join(out), alt
