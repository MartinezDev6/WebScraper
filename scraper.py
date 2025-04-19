#!/usr/bin/env python3
"""
WebScraper - A simple web scraping tool
"""

import requests
from bs4 import BeautifulSoup
import time
from urllib.parse import urljoin, urlparse


class WebScraper:
    def __init__(self, delay=1):
        self.session = requests.Session()
        self.delay = delay
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        
    def scrape_url(self, url):
        """Scrape a single URL and return content"""
        try:
            if self.delay > 0:
                time.sleep(self.delay)
            
            response = self.session.get(url, timeout=30)
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
        
        for script in soup(["script", "style"]):
            script.decompose()
        
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
                links.append(urljoin(base_url, href))
            elif base_url and href and not href.startswith('#'):
                links.append(urljoin(base_url, href))
        
        return list(set(links))  # Remove duplicates
    
    def extract_images(self, soup, base_url=""):
        """Extract all images from parsed HTML"""
        if not soup:
            return []
        
        images = []
        for img in soup.find_all('img', src=True):
            src = img['src']
            if src.startswith('http'):
                images.append(src)
            elif base_url and src.startswith('/'):
                images.append(urljoin(base_url, src))
            elif base_url and src:
                images.append(urljoin(base_url, src))
        
        return list(set(images))


if __name__ == "__main__":
    scraper = WebScraper()
    print("WebScraper initialized")