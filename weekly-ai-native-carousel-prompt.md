# Weekly AI-Native Carousel — Automation Prompt

Run this prompt in Claude Code to produce the full carousel end-to-end:

```bash
claude --prompt "$(cat ~/Projects/weekly\ news/weekly-ai-native-carousel-prompt.md)"
```

---

## The Prompt

```
You are producing the weekly "AI-Native Companies of the Week" LinkedIn carousel for Charles Lorin, founder of HappyRobot (Digital Natives @HappyRobot). Published every Friday.

Working directory: ~/Projects/weekly news/

## STEP 1 — RESEARCH (Exa AI via run_weekly.py)

Run the Exa search script:

```bash
cd ~/Projects/weekly\ news && python3 run_weekly.py --dry-run
```

This searches Exa AI for EMEA companies becoming AI-native and saves results to `research.json`. Review the output.

### Company Selection Criteria — ALL must apply:

**Company profile:**
- Based in EMEA (Europe, Middle East, Africa)
- Series C or above
- Founded between 2010 and 2021
- NOT an AI-native company from the start — this is a traditional tech company becoming AI-native
- One or more of these verticals:
  - Marketplaces & Two-Sided Platforms
  - Fintech, Neobanks & Financial Services Platforms
  - HR Tech & Workforce Platforms
  - Travel & Hospitality Tech
  - E-commerce & D2C Platforms
  - Logistics & Supply Chain Tech
  - Developer Tools & Infrastructure
  - EdTech & Content Platforms

**AI project must be customer or supplier-facing workflows:**
The company is launching AI to transform operational workflows — not just internal tooling. Examples:
- Customer support / contact center automation
- RevOps / sales automation
- Finance / billing / collections
- Shift management / workforce scheduling
- Vendor or customer onboarding
- Procurement / sourcing
- Order processing / fulfilment
- KYC/KYB compliance automation
- Pricing / demand forecasting
- Quality assurance / claims handling
Be creative — any workflow that touches customers or suppliers counts.

**Content must include ALL THREE:**
1. A specific, visceral PAIN — what was broken before? Use numbers where possible.
2. A concrete AI MOVE — what they actually deployed. Not "adopted AI" — what specifically?
3. Measurable IMPACT — real numbers: %, $, €, time saved, headcount equivalent.

**Avoid:** Pure AI startups, vaporware announcements, anything without concrete results, US-only companies.

### If Exa doesn't return 3 strong matches:

Run additional targeted searches directly:

```bash
python3 -c "
import requests, json
from datetime import datetime, timedelta
headers = {'x-api-key': 'YOUR_EXA_API_KEY', 'Content-Type': 'application/json'}
start = (datetime.now() - timedelta(weeks=8)).strftime('%Y-%m-%d')
resp = requests.post('https://api.exa.ai/search', headers=headers, json={
    'query': 'YOUR CUSTOM QUERY HERE',
    'type': 'auto', 'numResults': 10, 'category': 'news',
    'startPublishedDate': start, 'useAutoprompt': True,
    'contents': {'highlights': {'maxCharacters': 4000}},
}, timeout=60)
for r in resp.json().get('results', []):
    print(r['title'])
    print(r['url'])
    print(r.get('highlights', [''])[0][:200])
    print()
"
```

Vary the query: try specific verticals, specific workflows, specific countries. Widen the date range to 8-12 weeks if needed. As a last resort, use 2 companies instead of 3.

## STEP 2 — PICK 3 COMPANIES & WRITE THE CONTENT

From the research results, pick the 3 best companies matching ALL criteria above. For each, write:

- **name**: Company name (keep it short — must fit on a carousel slide)
- **pain**: 1-2 sentences. The problem before AI. Visceral, specific, use numbers.
- **move**: 1-2 sentences. What they actually deployed. Concrete — "deployed X that does Y."
- **impact**: 1-2 sentences. Lead with the number. Real metrics only.

**Tone:** Direct, confident, no fluff. Write like a smart operator explaining to another operator. No buzzwords, no "revolutionized", no "game-changing", no "leveraged AI."

**Critical: max 2 sentences per field.** Text must fit on carousel slides without overflow.

Save as `companies.json`:

```bash
cat > ~/Projects/weekly\ news/companies.json << 'JSONEOF'
[
  {
    "name": "Company Name",
    "pain": "...",
    "move": "...",
    "impact": "..."
  },
  {
    "name": "Company Name",
    "pain": "...",
    "move": "...",
    "impact": "..."
  },
  {
    "name": "Company Name",
    "pain": "...",
    "move": "...",
    "impact": "..."
  }
]
JSONEOF
```

## STEP 3 — GENERATE THE CAROUSEL

Run:

```bash
cd ~/Projects/weekly\ news && python3 run_weekly.py --from-json companies.json
```

This generates:
- `ai-native-carousel.pdf` — the LinkedIn carousel
- `ai-native-carousel_slide1.png` through `_slide5.png` — slide previews
- `linkedin-post.txt` — the accompanying post
- Updates `edition.txt` with the current edition number

## STEP 4 — VERIFY

Open each slide PNG and review:

```bash
open ~/Projects/weekly\ news/ai-native-carousel_slide*.png
```

Check:
- [ ] Company names render correctly (no text overflow)
- [ ] Content is factually accurate (cross-reference with Exa sources)
- [ ] No slide has text running off the edge
- [ ] Cover slide has Charles's photo bottom-right with sage green ring
- [ ] Cover shows correct edition number
- [ ] "Every Friday" on cover and closing slide
- [ ] "Digital Natives @HappyRobot" on closing slide
- [ ] All 5 slides present in PDF

If text overflows, shorten the content in companies.json and regenerate.

## STEP 5 — LINKEDIN POST + TYPEFULLY DRAFT

Read `linkedin-post.txt` and improve if needed. The post should follow this format:

```
3 companies that went AI-native this week 👇

→ [Company 1]: [one-line hook with the key metric]
→ [Company 2]: [one-line hook with the key metric]
→ [Company 3]: [one-line hook with the key metric]

Which transformation surprised you most?

#AI #AINative #EnterpriseAI
```

If Typefully is connected as an MCP server, create a draft there with the post text. The carousel PDF must be uploaded manually to the draft (Typefully MCP doesn't support file attachments).

## CONSTRAINTS
- Never fabricate company data. Every claim must trace back to a real source found by Exa.
- Companies must match the profile: EMEA, Series C+, founded 2010-2021, NOT AI-native from day 1.
- AI projects must be on customer/supplier-facing workflows.
- Keep body text to max 2 sentences per field — overflow breaks the carousel.
- The carousel brand uses Sage Green (#A9C59D) as the accent, NOT gold. Parchment (#E0DDCD) backgrounds, never white.
```

---

## How to Use

### Option A: Manual Friday run
Open Claude Code in `~/Projects/weekly news/`, paste the prompt above, and let it run.

### Option B: Claude Code with `--prompt` flag
```bash
cd ~/Projects/weekly\ news && claude --prompt "$(cat weekly-ai-native-carousel-prompt.md)"
```

### Option C: Step by step
```bash
# 1. Search
python3 run_weekly.py --dry-run

# 2. Review research.json, write companies.json (or ask Claude to)

# 3. Generate
python3 run_weekly.py --from-json companies.json

# 4. Review
open ai-native-carousel_slide*.png
```
