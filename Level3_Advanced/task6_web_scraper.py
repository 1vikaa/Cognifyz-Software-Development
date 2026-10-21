"""
Cognifyz Technologies - Software Development Internship
Level 3 - Task 6: Interactive web scraping

Uses requests + BeautifulSoup to scrape two practice websites built
for scraping and shows the results in neat tables:
  1. quotes.toscrape.com  - quotes, authors, tags (filter by tag)
  2. books.toscrape.com   - book titles, prices, ratings, stock
  3. Any URL              - page title, headings and links

Install:  pip install requests beautifulsoup4
"""

import csv
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

HEADERS = {"User-Agent": "Mozilla/5.0 (Cognifyz internship scraper)"}
RATINGS = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}


def fetch(url):
    """Download a page and return parsed HTML, or None on failure."""
    try:
        response = requests.get(url, headers=HEADERS, timeout=15)
        response.raise_for_status()
        return BeautifulSoup(response.text, "html.parser")
    except requests.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return None


def scrape_quotes(tag=None, max_pages=2):
    base = "https://quotes.toscrape.com"
    url = f"{base}/tag/{tag}/" if tag else base + "/"
    quotes = []
    for _ in range(max_pages):
        soup = fetch(url)
        if soup is None:
            break
        for q in soup.select("div.quote"):
            quotes.append({
                "quote": q.select_one("span.text").get_text(strip=True),
                "author": q.select_one("small.author").get_text(strip=True),
                "tags": ", ".join(t.get_text() for t in q.select("a.tag")),
            })
        next_link = soup.select_one("li.next a")
        if not next_link:
            break
        url = urljoin(url, next_link["href"])
    return quotes


def scrape_books(max_pages=1):
    url = "https://books.toscrape.com/catalogue/page-1.html"
    books = []
    for _ in range(max_pages):
        soup = fetch(url)
        if soup is None:
            break
        for b in soup.select("article.product_pod"):
            rating_word = b.select_one("p.star-rating")["class"][1]
            books.append({
                "title": b.select_one("h3 a")["title"],
                "price": b.select_one("p.price_color").get_text(strip=True).replace("Â", ""),
                "rating": "*" * RATINGS.get(rating_word, 0),
                "stock": b.select_one("p.availability").get_text(strip=True),
            })
        next_link = soup.select_one("li.next a")
        if not next_link:
            break
        url = urljoin(url, next_link["href"])
    return books


def scrape_any(url):
    if not url.startswith(("http://", "https://")):
        url = "https://" + url
    soup = fetch(url)
    if soup is None:
        return None
    title = soup.title.get_text(strip=True) if soup.title else "(no title)"
    headings = [h.get_text(strip=True) for h in soup.select("h1, h2, h3") if h.get_text(strip=True)]
    links = []
    for a in soup.select("a[href]"):
        text = a.get_text(strip=True)
        if text:
            links.append({"text": text, "url": urljoin(url, a["href"])})
    return {"title": title, "headings": headings, "links": links}


# ---------------- Presentation ----------------

def shorten(text, width):
    return text if len(text) <= width else text[:width - 3] + "..."


def print_table(rows, columns):
    """columns = list of (key, header, width)."""
    if not rows:
        print("No data found.")
        return
    header = " | ".join(h.ljust(w) for _, h, w in columns)
    print("\n" + header)
    print("-" * len(header))
    for row in rows:
        print(" | ".join(shorten(str(row[k]), w).ljust(w) for k, _, w in columns))
    print(f"\n{len(rows)} result(s).")


def offer_csv(rows, default_name):
    if not rows:
        return
    if input("Save results to CSV? (y/n): ").strip().lower() != "y":
        return
    name = input(f"File name [{default_name}]: ").strip() or default_name
    try:
        with open(name, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=rows[0].keys())
            writer.writeheader()
            writer.writerows(rows)
        print(f"Saved to {name}")
    except OSError as e:
        print(f"Could not save file: {e}")


def ask_pages(default):
    value = input(f"How many pages to scrape? [{default}]: ").strip()
    return int(value) if value.isdigit() and int(value) > 0 else default


def main():
    while True:
        print("""
========== INTERACTIVE WEB SCRAPER ==========
 1. Quotes  (quotes.toscrape.com)
 2. Books   (books.toscrape.com)
 3. Any website (title, headings, links)
 0. Exit
=============================================""")
        choice = input("Choose an option: ").strip()

        if choice == "1":
            tag = input("Filter by tag (e.g. love, life, humor) or Enter for all: ").strip().lower()
            print("Scraping quotes...")
            rows = scrape_quotes(tag or None, ask_pages(2))
            print_table(rows, [("quote", "Quote", 60), ("author", "Author", 20), ("tags", "Tags", 30)])
            offer_csv(rows, "quotes.csv")

        elif choice == "2":
            print("Scraping books...")
            rows = scrape_books(ask_pages(1))
            sort = input("Sort by (1) price  (2) rating  (Enter) none: ").strip()
            if sort == "1":
                rows.sort(key=lambda r: float(r["price"].lstrip("£")))
            elif sort == "2":
                rows.sort(key=lambda r: len(r["rating"]), reverse=True)
            print_table(rows, [("title", "Title", 45), ("price", "Price", 8),
                               ("rating", "Rating", 6), ("stock", "Stock", 10)])
            offer_csv(rows, "books.csv")

        elif choice == "3":
            url = input("Enter URL: ").strip()
            data = scrape_any(url)
            if data:
                print(f"\nPage title: {data['title']}")
                print(f"\nHeadings ({len(data['headings'])}):")
                for h in data["headings"][:15]:
                    print(f"  - {shorten(h, 80)}")
                print_table(data["links"][:20], [("text", "Link text", 35), ("url", "URL", 60)])
                offer_csv(data["links"], "links.csv")

        elif choice == "0":
            print("Goodbye!")
            break
        else:
            print("Invalid option.")


if __name__ == "__main__":
    main()
