---
name: Scrapling Web Scraper
description: Zero-bot-detection web scraping. Bypass Cloudflare, handle JavaScript-heavy sites, and adapt to website changes automatically. Supports basic, stealth, and dynamic scraping modes.
---

# Scrapling Web Scraping Tool

Web scraping skill using the Scrapling library. Supports three modes:
- **Basic**: Fast HTTP requests via `Fetcher`
- **Stealth**: Undetectable scraping with anti-bot evasion via `StealthyFetcher`
- **Dynamic**: Full browser automation for JavaScript-heavy sites via `DynamicFetcher`

## Setup (one-time)

```bash
pip install "scrapling[all]"
scrapling install
```

## Usage

### CLI

```bash
# Basic scrape
python3 scrapling_tool.py https://example.com --json

# Extract specific elements with CSS selector
python3 scrapling_tool.py https://example.com --selector "h1, h2, p" --json

# Stealth mode with Cloudflare bypass
python3 scrapling_tool.py https://example.com --mode stealth --cloudflare --json

# Dynamic mode for JavaScript SPAs
python3 scrapling_tool.py https://example.com --mode dynamic --wait ".content" --json
```

The `scrapling_tool.py` file is located at `.claude/skills/scrapling-web-scraper/scrapling_tool.py`.

### Python API

```python
from scrapling.fetchers import Fetcher, StealthyFetcher, DynamicFetcher

# Basic
page = Fetcher.get("https://example.com")
title = page.css('title::text').get()
paragraphs = page.css('p::text').getall()

# Stealth (Cloudflare bypass)
page = StealthyFetcher.fetch("https://example.com", headless=True, solve_cloudflare=True)

# Dynamic (JS rendering)
page = DynamicFetcher.fetch("https://example.com", headless=True, network_idle=True)
```

### CSS Selectors

- `h1::text` - heading text
- `p::text` - paragraph text
- `.class-name` - elements by class
- `#id` - element by ID
- `a::attr(href)` - link URLs
- `img::attr(src)` - image sources

## Important

- Only scrape websites you are authorized to access
- Respect robots.txt and website Terms of Service
- Use stealth/dynamic modes only when basic mode is insufficient
