# Build: "3 AI-Native Companies of the Week" — Weekly LinkedIn Carousel

You are a world-class brand designer and automation engineer. Your job is to build a production-quality weekly LinkedIn carousel that makes people STOP scrolling, READ every slide, and FOLLOW Charles Lorin.

Charles is CEO of HappyRobot (AI voice agents for enterprises — DHL, Uber Freight, TaskRabbit, Naturgy, Jobandtalent). He's building a personal brand as the go-to voice on companies going AI-native. This carousel is his flagship recurring LinkedIn format.

**The bar:** This should look like it was designed by a $50K/month creative agency. Not a Canva template. Not a "LinkedIn bro" carousel. Think: editorial magazine layout meets futuristic tech brand.

---

## STEP 0 — BRAND ASSETS SETUP

Before doing anything else, locate brand assets. Check in order:

```bash
# Find and unzip brand assets if needed
if [ ! -d "brand-assets" ] && [ ! -d "brand-assets/brand-assets" ]; then
  ZIP=$(ls brand-assets*.zip 2>/dev/null || ls ~/Downloads/brand-assets*.zip 2>/dev/null)
  if [ -n "$ZIP" ]; then
    unzip "$ZIP" -d brand-assets/
  fi
fi
```

Asset locations (check in order, use whichever exists):
- Fonts: `./brand-assets/brand-assets/fonts/` → `./brand-assets/fonts/` → `.skills/skills/happyrobot-brand/assets/fonts/`
- Images: `./brand-assets/brand-assets/images/` → `./brand-assets/images/` → `.skills/skills/happyrobot-brand/assets/images/`
- Headshot: `./charles_headshot.png` → `~/weekly news/charles_headshot.png` → look in `~/Downloads/` for `charles*pdp*` or `charles*headshot*`

Required files:
- `Tobias-Regular.otf` (baroque serif — headlines only)
- `SuisseIntl-Regular.ttf` (grotesque sans — everything else)
- `blurred-background.png` or `Blurred image background.png` (atmospheric texture)
- `datalayer_sketch.png` (isometric tech overlay)
- Charles's headshot photo (circular crop ready)

---

## WHAT YOU'RE BUILDING

A Python script (`build_carousel.py`) using **Pillow (PIL)** that generates a 5-slide LinkedIn carousel PDF (1080×1350px per slide, 4:5 portrait).

Then: an automation wrapper that uses Exa AI to research companies, writes punchy content, and generates the carousel + LinkedIn post.

**Do this in two phases. Phase 1 first, get my approval, then Phase 2.**

---

## PHASE 1 — BUILD THE CAROUSEL TEMPLATE

### Brand System

```
COLORS:
  Navy:         (17, 43, 66)    #112B42  — dark backgrounds, authority, gravitas
  Navy Light:   (24, 53, 80)    #183550  — subtle depth variation on dark slides
  Parchment:    (224, 221, 205) #E0DDCD  — light backgrounds (NEVER white — parchment IS the brand)
  Deep Gray:    (14, 13, 12)    #0E0D0C  — text on light backgrounds
  Gold:         (212, 168, 67)  #D4A843  — accents, dividers, CTAs, stat highlights
  Sage Green:   (169, 197, 157) #A9C59D  — secondary accent (sparingly)

FONTS:
  Tobias Regular (.otf) — elegant baroque serif. Headlines, company names, big stats ONLY.
  Suisse Int'l Regular (.ttf) — clean grotesque sans-serif. Everything else.

BRAND IMAGERY:
  blurred-background.png — atmospheric blue/teal depth layer for dark slides
  datalayer_sketch.png — isometric tech diagram, ghost at very low opacity for futuristic feel
```

### Design Philosophy

This carousel must feel like a premium editorial publication — think The Economist meets a high-end tech annual report. Every pixel is intentional.

1. **Information density done right** — Each company slide should teach the reader something they didn't know. The content should be rich enough that someone screenshots it and saves it.
2. **Visual hierarchy is king** — The reader's eye should follow a clear path: hero stat → company name → pain → move → impact. There must be ONE element per slide that dominates.
3. **Parchment is the signature** — Never use white. The warm parchment background is what makes this instantly recognizable in a sea of white/black LinkedIn carousels.
4. **Typography creates drama** — Tobias serif at large sizes creates authority. The contrast between elegant serif headlines and clean sans-serif body text is what makes this feel editorial, not startup-y.
5. **Dark-light-dark rhythm** — Cover (navy) → Company slides (parchment) → Closer (navy). Creates a visual arc that feels complete.
6. **Gold is the accent language** — Use it consistently for: stat numbers, dividers, accent dots, rings, CTAs. It ties everything together.

---

### SLIDE 1 — COVER (Navy, atmospheric)

The cover must stop the scroll in a LinkedIn feed. It needs to communicate: "This person curates something valuable every week."

**Background layers** (bottom to top):
- Solid navy `(17, 43, 66)` base
- `blurred-background.png` stretched to 1080×1350, brightness at 30%, blended at 50% opacity — creates atmospheric depth
- `datalayer_sketch.png` stretched to page width, positioned at top, alpha ~5-6% — ghosted tech texture
- Optional: very subtle grid overlay (white lines, 2-3% opacity, ~54px spacing)

**Content — LEFT-ALIGNED (x≈80)** to create intentional asymmetry with the headshot on the right:

- **Top bar:** HappyRobot logomark (abstract "H" as polygon approximation) + "HappyRobot" wordmark (Suisse ~18px, white). Week label top-right (Suisse 13px, white 35% opacity).

- **Gold "3" badge:** Rounded rectangle (~62×62px, radius 14, gold fill), number "3" centered in Suisse bold ~32px, navy color. This anchors the eye.

- **Title block (the hook):**
  - Tobias ~88px, three lines:
  - Line 1: "AI-Native" (white)
  - Line 2: "Companies" (white)
  - Line 3: "of the Week" (GOLD — this color shift creates emphasis)

- **Gold divider:** 100px × 3px horizontal line

- **Subtitle:** Suisse ~24px, white at 60% opacity
  - "Real companies. Real transformations."
  - "Every week."

- **Swipe indicator:** Bottom-left, "SWIPE" in Suisse 14px white 35% + small gold arrow (→)

- **Charles's headshot:** Bottom-right, circular crop ~420px diameter. Positioned to bleed slightly off the bottom-right edge (creates dynamism and modernity). Gold ring (3px) with faint outer glow. THE FACE IS CRITICAL — it builds trust and recognition in the feed.

---

### SLIDES 2–4 — COMPANY CARDS (Parchment, information-rich)

This is where the carousel earns its follows. Each slide = one company. The design must make dense content feel effortless to read.

**THE KEY INSIGHT: Content structure matters more than design.**

Each company needs:
- A **hero stat** that jumps off the page (the "screenshot moment")
- A **pain** that's visceral and specific (the hook that creates empathy)
- A **move** that teaches something concrete (the value — what they actually did)
- An **impact** that delivers the payoff (the proof)

**Layout structure (top to bottom):**

1. **Header strip** (y: 40–90):
   - Left: HappyRobot logomark + "HappyRobot" (Deep Gray, subtle, ~24px tall)
   - Right: Counter "01 / 03" (Suisse 16px, Deep Gray at 30% opacity)

2. **Company name** (y: ~120):
   - Tobias ~72px, Navy color, left-aligned at x≈72
   - Gold accent line below (80px × 3px)

3. **Hero stat bar** (y: ~240, full width):
   - This is the scroll-stopper on each company slide
   - Full-width strip: navy background `(17, 43, 66)` with slight transparency, height ~130px
   - Contains the single most impressive metric in LARGE type:
     - The number/stat: Tobias ~64px, GOLD color (e.g., "11 min → 2 min" or "80% faster" or "$40M saved")
     - A one-line label below: Suisse ~16px, white at 60% (e.g., "resolution time after AI deployment")
   - This bar creates visual drama and breaks up the parchment monotony

4. **Three content sections** (fill remaining space from below stat bar to bottom):
   - Divide the remaining vertical space into three sections
   - Each section gets proportional space based on content length, but THE MOVE gets the most room (~40%), PAIN and IMPACT split the rest (~30% each)

   **Each section structure:**
   - Colored left accent bar (5px wide, full section height)
   - Section label: Suisse ~14px, UPPERCASE, tracking +1px, in section color. Small gold dot (●) after label.
   - Body text: Suisse ~26-28px, Deep Gray at 90%, line-height ~42px
   - Thin separator line between sections (gold at 12% opacity)

   **Section colors:**
   - THE PAIN → warm rust `(160, 70, 30)` — feels urgent
   - THE MOVE → navy `(17, 43, 66)` — feels strategic
   - THE IMPACT → forest green `(30, 110, 60)` — feels triumphant

   **Content depth per section:**
   - **PAIN (2-3 sentences):** Set the scene. Be visceral. Use a specific number. Make the reader think "oh, I've felt that."
     - BAD: "They needed to improve customer service."
     - GOOD: "700+ agents drowning in repetitive tickets. Average handle time: 11 minutes. Every new market made it worse."

   - **MOVE (3-4 sentences):** This is where you TEACH. What specifically did they deploy? What was the architecture? What was surprising about their approach? This is Charles's thought-leadership moment.
     - BAD: "They deployed an AI solution."
     - GOOD: "Deployed an AI assistant across all chat channels in 30 days flat. The system handled 2/3 of all conversations autonomously — not by deflecting, but by actually resolving issues. Human agents were retrained exclusively for complex, high-empathy cases."

   - **IMPACT (2-3 sentences):** Lead with the number. Then give context that makes the number hit harder.
     - BAD: "They saw good results."
     - GOOD: "Resolution time collapsed from 11 minutes to 2. That's the equivalent output of 700 full-time agents — at a fraction of the cost. Projected savings: $40M/year."

---

### SLIDE 5 — CLOSING CTA (Navy, atmospheric)

Mirrors the cover's treatment. This slide converts scrollers into followers.

**Background:** Same atmospheric layers as cover (navy + blurred bg + datalayer sketch at bottom)

**Layout:**
- HappyRobot logo top-left (same as cover)
- Decorative open-quote mark: Tobias ~200px, gold at 10% opacity, centered — editorial touch
- **Headline:** Tobias ~50px, centered, white:
  - "Every week, I break down"
  - "how real companies become"
  - "AI-native." (this line in GOLD)
- Gold divider (88px, centered)
- **CTA pill:** Rounded rect, gold at 10% fill + gold at 22% border. Text: "Follow for weekly AI insights →" in Suisse ~22px, white. Arrow in gold.
- **Author row:** Small circular headshot (56px) with gold ring + "Charles Lorin" (Suisse 20px, white) + "CEO @ HappyRobot · AI Voice Agents" (Suisse 15px, white 45%)
- Bottom: "happyrobot.ai" (Suisse 14px, white 25%)

---

### Technical Requirements

- **Use Pillow (PIL)** — NOT reportlab (crashes on CFF/PostScript fonts), NOT matplotlib
- Tobias is OTF with CFF outlines. Pillow handles this natively via `ImageFont.truetype()`
- For transparency on solid backgrounds, pre-compute blended RGB: `tuple(int(fg*a + bg*(1-a)) for fg, bg in zip(fg_color, bg_color))`
- Circular photo: "L" mode mask, white filled ellipse, use as paste mask
- Logo: draw as filled polygons (approximate the SVG "H" shape — doesn't need to be exact at small sizes)
- Output: multi-page PDF via `slides[0].save(path, "PDF", save_all=True, append_images=slides[1:], resolution=72)`
- Also save individual PNGs for visual review
- **Text overflow protection:** Before rendering, measure text height. If it would overflow the section bounds, reduce font size by 2px and re-measure. Repeat until it fits.

### Test Data

Use these 3 companies to build/test the template. NOTE: This content is deliberately richer than v1 — the design must accommodate this depth:

```python
WEEK = "MARCH 2026 · WEEK 4"
COMPANIES = [
    {
        "name": "Klarna",
        "hero_stat": "11 min → 2 min",
        "hero_label": "customer resolution time after AI deployment",
        "pain": "700+ customer service agents drowning in repetitive tickets across 23 markets. Average handle time: 11 minutes. Every new country launch made the backlog worse — and hiring couldn't keep up.",
        "move": "Deployed an AI assistant across all chat channels in 30 days flat. The system handled 2/3 of all customer conversations autonomously — not by deflecting, but by actually resolving issues end-to-end. Human agents were retrained exclusively for complex, high-empathy cases that AI flagged for escalation.",
        "impact": "Resolution time collapsed from 11 minutes to 2. That's the equivalent output of 700 full-time agents — at a fraction of the cost. Projected annual savings: $40M. Customer satisfaction scores held steady through the transition.",
    },
    {
        "name": "Duolingo",
        "hero_stat": "+12% engagement",
        "hero_label": "after replacing static lessons with AI-powered roleplay",
        "pain": "Human tutors don't scale — and static pre-scripted lessons can't adapt to how each learner actually struggles. Personalization was the #1 user request, but building it manually meant hiring more content creators for every language pair.",
        "move": "Built AI-powered conversational roleplay directly into the core learning flow. Learners now practice real dialogues with an AI tutor that adapts difficulty in real-time, explains grammar mistakes contextually, and generates infinite practice scenarios. Reduced dependency on contract content creators by 10%.",
        "impact": "Engagement jumped 12%. Premium subscription growth accelerated. Duolingo set the benchmark for what AI-native edtech looks like — not AI as a feature, but AI as the core learning engine.",
    },
    {
        "name": "Mercado Libre",
        "hero_stat": "80% faster",
        "hero_label": "product listing time for sellers across Latin America",
        "pain": "Sellers spent 20+ minutes per listing — writing descriptions, selecting from thousands of categories, researching competitive pricing. For small sellers in Latin America, this friction was the #1 barrier to getting started. Onboarding was painfully slow.",
        "move": "Launched an AI listing engine: snap one photo, get a complete listing. The system auto-generates descriptions in the seller's language, classifies into the right category from 10,000+ options, suggests competitive pricing based on real-time market data, and optimizes the title for search.",
        "impact": "Listing creation time dropped 80%. New seller onboarding became 2× faster. First-quarter GMV from new sellers jumped 15% — proving that removing friction at the point of creation directly drives marketplace growth.",
    },
]
```

**After building, show me each slide as a PNG so I can review. We'll iterate until the design is perfect before moving to Phase 2.**

---

## PHASE 2 — AUTOMATED WEEKLY FLOW (only after Phase 1 is approved)

Once the template is locked, build `run_weekly.py` — a wrapper that researches, writes, generates, and outputs everything.

### Exa AI Setup

Exa is available as an MCP server. If not already connected, run:
```bash
claude mcp add --transport http exa https://mcp.exa.ai/mcp?exaApiKey=YOUR_EXA_API_KEY&tools=web_search_exa,web_search_advanced_exa,company_research_exa,deep_researcher_start,deep_researcher_check
```

For the Python automation script, use the Exa API directly with deep search + structured outputs:

```python
import requests
from datetime import datetime, timedelta

EXA_KEY = "YOUR_EXA_API_KEY"
HEADERS = {"x-api-key": EXA_KEY, "Content-Type": "application/json"}

four_weeks_ago = (datetime.now() - timedelta(weeks=4)).strftime("%Y-%m-%d")

resp = requests.post("https://api.exa.ai/search", headers=HEADERS, json={
    "query": "enterprise company deployed AI agents or automation with measurable cost savings headcount reduction or efficiency gains",
    "type": "deep",
    "num_results": 10,
    "category": "news",
    "startPublishedDate": four_weeks_ago,
    "outputSchema": {
        "type": "object",
        "description": "Companies that made concrete AI-native moves with measurable results",
        "required": ["companies"],
        "properties": {
            "companies": {
                "type": "array",
                "description": "List of companies with AI transformation stories",
                "items": {
                    "type": "object",
                    "required": ["name", "hero_stat", "hero_label", "pain", "move", "impact"],
                    "properties": {
                        "name": {
                            "type": "string",
                            "description": "Company name"
                        },
                        "hero_stat": {
                            "type": "string",
                            "description": "The single most impressive metric — short and punchy. Examples: '11 min → 2 min', '$40M saved', '80% faster', '3× throughput'"
                        },
                        "hero_label": {
                            "type": "string",
                            "description": "One-line context for the hero stat. Example: 'customer resolution time after AI deployment'"
                        },
                        "pain": {
                            "type": "string",
                            "description": "2-3 sentences: the specific problem before AI. Be visceral, use numbers, make it relatable. Set the scene."
                        },
                        "move": {
                            "type": "string",
                            "description": "3-4 sentences: what AI initiative they deployed. Be concrete and specific — what was the architecture? What was surprising? This is the teaching moment."
                        },
                        "impact": {
                            "type": "string",
                            "description": "2-3 sentences: measurable results. Lead with the biggest number. Give context that makes the number hit harder."
                        },
                        "source_url": {
                            "type": "string",
                            "description": "URL of the source article"
                        }
                    }
                }
            }
        }
    },
    "contents": {
        "highlights": {"max_characters": 4000}
    }
})

data = resp.json()
companies = data.get("output", {}).get("content", {}).get("companies", [])
grounding = data.get("output", {}).get("grounding", [])
```

Backup queries if first doesn't return 3 strong companies:
```python
backup_queries = [
    "company AI automation replacing manual processes with real ROI metrics",
    "enterprise AI deployment case study results 2026",
    "AI-native company transformation headcount cost savings",
]
```

### Company Selection Criteria

A company MUST have ALL THREE to qualify:
1. A specific, visceral **pain** (not vague "needed to innovate")
2. A concrete **AI move** (what they deployed — not just "adopted AI")
3. **Measurable impact** (real numbers: %, $, time, headcount)

**Prefer:** Enterprise/ops/CX/logistics use cases (HappyRobot's audience), well-known brands (recognition in feed), recent (last 1-4 weeks).
**Avoid:** Pure AI startups announcing products, vaporware, anything without concrete results.

### Content Writing Rules

After getting structured data from Exa, REWRITE each field to match the content depth and tone described in the slide spec above. The Exa output is raw material — you are the editor.

- **Tone:** Direct, operator-to-operator. Like a smart friend explaining over coffee. Never: "revolutionized," "game-changing," "leveraged AI," "cutting-edge."
- **hero_stat:** Must be ≤ 20 characters. It's the billboard headline.
- **hero_label:** Must be one line, ≤ 60 characters. Context for the stat.
- **pain:** 2-3 sentences. Visceral. Numbers help. Make the reader nod.
- **move:** 3-4 sentences. This is where you teach. Be specific about what they built.
- **impact:** 2-3 sentences. Lead with the number. Context that makes it land.
- **CRITICAL: Text must fit on the slides.** Test by running the generator and checking PNGs.

### Generate & Verify

1. Inject the 3 companies + current week label into `build_carousel.py` and run it
2. Open each slide PNG and verify:
   - All text fits within slide bounds (no overflow/clipping)
   - Company names render correctly
   - Hero stats are readable and impactful
   - Content is factually accurate (cross-reference with Exa's grounding citations)
   - Cover has Charles's photo bottom-right with gold ring
   - 5 slides total in the PDF
   - Visual rhythm: dark → light → light → light → dark

### LinkedIn Post Copy

Write a LinkedIn post to accompany the carousel. Format:

```
3 companies that satisfies AI-native this week 👇

1/ [Company] — [one-line hook with the hero stat]
2/ [Company] — [one-line hook with the hero stat]
3/ [Company] — [one-line hook with the hero stat]

The pattern? [One insightful observation tying the 3 stories together]

Which transformation surprised you most? Drop a comment.

♻️ Repost if your network needs to see this.

#AI #AINative #EnterpriseAI #Automation
```

Save as `linkedin-post.txt` alongside the PDF.

---

## OUTPUT FILES

All saved to the working directory:
- `build_carousel.py` — the reusable template generator
- `run_weekly.py` — the full automation script (Exa research → content → carousel → post)
- `ai-native-carousel.pdf` — this week's carousel
- `ai-native-carousel_slide1.png` through `_slide5.png` — previews
- `linkedin-post.txt` — the post copy

**Start with Phase 1 now. Build the template, show me the slides, and wait for my feedback before proceeding.**
