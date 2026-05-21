"""
dhl_fuel_surcharge.py
Fetches the current DHL Express fuel surcharge percentage from:
  https://mydhl.express.dhl/in/en/ship/surcharges.html#/fuel_surcharge

The page is a JavaScript SPA; the data is loaded from a JSON API endpoint.
This script tries the known endpoint patterns and falls back to scraping
the rendered HTML via Playwright if available.

Usage:
    python dhl_fuel_surcharge.py [--country in] [--lang en]

Returns:
    Prints the current fuel surcharge % and effective date to stdout.
    Exit code 0 on success, 1 on failure.
"""

import argparse
import json
import re
import sys
from datetime import date, datetime

# ── try requests first (lightweight) ──────────────────────────────────────────
try:
    import requests
    HAS_REQUESTS = True
except ImportError:
    HAS_REQUESTS = False

# ── try playwright as fallback (renders JS) ────────────────────────────────────
try:
    from playwright.sync_api import sync_playwright
    HAS_PLAYWRIGHT = True
except ImportError:
    HAS_PLAYWRIGHT = False


HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept": "application/json, text/plain, */*",
    "Referer": "https://mydhl.express.dhl/",
}

# Known API endpoint patterns used by the MyDHL+ SPA (discovered via browser devtools)
API_PATTERNS = [
    "https://mydhl.express.dhl/{country}/{lang}/content/surcharges.json",
    "https://mydhl.express.dhl/api/{lang}/content/surcharges?country={country}",
    "https://mydhl.express.dhl/{country}/{lang}/ship/surcharges.json",
    "https://mydhl.express.dhl/content/dhl/{country}/{lang}/ship/surcharges/_jcr_content/surcharges.json",
    "https://mydhl.express.dhl/{country}/{lang}/ship/surcharges/jcr:content.json",
]


def parse_surcharge_data(data, today=None):
    """
    Given a parsed JSON object (dict or list), find the fuel surcharge
    entry closest to today and return (effective_date_str, rate_percent).
    """
    today = today or date.today()

    # Normalise to a flat list of records
    records = []
    if isinstance(data, list):
        records = data
    elif isinstance(data, dict):
        # Common structures: {"surcharges": [...]} or {"fuelSurcharge": [...]}
        for key in ("surcharges", "fuelSurcharge", "fuel_surcharge", "items", "data"):
            if key in data and isinstance(data[key], list):
                records = data[key]
                break
        if not records:
            # Flatten one level deep
            for v in data.values():
                if isinstance(v, list):
                    records = v
                    break

    # Filter to fuel-surcharge-related records
    fuel_records = []
    for rec in records:
        if not isinstance(rec, dict):
            continue
        label = " ".join(str(v) for v in rec.values()).lower()
        if "fuel" in label:
            fuel_records.append(rec)
    if not fuel_records:
        fuel_records = records  # fall back to all records

    # Find common date and rate field names
    DATE_KEYS = ("effectiveDate", "effective_date", "date", "startDate",
                 "validFrom", "valid_from", "month", "period")
    RATE_KEYS = ("rate", "surcharge", "percentage", "percent",
                 "fuelSurcharge", "fuel_surcharge", "value", "amount")

    best = None
    best_delta = None

    for rec in fuel_records:
        # Extract date
        rec_date = None
        for dk in DATE_KEYS:
            if dk in rec:
                raw = rec[dk]
                for fmt in ("%Y-%m-%d", "%d/%m/%Y", "%m/%Y", "%Y/%m",
                            "%B %Y", "%b %Y", "%Y-%m"):
                    try:
                        parsed = datetime.strptime(str(raw).strip(), fmt).date()
                        # For month-only formats, use last day of month
                        if fmt in ("%m/%Y", "%Y/%m", "%B %Y", "%b %Y", "%Y-%m"):
                            import calendar
                            last = calendar.monthrange(parsed.year, parsed.month)[1]
                            parsed = parsed.replace(day=last)
                        rec_date = parsed
                        break
                    except ValueError:
                        continue
                if rec_date:
                    break

        # Extract rate
        rec_rate = None
        for rk in RATE_KEYS:
            if rk in rec:
                try:
                    rec_rate = float(str(rec[rk]).replace("%", "").strip())
                    break
                except (ValueError, TypeError):
                    continue

        if rec_rate is None:
            continue

        if rec_date is None:
            # No date available — just use this record if it's the only one
            if best is None:
                best = (None, rec_rate, rec)
            continue

        delta = abs((rec_date - today).days)
        if best_delta is None or delta < best_delta:
            best_delta = delta
            best = (rec_date, rec_rate, rec)

    return best


def try_api_endpoints(country, lang):
    """Try each API endpoint pattern with requests. Return parsed JSON or None."""
    if not HAS_REQUESTS:
        return None
    session = requests.Session()
    session.headers.update(HEADERS)
    for pattern in API_PATTERNS:
        url = pattern.format(country=country, lang=lang)
        try:
            resp = session.get(url, timeout=10)
            if resp.status_code == 200:
                ct = resp.headers.get("content-type", "")
                if "json" in ct or resp.text.strip().startswith(("[", "{")):
                    try:
                        return resp.json(), url
                    except json.JSONDecodeError:
                        continue
        except Exception:
            continue
    return None, None


def scrape_with_playwright(country, lang):
    """
    Use Playwright to render the page and intercept the XHR/fetch response
    that contains the fuel surcharge data.
    """
    if not HAS_PLAYWRIGHT:
        return None, None

    target_url = (
        f"https://mydhl.express.dhl/{country}/{lang}/ship/surcharges.html"
        "#/fuel_surcharge"
    )
    captured = {}

    def handle_response(response):
        url = response.url
        if "surcharge" in url.lower() or "fuel" in url.lower():
            try:
                captured[url] = response.json()
            except Exception:
                pass

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.on("response", handle_response)
        page.goto(target_url, wait_until="networkidle", timeout=30000)
        # Wait a bit more for lazy XHRs
        page.wait_for_timeout(3000)
        browser.close()

    if captured:
        url, data = next(iter(captured.items()))
        return data, url

    return None, None


def scrape_html_fallback(country, lang):
    """
    Last resort: fetch raw HTML and look for inline JSON containing 'fuel'
    or a percentage pattern near the word 'fuel'.
    """
    if not HAS_REQUESTS:
        return None, None
    url = (
        f"https://mydhl.express.dhl/{country}/{lang}/ship/surcharges.html"
    )
    try:
        resp = requests.get(url, headers=HEADERS, timeout=15)
        html = resp.text
    except Exception:
        return None, None

    # Look for JSON blobs containing 'fuel'
    blobs = re.findall(r'\{[^{}]{0,2000}fuel[^{}]{0,2000}\}', html, re.IGNORECASE)
    for blob in blobs:
        try:
            data = json.loads(blob)
            return data, url
        except Exception:
            continue

    # Look for plain percentage near 'fuel surcharge'
    pct_near_fuel = re.findall(
        r'fuel[^.]{0,80}?(\d{1,2}(?:\.\d{1,2})?)\s*%',
        html, re.IGNORECASE
    )
    if pct_near_fuel:
        rate = float(pct_near_fuel[0])
        return {"rate": rate, "source": "html_regex"}, url

    return None, None


def main():
    parser = argparse.ArgumentParser(description="Fetch DHL fuel surcharge rate")
    parser.add_argument("--country", default="in",
                        help="Country code (default: in for India)")
    parser.add_argument("--lang", default="en",
                        help="Language code (default: en)")
    args = parser.parse_args()

    country = args.country.lower()
    lang = args.lang.lower()
    today = date.today()
    print(f"Today: {today}  |  Target: {country}/{lang}")
    print("-" * 50)

    # Strategy 1: direct API endpoints
    data, source_url = try_api_endpoints(country, lang)
    strategy = "API endpoint"

    # Strategy 2: Playwright (renders JS)
    if data is None:
        print("Direct API endpoints returned no data — trying Playwright...")
        data, source_url = scrape_with_playwright(country, lang)
        strategy = "Playwright (XHR intercept)"

    # Strategy 3: HTML regex fallback
    if data is None:
        print("Playwright unavailable or returned no data — trying HTML scrape...")
        data, source_url = scrape_html_fallback(country, lang)
        strategy = "HTML regex fallback"

    if data is None:
        print("ERROR: Could not retrieve fuel surcharge data.", file=sys.stderr)
        print(
            "The MyDHL+ page is a JavaScript SPA. To run this reliably, install:\n"
            "  pip install playwright && playwright install chromium",
            file=sys.stderr,
        )
        sys.exit(1)

    print(f"Data source : {strategy}")
    print(f"Source URL  : {source_url}")

    result = parse_surcharge_data(data, today)
    if result is None:
        print("ERROR: Data retrieved but could not parse fuel surcharge.", file=sys.stderr)
        print("Raw data:", json.dumps(data, indent=2)[:500], file=sys.stderr)
        sys.exit(1)

    eff_date, rate, raw_rec = result
    print()
    print("=" * 50)
    if eff_date:
        print(f"  Effective date : {eff_date}")
    print(f"  Fuel surcharge : {rate}%")
    print("=" * 50)
    print()
    print("Raw record:", json.dumps(raw_rec, indent=2))


if __name__ == "__main__":
    main()
