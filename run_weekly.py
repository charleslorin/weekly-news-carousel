"""
Weekly AI-Native Carousel — Automation Script
Searches Exa AI for articles, extracts company stories, generates carousel + LinkedIn post.

Usage:
    python3 run_weekly.py                  # full run: search → generate
    python3 run_weekly.py --edition 5      # override edition number
    python3 run_weekly.py --dry-run        # search only, save research.json
    python3 run_weekly.py --from-json research.json  # skip search, generate from saved data
"""

import requests, json, os, sys, re, argparse
from datetime import datetime, timedelta

# ── CONFIG ────────────────────────────────────────────────────────────
EXA_KEY = os.environ.get("EXA_API_KEY", "")
HEADERS = {"x-api-key": EXA_KEY, "Content-Type": "application/json"}
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
EDITION_FILE = os.path.join(BASE_DIR, "edition.txt")

# Target: EMEA companies, Series C+, founded 2010-2021 (NOT AI-native from day 1)
# Launching AI projects on customer/supplier-facing workflows to become AI-native
# Verticals: marketplaces, fintech, HR tech, travel, e-commerce, logistics, dev tools, edtech

QUERIES = [
    # Customer-facing AI workflows
    "European company launching AI customer support automation chatbot agents results 2026",
    "European fintech e-commerce AI customer service onboarding automation measurable results",
    "European company AI-powered sales revops automation deployment results",
    # Supplier/ops-facing AI workflows
    "European company AI vendor onboarding procurement supply chain automation results",
    "European company AI shift management workforce scheduling automation results",
    "European logistics marketplace AI operations finance automation deployment",
    # Broad EMEA becoming AI-native
    "European startup going AI-native deploying AI agents across operations 2026 results",
    "EMEA company AI transformation customer operations real metrics cost savings",
    # Vertical-specific becoming AI-native
    "European fintech neobank deploying AI agents customer operations not AI startup",
    "European marketplace platform travel hospitality AI deployment operations results",
    "European HR tech edtech company launching AI automation workflows results",
]


# ── EXA SEARCH ────────────────────────────────────────────────────────
def search_exa(query, weeks_back=4):
    """Search Exa and return raw article results with highlights."""
    start_date = (datetime.now() - timedelta(weeks=weeks_back)).strftime("%Y-%m-%d")
    print(f"  Searching: {query[:80]}...")
    resp = requests.post(
        "https://api.exa.ai/search",
        headers=HEADERS,
        json={
            "query": query,
            "type": "auto",
            "numResults": 10,
            "category": "news",
            "startPublishedDate": start_date,
            "useAutoprompt": True,
            "contents": {"highlights": {"maxCharacters": 4000}},
        },
        timeout=60,
    )
    resp.raise_for_status()
    return resp.json().get("results", [])


def extract_company_name(title):
    """Best-effort extraction of company name from article title."""
    # Common patterns: "Company does X", "Company's Y", "How Company Z"
    # Remove common prefixes
    title = re.sub(r"^(How |Why |What |When )", "", title)
    # Take text before common separators
    for sep in [" claims ", " deploys ", " deployed ", " launches ", " launched ",
                " announces ", " announced ", " reports ", " reveals ", " says ",
                " cuts ", " saves ", " reduces ", " automates ", " uses ",
                " delivers ", " delivered ", " achieved ", "'s ", "\u2019s ",
                " AI-", " -"]:
        if sep in title:
            return title.split(sep)[0].strip()
    # Take text before pipe/dash at end
    for sep in [" | ", " \u2013 ", " - "]:
        if sep in title:
            parts = title.split(sep)
            # Company name is usually the shorter part
            return min(parts, key=len).strip()
    return title.split()[0]  # fallback: first word


VERTICAL_KEYWORDS = {
    "Marketplace": ["marketplace", "two-sided", "platform connect", "matching"],
    "Fintech": ["fintech", "neobank", "banking", "payments", "lending", "insurance", "financial"],
    "HR Tech": ["hr tech", "workforce", "hiring", "recruitment", "payroll", "employee"],
    "Travel": ["travel", "hospitality", "booking", "hotel", "flight", "tourism"],
    "E-commerce": ["e-commerce", "ecommerce", "d2c", "retail", "shopping", "commerce"],
    "Logistics": ["logistics", "supply chain", "shipping", "freight", "delivery", "warehouse"],
    "Dev Tools": ["developer", "devtools", "infrastructure", "api", "cloud", "saas platform"],
    "EdTech": ["edtech", "education", "learning", "content platform", "training"],
}

WORKFLOW_KEYWORDS = {
    "CX": ["customer support", "customer service", "contact center", "helpdesk", "chat", "ticket"],
    "RevOps": ["revops", "revenue operations", "sales ops", "sales automation", "crm", "pipeline"],
    "Finance": ["finance", "accounting", "invoice", "billing", "collections", "expense"],
    "Onboarding": ["onboarding", "vendor onboarding", "supplier onboarding", "customer onboarding"],
    "Shift Mgmt": ["shift", "scheduling", "workforce management", "rostering", "staffing"],
    "Procurement": ["procurement", "purchasing", "vendor management", "sourcing", "rfp"],
    "Ops": ["operations", "fulfilment", "fulfillment", "order processing", "automation"],
}


def guess_tags(title, highlights):
    """Best-effort vertical + workflow classification from article text."""
    text = (title + " " + " ".join(highlights)).lower()
    verticals = [v for v, kws in VERTICAL_KEYWORDS.items() if any(kw in text for kw in kws)]
    workflows = [w for w, kws in WORKFLOW_KEYWORDS.items() if any(kw in text for kw in kws)]
    parts = []
    if verticals:
        parts.append(", ".join(verticals))
    if workflows:
        parts.append("→ " + ", ".join(workflows))
    return " | ".join(parts) if parts else "?"


def find_articles(target=15):
    """Search Exa with multiple queries, deduplicate, return articles."""
    all_articles = []
    seen_urls = set()

    for i, query in enumerate(QUERIES):
        if len(all_articles) >= target:
            break
        weeks_back = 4 if i < 2 else 8
        results = search_exa(query, weeks_back)
        for r in results:
            url = r.get("url", "")
            if url in seen_urls:
                continue
            seen_urls.add(url)
            highlights = r.get("highlights", [])
            all_articles.append({
                "title": r.get("title", ""),
                "url": url,
                "published": r.get("publishedDate", ""),
                "highlights": highlights,
                "company_guess": extract_company_name(r.get("title", "")),
                "tags": guess_tags(r.get("title", ""), highlights),
            })

    return all_articles[:target]


# ── LINKEDIN POST ─────────────────────────────────────────────────────
def generate_linkedin_post(companies):
    lines = ["3 companies that went AI-native this week\n"]
    for co in companies:
        # Split on sentence-ending period (followed by space or end), not decimal points
        sentences = re.split(r'\.(?:\s|$)', co["impact"])
        hook = sentences[0].strip()
        lines.append(f"> {co['name']}: {hook}")
    lines.append("\nWhich transformation surprised you most?\n")
    lines.append("#AI #AINative #EnterpriseAI")
    return "\n".join(lines)


# ── EDITION TRACKING ──────────────────────────────────────────────────
def get_edition(override=None):
    if override is not None:
        return override
    if os.path.exists(EDITION_FILE):
        with open(EDITION_FILE) as fh:
            return int(fh.read().strip()) + 1
    return 1


def save_edition(n):
    with open(EDITION_FILE, "w") as fh:
        fh.write(str(n))


# ── GENERATE CAROUSEL ─────────────────────────────────────────────────
def generate_carousel(companies, edition):
    now = datetime.now()
    week_label = now.strftime("%B %Y").upper() + f" \u00b7 WEEK {now.isocalendar()[1]}"

    sys.path.insert(0, BASE_DIR)
    import build_carousel

    build_carousel.WEEK = week_label
    build_carousel.EDITION = edition
    build_carousel.COS = [
        {
            "name": co["name"],
            "hero_stat": co.get("hero_stat", ""),
            "hero_label": co.get("hero_label", ""),
            "pain": co["pain"],
            "move": co["move"],
            "impact": co["impact"],
        }
        for co in companies
    ]
    build_carousel.main()


# ── MAIN ──────────────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(description="Weekly AI-Native Carousel Generator")
    parser.add_argument("--edition", type=int, help="Override edition number")
    parser.add_argument("--dry-run", action="store_true", help="Search only, save research")
    parser.add_argument("--from-json", type=str, help="Skip search, load companies from JSON")
    args = parser.parse_args()

    edition = get_edition(args.edition)
    print(f"\n{'='*60}")
    print(f"  AI-Native Companies of the Week \u2014 Edition {edition}")
    print(f"{'='*60}\n")

    # ── MODE 1: Generate from pre-written JSON ──
    if args.from_json:
        print(f"[1/3] Loading companies from {args.from_json}...\n")
        with open(args.from_json) as fh:
            companies = json.load(fh)
        for i, co in enumerate(companies, 1):
            print(f"  {i}. {co['name']}")
        print()
    else:
        # ── MODE 2: Search Exa for articles ──
        print("[1/3] Searching Exa AI for articles...\n")
        articles = find_articles(target=15)

        if not articles:
            print("ERROR: No articles found.")
            sys.exit(1)

        # Save raw research
        research_path = os.path.join(BASE_DIR, "research.json")
        with open(research_path, "w") as fh:
            json.dump(articles, fh, indent=2)

        print(f"\nFound {len(articles)} articles:\n")
        for i, a in enumerate(articles, 1):
            date = a["published"][:10] if a["published"] else "unknown"
            vtag = f" [{a['tags']}]" if a.get("tags") else ""
            print(f"  {i:2d}. [{date}] {a['company_guess']}{vtag}")
            print(f"      {a['title']}")
            print(f"      {a['url']}")
            if a["highlights"]:
                snippet = a["highlights"][0][:150].replace("\n", " ")
                print(f"      \"{snippet}...\"")
            print()

        print(f"Research saved to {research_path}")

        if args.dry_run:
            print("\nDry run complete. Review research.json, then either:")
            print("  1. Create companies.json with pain/move/impact for each company")
            print("     and run: python3 run_weekly.py --from-json companies.json")
            print("  2. Or paste the research into Claude Code to write the content")
            return

        # Without an LLM, we can't auto-write pain/move/impact from raw articles.
        # Print instructions for the user.
        print("\n" + "="*60)
        print("  NEXT STEP: Write the company content")
        print("="*60)
        print()
        print("The Exa search found articles above. To generate the carousel,")
        print("create a companies.json file with 3 entries like this:\n")
        print(json.dumps([{
            "name": "Company Name",
            "pain": "1-2 sentences about the problem before AI.",
            "move": "1-2 sentences about what AI they deployed.",
            "impact": "1-2 sentences with measurable results.",
        }], indent=2))
        print(f"\nThen run: python3 run_weekly.py --from-json companies.json")
        print("Or: paste the research into Claude Code and ask it to write + generate.")
        return

    # ── Generate carousel ──
    print("[2/3] Generating carousel PDF + PNGs...\n")
    generate_carousel(companies, edition)

    # ── LinkedIn post ──
    print("\n[3/3] Writing LinkedIn post...\n")
    post = generate_linkedin_post(companies)
    post_path = os.path.join(BASE_DIR, "linkedin-post.txt")
    with open(post_path, "w") as fh:
        fh.write(post)
    print(post)
    print(f"\nSaved to {post_path}")

    # Save edition
    save_edition(edition)

    print(f"\nDone! Edition {edition} complete.")
    print(f"  PDF: {os.path.join(BASE_DIR, 'ai-native-carousel.pdf')}")
    print(f"  Post: {post_path}")


if __name__ == "__main__":
    main()
