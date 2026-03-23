# AI-Native Companies of the Week — LinkedIn Carousel

You are producing a weekly LinkedIn carousel for Charles Lorin, CEO of HappyRobot. HappyRobot builds AI voice agents for enterprises (customers include DHL, Uber Freight, TaskRabbit). Charles is building a personal brand as the go-to voice on companies going AI-native.

The carousel is a recurring weekly format: "3 AI-Native Companies of the Week." It features 3 real companies that made concrete AI-native moves, with a clear Pain → Move → Impact structure for each.

---

## PHASE 1 — RESEARCH WITH EXA AI

Use the Exa AI API to find 3 companies. Your Exa API key should be set as an environment variable `EXA_API_KEY`.

```python
import os, requests

EXA_KEY = os.environ.get("EXA_API_KEY")
headers = {"x-api-key": EXA_KEY, "Content-Type": "application/json"}

# Run multiple searches to cast a wide net
queries = [
    "company deployed AI agents with measurable results",
    "enterprise AI automation saving costs or headcount",
    "AI replacing manual operations with real metrics",
    "company AI-native transformation case study",
]

all_results = []
for q in queries:
    resp = requests.post("https://api.exa.ai/search", headers=headers, json={
        "query": q,
        "type": "auto",
        "numResults": 8,
        "startPublishedDate": "2026-02-01",  # ← adjust to ~4 weeks before current date
        "useAutoprompt": True
    })
    if resp.ok:
        all_results.extend(resp.json().get("results", []))

# Deduplicate by URL
seen = set()
unique = []
for r in all_results:
    if r["url"] not in seen:
        seen.add(r["url"])
        unique.append(r)

# Get full content for top candidates
top_ids = [r["id"] for r in unique[:15]]
resp2 = requests.post("https://api.exa.ai/contents", headers=headers, json={
    "ids": top_ids, "text": True, "highlights": True
})
```

**Selection criteria — a company MUST have all three:**
1. A specific, visceral PAIN (not vague "needed to innovate")
2. A concrete AI MOVE (what they actually deployed — not "adopted AI")
3. Measurable IMPACT (real numbers: %, $, time, headcount equivalent)

**Prefer:** Enterprise/ops/CX/logistics use cases (HappyRobot's audience), well-known companies (brand recognition in the feed), recent news (last 1-2 weeks). **Avoid:** Pure AI startups announcing products, vaporware, anything without real results.

If you can't find 3 strong ones in the last week, expand to 2-3 weeks. Quality over recency.

---

## PHASE 2 — WRITE THE CONTENT

For each company, write exactly these fields:

- **name**: Company name (just the name, no tagline)
- **pain**: 1-2 sentences. The problem before AI. Be specific and visceral. Use numbers where possible. Example: "700+ customer service agents handling repetitive inquiries. Costs spiraling. Average response time: 11 minutes."
- **move**: 1-2 sentences. What they actually deployed. Be concrete. Example: "Deployed an AI assistant that handled 2/3 of all customer chats within 30 days. Retrained humans for high-value conversations only."
- **impact**: 1-2 sentences. Lead with the number. Example: "Resolution time: 11 min → 2 min. Work equivalent of 700 agents. $40M projected annual savings."

**Tone:** Direct, confident, operator-to-operator. No "revolutionized," no "game-changing," no "leveraged AI." Write like you're explaining it to a smart founder over coffee.

**Critical constraint:** Keep each field to 2 sentences max. The text must fit on the carousel slides without overflowing. Shorter is better — punchier.

---

## PHASE 3 — BUILD THE CAROUSEL

Build a 5-slide LinkedIn carousel PDF using Python + Pillow. Each slide is **1080 × 1350 px** (4:5 portrait — maximum LinkedIn feed real estate on mobile).

### Brand Identity

```
COLORS:
  Navy:      #112B42  (17, 43, 66)   — primary dark background
  Navy Light: #183550  (24, 53, 80)   — subtle variation
  Parchment: #E0DDCD  (224, 221, 205) — signature light background (NOT white)
  Deep Gray:  #0E0D0C  (14, 13, 12)   — primary text on light
  Gold:       #D4A843  (212, 168, 67)  — accent, dividers, CTAs
  Sage Green: #A9C59D  (169, 197, 157) — secondary accent

FONTS (load from the happyrobot-brand skill assets):
  Tobias Regular (.otf) — baroque serif, headlines ONLY (H1/H2)
  Suisse Int'l Regular (.ttf) — grotesque sans, everything else

  Find them in the .skills/skills/happyrobot-brand/assets/fonts/ directory.

BRAND IMAGERY (from the same skill assets directory):
  blurred-background.png — atmospheric teal/blue texture for dark slides
  datalayer_sketch.png — isometric tech diagram, use as ghosted overlay for futuristic feel

  Find them in .skills/skills/happyrobot-brand/assets/images/

CHARLES'S HEADSHOT:
  ~/weekly news/charles_headshot.png (800×800 RGBA)
```

### Slide-by-Slide Design Spec

**SLIDE 1 — COVER (Navy background)**

Visual rhythm: Dark → Light → Dark (cover navy, company slides parchment, closer navy).

Layers (bottom to top):
1. Solid navy (#112B42) fill
2. `blurred-background.png` resized to 1080×1350, brightness reduced to 30%, blended at 50% opacity — creates subtle atmospheric depth
3. `datalayer_sketch.png` resized to page width, positioned at top, alpha reduced to ~6% — ghosted tech texture for futuristic feel
4. Subtle grid overlay (white lines, ~2.5% opacity, 54px spacing) — adds structure

Content (all left-aligned at x=80):
- **Top bar:** HappyRobot logo mark + "HappyRobot" text (Suisse 18px, white) at top-left (60, 56). Week label "MONTH YEAR · WEEK N" (Suisse 13px, white at 35% opacity) at top-right
- **"3" badge:** Gold (#D4A843) rounded rectangle (62×62, radius 14) with "3" in Suisse 32px navy. Positioned at y≈320
- **Title:** Three lines in Tobias 88px — "AI-Native" (white), "Companies" (white), "of the Week" (gold). Left-aligned
- **Gold divider:** 100px wide, 3px tall, gold, below title
- **Subtitle:** "Real companies. Real transformations." + "Every week." in Suisse 24px, white at 60% opacity
- **Swipe indicator:** "SWIPE" (Suisse 14px, white 35%) + gold arrow, bottom-left
- **Headshot:** Charles's photo in a circular crop (420px diameter), positioned bottom-right (slightly bleeding off edge: x = W-420+40, y = H-420+40). Gold ring (3px) around it with a faint outer glow (6px, gold at 15% opacity)

**SLIDES 2-4 — COMPANY CARDS (Parchment background)**

Background: Solid parchment (#E0DDCD)

Layout:
- **Top bar:** Logo mark + "HappyRobot" in Deep Gray at top-left. Counter "01 / 03" (Suisse 16px, 30% opacity) at top-right
- **Company name:** Tobias 86px, navy (#112B42), at x=72, y≈130
- **Gold accent:** 100×3px gold line below the company name

Then the page is divided into THREE equal-height full-width section cards that fill from below the name to the bottom of the page:

Each section card:
- Full-width background with a very subtle tint (4% opacity of the section color blended with parchment)
- 6px left accent bar in the section's color (full height of the card)
- Thin gold border between cards (1px, 15% opacity)
- Section label: Suisse 16px, uppercase, in the section's color. Small gold dot (6px circle) after the label
- Body text: Suisse 32px, Deep Gray at 90% opacity, line height 50px

Section colors:
- THE PAIN → warm brown (140, 60, 20)
- THE MOVE → navy (17, 43, 66)
- THE IMPACT → green (26, 120, 66)

**SLIDE 5 — CLOSING CTA (Navy background)**

Same atmospheric layers as cover (blurred bg + datalayer sketch, but sketch positioned at bottom this time).

Content (centered):
- Logo bar at top-left (same as cover)
- Decorative open quote mark: Tobias 200px, gold at 10% opacity, centered
- Headline: Tobias 52px, centered — "Every week, I break down" / "how real companies become" (white) / "AI-native." (gold)
- Gold divider: 88px wide, centered
- CTA pill: rounded rectangle (radius 14) with gold 10% fill + gold 22% border. Text: "Follow for weekly agentic AI insights" (Suisse 22px, white) + gold arrow
- Author row: Small circular headshot (56px) with gold ring + "Charles Lorin" (Suisse 20px, white) + "CEO @ HappyRobot · AI Voice Agents" (Suisse 15px, white 45%)
- Bottom: "happyrobot.ai" (Suisse 14px, white 25%)

### Technical Notes

- Use Pillow (PIL) for image generation — `pip install Pillow --break-system-packages`
- Tobias is an OTF font with CFF outlines. Pillow handles this natively via `ImageFont.truetype()`. Do NOT use reportlab (it can't handle CFF fonts)
- For alpha blending on solid backgrounds, pre-compute the blended RGB: `blended = tuple(int(fg * alpha + bg * (1-alpha)) for fg, bg in zip(fg_color, bg_color))`
- Circular photo crop: create an "L" mode mask image, draw a filled white ellipse, use as paste mask
- Save as multi-page PDF: `slides[0].save(out, "PDF", save_all=True, append_images=slides[1:], resolution=72)`
- Also save individual PNGs for preview/verification
- The logo mark is an abstract "H" made of two interlocking shapes. Draw it as filled polygons (simplified — the exact curves aren't critical at small sizes)

---

## PHASE 4 — VERIFY

After generating, open and review each slide PNG:
- [ ] All text fits within slide bounds (no overflow/clipping)
- [ ] Company names render correctly
- [ ] Content is factually accurate
- [ ] Cover has Charles's photo bottom-right with gold ring
- [ ] 5 slides total in the PDF
- [ ] Visual rhythm: dark → light → light → light → dark

---

## PHASE 5 — LINKEDIN POST COPY

Write a short LinkedIn post to accompany the carousel:

```
3 companies that went AI-native this week 👇

→ [Company 1]: [one-line hook]
→ [Company 2]: [one-line hook]
→ [Company 3]: [one-line hook]

Which transformation surprised you most? Drop a comment.

#AI #AINative #EnterpriseAI #Automation
```

Save the post copy as a .txt file alongside the PDF.

---

## OUTPUT

Save everything to the working directory:
- `ai-native-carousel.pdf` — the carousel, ready to upload to LinkedIn
- `ai-native-carousel_slide1.png` through `_slide5.png` — individual slides for review
- `linkedin-post.txt` — the post copy
