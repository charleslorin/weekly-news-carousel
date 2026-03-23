# Weekly AI-Native Companies Carousel

A LinkedIn carousel generator that researches and showcases companies going AI-native. Built for [HappyRobot](https://happyrobot.ai) by Charles Lorin.

Every week, the system finds 3 companies that deployed AI on customer or supplier-facing workflows, writes up their Pain / Move / Impact story, and generates a publication-ready 5-slide PDF carousel.

## What it produces

- **Slide 1** — Cover: "3 AI-Native Companies of the Week"
- **Slides 2-4** — Case study cards with hero stat banner, gold callout numbers, and full narrative
- **Slide 5** — Closing CTA with author info

All slides are 1080×1350px (4:5 portrait) — the optimal format for LinkedIn carousel PDFs.

## Quick start

```bash
# Install dependencies
pip install Pillow requests

# Set your Exa API key
export EXA_API_KEY="your-key-here"

# Search for companies
python3 run_weekly.py --dry-run

# Write companies.json with 3 picks, then generate
python3 run_weekly.py --from-json companies.json
```

Or run the carousel generator directly with the built-in test data:

```bash
python3 build_carousel.py
```

## How it works

### 1. Research (`run_weekly.py`)

Searches [Exa AI](https://exa.ai) for EMEA companies (Series C+, founded 2010-2021) deploying AI on operational workflows — customer support, RevOps, onboarding, order processing, shift management, etc.

### 2. Generate (`build_carousel.py`)

Takes company data and produces a branded PDF carousel using Pillow. Features:

- **Stat-led editorial layout** — gold callout numbers on the left, narrative text on the right
- **Hero stat banner** — the single most impressive metric, large and centered
- **Source citations** — every company slide cites its data source
- **Company logos** — auto-fetched via Clearbit API
- **Text overflow protection** — font sizes auto-calculated to fit all content

### 3. Automate (Claude Code)

Paste the prompt from `weekly-ai-native-carousel-prompt.md` into Claude Code and it runs the entire flow end-to-end: search → pick companies → write content → generate carousel → LinkedIn post copy.

```bash
claude --prompt "$(cat weekly-ai-native-carousel-prompt.md)"
```

## Brand system

| Element | Value |
|---------|-------|
| Background | Parchment `#E0DDCD` (never white) |
| Dark slides | Navy `#112B42` |
| Accent | Gold `#D4A843` |
| Body text | Deep Gray `#0E0D0C` |
| Headlines | Tobias Regular (serif) |
| Body | Suisse Int'l Regular (sans-serif) |
| Slide size | 1080×1350px (4:5) |

## Required assets (not included)

These are excluded from the repo for licensing/privacy:

- `brand-assets/` — HappyRobot brand fonts and images
- `charles_headshot.png` — author headshot

Place them in the project root before running.

## Company data structure

```python
{
    "name": "Company Name",
    "subtitle": "One-line descriptor · key metric",
    "domain": "company.com",
    "hero_stat": "8× faster",
    "hero_label": "context for the headline stat",
    "pain": "2-3 sentences about the problem before AI.",
    "move": "3-4 sentences about what they deployed.",
    "impact": "2-3 sentences with measurable results.",
    "callouts": {
        "pain_stat": "1.2M", "pain_label": "tickets per month",
        "move_stat": "31", "move_label": "languages supported",
        "impact_stat": "8×", "impact_label": "faster resolution"
    },
    "source": "Source: Company press release, Date"
}
```

## Target company criteria

- **Region:** EMEA
- **Stage:** Series C+
- **Founded:** 2010-2021 (not AI-native from day 1)
- **Verticals:** Marketplaces, Fintech, HR Tech, Travel, E-commerce, Logistics, Dev Tools, EdTech
- **AI projects:** Customer or supplier-facing workflows (CX, RevOps, onboarding, procurement, etc.)

## License

MIT
