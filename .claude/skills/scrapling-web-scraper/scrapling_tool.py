#!/usr/bin/env python3
"""
Scrapling Web Scraping Tool
Simplified wrapper for command-line usage
"""

import sys
import json
import argparse

try:
    from scrapling.fetchers import Fetcher, StealthyFetcher, DynamicFetcher
    SCRAPLING_AVAILABLE = True
except ImportError:
    SCRAPLING_AVAILABLE = False
    print("Scrapling not installed. Run: pip install 'scrapling[all]'")
    sys.exit(1)

def scrape_basic(url, selector=None):
    """Basic scraping mode"""
    try:
        page = Fetcher.get(url)
        result = {
            "url": url,
            "title": page.css('title::text').get(),
            "status": "success"
        }
        if selector:
            result["data"] = page.css(selector).getall()
        else:
            result["text"] = page.css('body').get()
        return result
    except Exception as e:
        return {"error": str(e), "url": url}

def scrape_stealth(url, selector=None, solve_cloudflare=False):
    """Stealth mode (bypass Cloudflare)"""
    try:
        page = StealthyFetcher.fetch(url,
                                      headless=True,
                                      solve_cloudflare=solve_cloudflare)
        result = {
            "url": url,
            "title": page.css('title::text').get(),
            "mode": "stealth",
            "status": "success"
        }
        if selector:
            result["data"] = page.css(selector).getall()
        return result
    except Exception as e:
        return {"error": str(e), "url": url}

def scrape_dynamic(url, selector=None, wait_for=None):
    """Dynamic content scraping (JavaScript rendering)"""
    try:
        page = DynamicFetcher.fetch(url, headless=True, network_idle=True)

        if wait_for:
            page.wait_for_selector(wait_for, timeout=10000)

        result = {
            "url": url,
            "title": page.css('title::text').get(),
            "mode": "dynamic",
            "status": "success"
        }
        if selector:
            result["data"] = page.css(selector).getall()
        return result
    except Exception as e:
        return {"error": str(e), "url": url}

def main():
    parser = argparse.ArgumentParser(description='Scrapling Web Scraping Tool')
    parser.add_argument('url', help='Target URL to scrape')
    parser.add_argument('--mode', choices=['basic', 'stealth', 'dynamic'],
                       default='basic', help='Scraping mode')
    parser.add_argument('--selector', '-s', help='CSS selector to extract')
    parser.add_argument('--cloudflare', action='store_true',
                       help='Solve Cloudflare (stealth mode)')
    parser.add_argument('--wait', help='Wait for selector (dynamic mode)')
    parser.add_argument('--json', '-j', action='store_true',
                       help='Output as JSON')

    args = parser.parse_args()

    if args.mode == 'basic':
        result = scrape_basic(args.url, args.selector)
    elif args.mode == 'stealth':
        result = scrape_stealth(args.url, args.selector, args.cloudflare)
    elif args.mode == 'dynamic':
        result = scrape_dynamic(args.url, args.selector, args.wait)

    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print(f"URL: {result.get('url')}")
        print(f"Title: {result.get('title')}")
        if 'data' in result:
            print(f"\nExtracted Data ({len(result['data'])} items):")
            for i, item in enumerate(result['data'][:5], 1):
                print(f"  {i}. {item[:100]}...")
        if 'error' in result:
            print(f"\nError: {result['error']}")

if __name__ == '__main__':
    main()
