"""
HappyRobot — 3 AI-Native Companies of the Week
LinkedIn Carousel v7 — 1080×1350 (4:5)
Single-column sections, gold accents, full rich content, source citations
"""

from PIL import Image, ImageDraw, ImageFont, ImageEnhance
import os, urllib.request, hashlib

# ── PATHS ────────────────────────────────────────────────────────────
BRAND = "/Users/charleslorin/Projects/weekly news/brand-assets/brand-assets"
PHOTO = "/Users/charleslorin/Projects/weekly news/charles_headshot.png"
OUT   = "/Users/charleslorin/Projects/weekly news/ai-native-carousel.pdf"
LOGO_DIR = "/Users/charleslorin/Projects/weekly news/logos"

# ── FONTS ────────────────────────────────────────────────────────────
_fc = {}
def f(name, size):
    k = (name, size)
    if k not in _fc:
        _fc[k] = ImageFont.truetype(
            f"{BRAND}/fonts/{'Tobias-Regular.otf' if name == 'tobias' else 'SuisseIntl-Regular.ttf'}",
            size)
    return _fc[k]

# ── COLORS ───────────────────────────────────────────────────────────
NAVY      = (17, 43, 66)
PARCHMENT = (224, 221, 205)
DEEP      = (14, 13, 12)
GOLD      = (212, 168, 67)
WHITE     = (255, 255, 255)

PAIN_C    = (160, 70, 30)
MOVE_C    = (17, 43, 66)
IMPACT_C  = (30, 110, 60)

W, H = 1080, 1350

# ── DATA ─────────────────────────────────────────────────────────────
WEEK = "MARCH 2026 · WEEK 4"
EDITION = 1
COS = [
    {
        "name": "Revolut",
        "subtitle": "Digital banking \u00b7 50M+ customers \u00b7 38 markets",
        "domain": "revolut.com",
        "hero_stat": "8\u00d7 faster",
        "hero_label": "time to ticket resolution with AI voice agents",
        "pain": "50 million customers generating 1.2 million support tickets per month across 31 languages. Human agents couldn\u2019t scale fast enough without costs spiraling \u2014 and wait times were frustrating premium users.",
        "move": "Deployed AI voice agents powered by ElevenLabs for 24/7 multilingual customer support. The system handles frontline queries conversationally across all markets simultaneously, escalating only complex cases to human specialists.",
        "impact": "Time to ticket resolution dropped 8\u00d7. Premium voice support now scales across 31 languages without adding headcount. 4 million customers served through the new AI channel in the first quarter.",
        "callouts": {
            "pain_stat": "1.2M", "pain_label": "tickets per month",
            "move_stat": "31", "move_label": "languages supported",
            "impact_stat": "8\u00d7", "impact_label": "faster resolution",
        },
        "source": "Source: ElevenLabs case study, Jan 2026; Revolut press materials",
    },
    {
        "name": "Zalando",
        "subtitle": "Fashion e-commerce \u00b7 50M+ active customers \u00b7 Europe",
        "domain": "zalando.com",
        "hero_stat": "50 AI robots",
        "hero_label": "deployed across European fulfilment centres",
        "pain": "Millions of individual items flowing through fulfilment centres daily. Manual picking and sorting couldn\u2019t keep pace with order volume \u2014 especially during seasonal peaks. Labor shortages across European warehouses made the problem worse.",
        "move": "Rolled out 50 AI-powered Nomagic robots across European fulfilment centres. Each robot, named Richard, handles item-level picking, sorting, and packing autonomously using computer vision and real-time decision-making.",
        "impact": "Fulfilment speed increased significantly across all equipped centres. Zalando announced a \u20ac300M share buyback backed by strong 2025 results. AI-driven logistics is now a core pillar of their 2026 acceleration strategy.",
        "callouts": {
            "pain_stat": "Millions", "pain_label": "items picked daily",
            "move_stat": "50", "move_label": "Nomagic AI robots",
            "impact_stat": "\u20ac300M", "impact_label": "share buyback announced",
        },
        "source": "Source: Zalando press release, Mar 2026; Globe Newswire",
    },
    {
        "name": "Emporix",
        "subtitle": "B2B commerce platform \u00b7 Zug, Switzerland",
        "domain": "emporix.com",
        "hero_stat": "87% faster",
        "hero_label": "B2B order processing time after AI deployment",
        "pain": "ACR\u2019s B2B customers sent purchase orders as PDFs via email. Every order was manually keyed into the ERP \u2014 8 minutes per order, constant errors, and customer service buried in data entry instead of serving customers.",
        "move": "Deployed an AI orchestration layer that autonomously reads unstructured PDF purchase orders, validates business logic against ERP rules, and triggers downstream actions \u2014 all without human intervention. Processing runs 24/7.",
        "impact": "Order processing time dropped from 8 minutes to under 60 seconds \u2014 an 87% reduction. Error rates collapsed. Customer service teams shifted from manual data entry to value-added customer conversations.",
        "callouts": {
            "pain_stat": "8 min", "pain_label": "per order manually",
            "move_stat": "24/7", "move_label": "autonomous processing",
            "impact_stat": "87%", "impact_label": "time reduction",
        },
        "source": "Source: Emporix/ACR press release, Mar 2026",
    },
]


# ── HELPERS ──────────────────────────────────────────────────────────
def blend(c, a, bg):
    return tuple(int(cv * a + bv * (1 - a)) for cv, bv in zip(c, bg))


def wrap(text, fnt, maxw):
    lines, cur = [], ""
    for w in text.split():
        t = f"{cur} {w}".strip()
        if fnt.getbbox(t)[2] - fnt.getbbox(t)[0] <= maxw:
            cur = t
        else:
            if cur: lines.append(cur)
            cur = w
    if cur: lines.append(cur)
    return lines


def draw_block(draw, text, x, y, fnt, color, maxw, lh):
    for line in wrap(text, fnt, maxw):
        draw.text((x, y), line, fill=color, font=fnt)
        y += lh
    return y


def measure_block(text, fnt, maxw, lh):
    return len(wrap(text, fnt, maxw)) * lh


def centered_text(draw, text, y, fnt, color):
    bb = fnt.getbbox(text)
    draw.text((W // 2 - (bb[2] - bb[0]) // 2, y), text, fill=color, font=fnt)


def circle_mask(sz):
    m = Image.new("L", (sz, sz), 0)
    ImageDraw.Draw(m).ellipse([0, 0, sz - 1, sz - 1], fill=255)
    return m


def draw_arrow(draw, x, y, sz, color, w=3):
    draw.line([(x, y), (x + sz, y)], fill=color, width=w)
    draw.line([(x + int(sz * .55), y - int(sz * .4)), (x + sz, y)], fill=color, width=w)
    draw.line([(x + int(sz * .55), y + int(sz * .4)), (x + sz, y)], fill=color, width=w)


def draw_logo(draw, x, y, h, color):
    s = h / 137.0
    pts_l = [(86*s+x, 85.75*s+y), (72.365*s+x, 62.62*s+y),
             (60.157*s+x, 55.87*s+y), (46.52*s+x, 32.74*s+y),
             (46.52*s+x, y), (x, y), (x, 18.53*s+y),
             (14.06*s+x, 41.88*s+y), (25.42*s+x, 47.91*s+y),
             (39.48*s+x, 71.26*s+y), (39.48*s+x, 137*s+y), (86*s+x, 137*s+y)]
    pts_r = [(173*s+x, 121.11*s+y), (159.13*s+x, 97.85*s+y),
             (146.43*s+x, 90.99*s+y), (132.56*s+x, 67.73*s+y),
             (132.56*s+x, y), (86*s+x, y), (86*s+x, 52.92*s+y),
             (99.87*s+x, 76.18*s+y), (112.57*s+x, 83.04*s+y),
             (126.44*s+x, 106.30*s+y), (126.44*s+x, 137*s+y), (173*s+x, 137*s+y)]
    draw.polygon(pts_l, fill=color)
    draw.polygon(pts_r, fill=color)
    return int(173 * s)


def logo_bar(draw, x, y, h, color, show_week=True):
    lw = draw_logo(draw, x, y, h, color)
    draw.text((x + lw + 14, y + int(h * .18)), "HappyRobot",
              fill=color, font=f("suisse", int(h * .65)))
    if show_week:
        wc = blend(color, 0.35, NAVY)
        fnt2 = f("suisse", 13)
        tw = fnt2.getbbox(WEEK)[2] - fnt2.getbbox(WEEK)[0]
        draw.text((W - 64 - tw, y + int(h * .25)), WEEK, fill=wc, font=fnt2)


def fetch_logo(domain, sz=52):
    """Fetch real company logo. Tries Clearbit first, then Google favicon.
    Ensures logo is visible on parchment background."""
    if not domain:
        return None
    os.makedirs(LOGO_DIR, exist_ok=True)
    cache = os.path.join(LOGO_DIR, f"{domain.replace('.', '_')}.png")

    if not os.path.exists(cache):
        # Try sources in order of quality
        urls = [
            f"https://logo.clearbit.com/{domain}?size=128",
            f"https://img.logo.dev/{domain}?token=pk_anonymous&size=128",
            f"https://www.google.com/s2/favicons?domain={domain}&sz=128",
        ]
        fetched = False
        for url in urls:
            try:
                req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
                with urllib.request.urlopen(req, timeout=5) as resp:
                    data = resp.read()
                    if len(data) > 500:  # skip tiny placeholder responses
                        with open(cache, "wb") as fout:
                            fout.write(data)
                        fetched = True
                        break
            except:
                continue
        if not fetched:
            print(f"  \u26a0 Logo fetch failed ({domain})")
            return None

    try:
        img = Image.open(cache).convert("RGBA")
        img.thumbnail((sz, sz), Image.LANCZOS)

        # Ensure minimum usable size
        if img.width < 24 or img.height < 24:
            print(f"  \u26a0 Logo too small for {domain}")
            return None

        # Check contrast against parchment — darken if too close
        pixels = list(img.getdata())
        visible = [p for p in pixels if len(p) == 4 and p[3] > 128]
        if visible:
            avg_b = sum((r*.299 + g*.587 + b*.114) for r, g, b, a in visible) / len(visible)
            parch_b = 224*.299 + 221*.587 + 205*.114
            if abs(avg_b - parch_b) < 35:
                img_rgb = ImageEnhance.Brightness(img.convert("RGB")).enhance(0.45)
                r2, g2, b2 = img_rgb.split()
                img = Image.merge("RGBA", (r2, g2, b2, img.split()[3]))

        return img
    except:
        return None


def draw_fallback_logo(draw, x, y, sz, name, bg):
    draw.rounded_rectangle([x, y, x + sz, y + sz], radius=10,
                           fill=blend(GOLD, 0.12, bg), outline=blend(GOLD, 0.25, bg), width=2)
    fnt = f("suisse", int(sz * .5))
    ch = name[0].upper()
    bb = fnt.getbbox(ch)
    draw.text((x + sz // 2 - (bb[2] - bb[0]) // 2, y + sz // 2 - (bb[3] - bb[1]) // 2 - 3),
              ch, fill=NAVY, font=fnt)


def dark_bg():
    img = Image.new("RGB", (W, H), NAVY)
    p = f"{BRAND}/images/Blurred image background.png"
    if os.path.exists(p):
        bg = Image.open(p).convert("RGB").resize((W, H), Image.LANCZOS)
        bg = ImageEnhance.Brightness(bg).enhance(0.3)
        img = Image.blend(img, bg, 0.5)
    return img


def sketch_overlay(img, yoff=0):
    p = f"{BRAND}/images/datalayer_sketch.png"
    if not os.path.exists(p): return
    sk = Image.open(p).convert("RGBA")
    r = W / sk.width
    sk = sk.resize((W, int(sk.height * r)), Image.LANCZOS)
    a = sk.split()[3].point(lambda v: int(v * 0.03))  # 3% opacity
    sk.putalpha(a)
    img.paste(sk, (0, yoff), sk)


def headshot_circle(img, hx, hy, hsz):
    hs = Image.open(PHOTO).convert("RGBA").resize((hsz, hsz), Image.LANCZOS)
    m = circle_mask(hsz)
    circ = Image.new("RGBA", (hsz, hsz), (0, 0, 0, 0))
    circ.paste(hs, (0, 0), m)
    ring = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    rd = ImageDraw.Draw(ring)
    cx, cy, r = hx + hsz // 2, hy + hsz // 2, hsz // 2
    rd.ellipse([cx-r-4, cy-r-4, cx+r+4, cy+r+4], outline=GOLD+(200,), width=4)
    rd.ellipse([cx-r-12, cy-r-12, cx+r+12, cy+r+12], outline=GOLD+(40,), width=6)
    img.paste(ring, (0, 0), ring)
    img.paste(circ, (hx, hy), circ)


# ── FONT SIZE CALC ───────────────────────────────────────────────────
def calc_body_font(companies, textw, section_heights):
    """Find largest font size (start 28, min 18) that fits all content."""
    for sz in range(28, 17, -1):
        fnt = f("suisse", sz)
        lh = int(sz * 1.58)
        ok = True
        for co in companies:
            for field, maxh in zip(["pain", "move", "impact"], section_heights):
                needed = measure_block(co[field], fnt, textw, lh)
                if needed > maxh - 50:  # 50px for label + padding
                    ok = False; break
            if not ok: break
        if ok: return sz, lh
    return 18, 30


# ════════════════════════════════════════════════════════════════════
#  SLIDE 1 — COVER
# ════════════════════════════════════════════════════════════════════
def slide_cover():
    img = dark_bg()
    sketch_overlay(img, yoff=-60)
    d = ImageDraw.Draw(img)

    logo_bar(d, 60, 56, 28, WHITE)
    cx = 80

    # Content block centered against headshot
    badge_y = 340
    bsz = 62
    d.rounded_rectangle([cx, badge_y, cx+bsz, badge_y+bsz], radius=14, fill=GOLD)
    fb = f("suisse", 32)
    bw = fb.getbbox("3")[2] - fb.getbbox("3")[0]
    d.text((cx + bsz//2 - bw//2, badge_y + 12), "3", fill=NAVY, font=fb)

    ty = badge_y + bsz + 28
    ft = f("tobias", 88)
    d.text((cx, ty), "AI-Native", fill=WHITE, font=ft)
    d.text((cx, ty+100), "Companies", fill=WHITE, font=ft)
    d.text((cx, ty+200), "of the Week", fill=GOLD, font=ft)

    dy = ty + 305
    d.rectangle([cx, dy, cx+100, dy+3], fill=GOLD)

    sy = dy + 24
    fs = f("suisse", 24)
    sc = blend(WHITE, 0.6, NAVY)
    d.text((cx, sy), "Real companies. Real transformations.", fill=sc, font=fs)
    d.text((cx, sy+36), "Every week.", fill=sc, font=fs)

    # Swipe
    swy = H - 68
    d.text((cx, swy), "SWIPE", fill=blend(WHITE, 0.50, NAVY), font=f("suisse", 16))
    draw_arrow(d, cx+78, swy+9, 28, GOLD, 3)

    # Headshot — 450px
    headshot_circle(img, W-450+30, H-450+30, 450)
    return img


# ════════════════════════════════════════════════════════════════════
#  SLIDES 2–4 — COMPANY CARDS (single-column, accent bars)
# ════════════════════════════════════════════════════════════════════
def slide_company(co, idx, total, bsz, blh):
    img = Image.new("RGB", (W, H), PARCHMENT)
    d = ImageDraw.Draw(img)

    ML = 72
    MR = 64
    CALLOUT_W = 200  # left column for stat callouts

    # Header
    logo_bar(d, 64, 44, 24, DEEP, show_week=False)
    ctr = f"{str(idx+1).zfill(2)} / {str(total).zfill(2)}"
    fc = f("suisse", 16)
    bb = fc.getbbox(ctr)
    d.text((W-MR-(bb[2]-bb[0]), 50), ctr, fill=blend(DEEP, 0.3, PARCHMENT), font=fc)

    # Company logo + name
    name_y = 105
    logo_sz = 52
    logo_img = fetch_logo(co.get("domain", ""), logo_sz)
    if logo_img:
        img.paste(logo_img, (ML, name_y + 8), logo_img)
        name_x = ML + logo_sz + 16
    else:
        draw_fallback_logo(d, ML, name_y + 8, logo_sz, co["name"], PARCHMENT)
        name_x = ML + logo_sz + 16

    fn = f("tobias", 64)
    d.text((name_x, name_y), co["name"], fill=DEEP, font=fn)
    nb = fn.getbbox(co["name"])
    nh = nb[3] - nb[1]

    # Gold underline — generous space below name/logo
    uly = name_y + nh + 28
    d.rectangle([ML, uly, ML+80, uly+3], fill=GOLD)

    # Subtitle
    sub = co.get("subtitle", "")
    if sub:
        d.text((ML, uly+16), sub, fill=(107, 107, 107), font=f("suisse", 14))

    # Hero stat bar + gold bottom border — space after subtitle
    hy = uly + 48
    hh = 115
    d.rectangle([0, hy, W, hy+hh], fill=NAVY)
    d.rectangle([0, hy+hh, W, hy+hh+1], fill=blend(GOLD, 0.20, PARCHMENT))

    fhs = f("tobias", 64)
    st = co.get("hero_stat", "")
    sw = fhs.getbbox(st)[2] - fhs.getbbox(st)[0]
    d.text((W//2 - sw//2, hy+10), st, fill=GOLD, font=fhs)

    fhl = f("suisse", 15)
    hl = co.get("hero_label", "")
    hw = fhl.getbbox(hl)[2] - fhl.getbbox(hl)[0]
    d.text((W//2 - hw//2, hy+80), hl, fill=blend(WHITE, 0.55, NAVY), font=fhl)

    # ── SECTIONS: variable height, two-column with callouts ──
    sections_top = hy + hh + 14
    source_reserve = 52
    sections_avail = H - sections_top - source_reserve

    callouts = co.get("callouts", {})
    sections = [
        ("THE PAIN", co["pain"], PAIN_C,
         callouts.get("pain_stat", ""), callouts.get("pain_label", "")),
        ("THE MOVE", co["move"], MOVE_C,
         callouts.get("move_stat", ""), callouts.get("move_label", "")),
        ("THE IMPACT", co["impact"], IMPACT_C,
         callouts.get("impact_stat", ""), callouts.get("impact_label", "")),
    ]

    body_x = ML + CALLOUT_W + 8
    body_w = W - body_x - MR
    fnt_label = f("suisse", 14)
    fnt_body = f("suisse", bsz)
    fnt_callout_num = f("tobias", 44)
    fnt_callout_lbl = f("suisse", 12)
    body_c = blend(DEEP, 0.90, PARCHMENT)

    # Fixed equal section heights — identical format across all slides
    label_h = 36
    pad = 24
    section_h = sections_avail // 3
    section_heights = [section_h, section_h, section_h]

    cy = sections_top
    for i, (label, txt, accent_c, cstat, clbl) in enumerate(sections):
        sh = section_heights[i]
        card_bg = blend(accent_c, 0.035, PARCHMENT)

        # Section background tint
        d.rectangle([0, cy, W, cy + sh], fill=card_bg)

        # Left accent bar (5px)
        d.rectangle([0, cy, 5, cy + sh], fill=accent_c)

        # Gold separator between sections
        if i > 0:
            d.rectangle([ML, cy, W - MR, cy + 1], fill=blend(GOLD, 0.15, card_bg))

        # Label with pill background
        ly = cy + pad
        lbb = fnt_label.getbbox(label)
        lw = lbb[2] - lbb[0]
        lh_px = lbb[3] - lbb[1]
        pill_pad_x, pill_pad_y = 10, 5
        d.rounded_rectangle(
            [ML + 14, ly - pill_pad_y, ML + 14 + lw + 2*pill_pad_x, ly + lh_px + pill_pad_y],
            radius=6, fill=blend(accent_c, 0.10, card_bg))
        d.text((ML + 14 + pill_pad_x, ly), label, fill=accent_c, font=fnt_label)
        # Gold dot after label
        dot_x = ML + 14 + lw + 2*pill_pad_x + 8
        d.ellipse([dot_x, ly + 3, dot_x + 7, ly + 10], fill=GOLD)

        content_y = ly + label_h

        # LEFT COLUMN: callout stat — number and label MUST NOT touch
        if cstat:
            body_h = measure_block(txt, fnt_body, body_w, blh)
            callout_num_bb = fnt_callout_num.getbbox(cstat)
            callout_num_h = callout_num_bb[3] - callout_num_bb[1]
            NUM_LABEL_GAP = 14  # minimum 14px gap between number and label
            callout_lbl_bb = fnt_callout_lbl.getbbox(clbl)
            callout_lbl_h = callout_lbl_bb[3] - callout_lbl_bb[1]
            callout_total_h = callout_num_h + NUM_LABEL_GAP + callout_lbl_h
            callout_y = content_y + max(0, (body_h - callout_total_h) // 2)

            d.text((ML + 14, callout_y), cstat, fill=GOLD, font=fnt_callout_num)
            d.text((ML + 14, callout_y + callout_num_h + NUM_LABEL_GAP), clbl,
                   fill=blend(DEEP, 0.45, card_bg), font=fnt_callout_lbl)

        # RIGHT COLUMN: body text
        draw_block(d, txt, body_x, content_y, fnt_body, body_c, body_w, blh)

        cy += sh

    # Source citation
    src = co.get("source", "")
    if src:
        src_y = H - 40
        d.rectangle([ML, src_y - 8, W - MR, src_y - 7], fill=blend(GOLD, 0.15, PARCHMENT))
        d.text((ML, src_y), src, fill=blend(DEEP, 0.55, PARCHMENT), font=f("suisse", 12))

    return img


# ════════════════════════════════════════════════════════════════════
#  SLIDE 5 — CLOSING CTA
# ════════════════════════════════════════════════════════════════════
def slide_closing():
    img = dark_bg()
    sketch_overlay(img, yoff=H-800)
    d = ImageDraw.Draw(img)

    logo_bar(d, 60, 56, 28, WHITE, show_week=False)

    # Vertically center: content block ~500px, center of gravity at ~45%
    block_top = 280

    # Quote marks — gold 12%
    fq = f("tobias", 200)
    qc = blend(GOLD, 0.12, NAVY)
    qbb = fq.getbbox("\u201C")
    d.text((W//2 - (qbb[2]-qbb[0])//2, block_top), "\u201C", fill=qc, font=fq)

    # Headline
    fh = f("tobias", 50)
    hy = block_top + 190
    for i, ln in enumerate(["Every week, I break down", "how real companies become"]):
        centered_text(d, ln, hy + i*66, fh, WHITE)
    centered_text(d, "AI-native.", hy + 132, fh, GOLD)

    # Gold divider
    dy = hy + 132 + 72
    d.rectangle([W//2-44, dy, W//2+44, dy+2], fill=GOLD)

    # CTA pill — GOLD toned, not green
    cta = "Follow for weekly AI insights \u2192"
    fc = f("suisse", 22)
    ctbb = fc.getbbox(cta)
    ctw = ctbb[2] - ctbb[0]
    pw, ph = ctw + 90, 64
    px, py = W//2 - pw//2, dy + 38
    pill_bg = blend(GOLD, 0.15, NAVY)
    pill_border = blend(GOLD, 0.30, NAVY)
    d.rounded_rectangle([px, py, px+pw, py+ph], radius=14,
                        fill=pill_bg, outline=pill_border, width=2)
    d.text((px + 36, py + 17), cta, fill=WHITE, font=fc)

    # Author row
    ay = py + ph + 44
    hs = Image.open(PHOTO).convert("RGBA").resize((56, 56), Image.LANCZOS)
    m = circle_mask(56)
    ac = Image.new("RGBA", (56, 56), (0, 0, 0, 0))
    ac.paste(hs, (0, 0), m)
    ax = W//2 - 130
    ring = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(ring).ellipse([ax-3, ay-3, ax+59, ay+59], outline=GOLD+(180,), width=2)
    img.paste(ring, (0, 0), ring)
    img.paste(ac, (ax, ay), ac)

    d.text((ax+70, ay+6), "Charles Lorin", fill=WHITE, font=f("suisse", 20))
    d.text((ax+70, ay+32), "Digital Natives @HappyRobot",
           fill=blend(WHITE, 0.45, NAVY), font=f("suisse", 15))

    # Contact
    fnt_url = f("suisse", 14)
    url_c = blend(WHITE, 0.30, NAVY)
    centered_text(d, "charles.lorin@happyrobot.ai", H-80, fnt_url, url_c)
    centered_text(d, "happyrobot.ai", H-56, fnt_url, blend(WHITE, 0.20, NAVY))

    return img


# ════════════════════════════════════════════════════════════════════
#  BUILD
# ════════════════════════════════════════════════════════════════════
def main():
    ML, MR = 72, 64
    CALLOUT_W = 200
    textw = W - (ML + CALLOUT_W + 8) - MR  # right column width

    # Section heights for overflow calc (variable, but estimate)
    total_avail = 750
    sheights = [int(total_avail * p) for p in [0.25, 0.40, 0.35]]
    bsz, blh = calc_body_font(COS, textw, sheights)
    print(f"  Body: {bsz}px / {blh}px lh")

    slides = [slide_cover()]
    for i, co in enumerate(COS):
        slides.append(slide_company(co, i, len(COS), bsz, blh))
    slides.append(slide_closing())

    # Verify all slides are exactly 1080x1350 (LinkedIn 4:5 carousel)
    for i, s in enumerate(slides):
        assert s.size == (W, H), f"Slide {i+1} is {s.size}, expected ({W}, {H})"

    # PDF export — 72 DPI, all pages same size
    slides[0].save(OUT, "PDF", save_all=True, append_images=slides[1:], resolution=72)
    print(f"\u2713 {OUT}")
    for i, s in enumerate(slides):
        png = OUT.replace(".pdf", f"_slide{i+1}.png")
        s.save(png)
        print(f"  \u2192 slide {i+1} ({s.size[0]}\u00d7{s.size[1]})")

if __name__ == "__main__":
    main()
