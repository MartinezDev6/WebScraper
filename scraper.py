#!/usr/bin/env python3
"""
WebScraper - A simple web scraping tool
"""

import requests
from bs4 import BeautifulSoup
import time


class WebScraper:
    def __init__(self, delay=1):
        self.session = requests.Session()
        self.delay = delay
        
    def scrape_url(self, url):
        """Scrape a single URL and return content"""
        try:
            response = self.session.get(url)
            response.raise_for_status()
            return response.text
        except requests.RequestException as e:
            print(f"Error scraping {url}: {e}")
            return None
    
    def parse_html(self, html_content):
        """Parse HTML content and return BeautifulSoup object"""
        if not html_content:
            return None
        return BeautifulSoup(html_content, 'lxml')
    
    def extract_text(self, soup):
        """Extract all text from parsed HTML"""
        if not soup:
            return ""
        return soup.get_text().strip()
    
    def extract_links(self, soup, base_url=""):
        """Extract all links from parsed HTML"""
        if not soup:
            return []
        
        links = []
        for link in soup.find_all('a', href=True):
            href = link['href']
            if href.startswith('http'):
                links.append(href)
            elif base_url and href.startswith('/'):
                links.append(base_url + href)
        
        return links


if __name__ == "__main__":
    scraper = WebScraper()
    print("WebScraper initialized")