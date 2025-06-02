import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse, urldefrag

BASE_URL = "https://www.pdx.edu/"
OUTPUT_DIR = "./local_data/html"
VISITED = set()
MAX_PAGES = 200

def is_valid_url(url):
    parsed = urlparse(url)
    return parsed.netloc == "www.pdx.edu" and parsed.scheme in ["http", "https"]

def sanitize_filename(url):
    path = urlparse(url).path.strip("/")
    filename = path.replace("/", "_") or "index"
    return f"{filename}.html"

def save_page(url, content):
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    filename = sanitize_filename(url)
    path = os.path.join(OUTPUT_DIR, filename)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Saved: {url} → {filename}")

def normalize_url(url):
    url, _ = urldefrag(url)  # remove fragment
    return url.strip("/")

def scrape(url):
    global MAX_PAGES
    url = normalize_url(url)
    if url in VISITED or MAX_PAGES <= 0:
        return
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200 and "text/html" in response.headers.get("Content-Type", ""):
            VISITED.add(url)
            soup = BeautifulSoup(response.text, "html.parser")
            save_page(url, response.text)
            MAX_PAGES -= 1

            for link in soup.find_all("a", href=True):
                full_url = urljoin(BASE_URL, link["href"])
                full_url = normalize_url(full_url)
                if is_valid_url(full_url) and full_url not in VISITED:
                    scrape(full_url)
    except Exception as e:
        print(f"Failed to scrape {url}: {e}")

if __name__ == "__main__":
    print("Starting scrape of pdx.edu ...")
    scrape(BASE_URL)
    print(f"\n Done Scraping. Total pages scraped: {len(VISITED)}")