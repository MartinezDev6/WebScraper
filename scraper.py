#!/usr/bin/env python3
"""
WebScraper - A simple web scraping tool
"""

import requests
from bs4 import BeautifulSoup


class WebScraper:
    def __init__(self):
        self.session = requests.Session()
        
    def scrape_url(self, url):
        """Scrape a single URL and return content"""
        try:
            response = self.session.get(url)
            response.raise_for_status()
            return response.text
        except requests.RequestException as e:
            print(f"Error scraping {url}: {e}")
            return None


if __name__ == "__main__":
    scraper = WebScraper()
    print("WebScraper initialized")