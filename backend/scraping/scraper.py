import requests
from bs4 import BeautifulSoup

def scrape_text_from_url(url: str) -> str:
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        return soup.get_text()
    except Exception as e:
        return f"Error scraping URL: {str(e)}"

# Example usage
if __name__ == "__main__":
    test_url = "https://docs.google.com/document/d/knowledge_base.json/pub"
    content = scrape_text_from_url(test_url)
    print(content[:1000])  # Print first 1000 characters of scraped text
