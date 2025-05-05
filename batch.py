#!/usr/bin/env python3
"""
Batch processing module for WebScraper
"""

import csv
import json
import os
import time
from datetime import datetime
from scraper import WebScraper
from output import OutputManager
from config import Config


class BatchProcessor:
    def __init__(self, config_file=None):
        self.config = Config(config_file)
        self.scraper = WebScraper(delay=self.config.get('delay', 1.0))
        self.output_manager = OutputManager(self.config.get('output_dir', 'output'))
        self.results = []
        
    def load_urls_from_file(self, filename):
        """Load URLs from text file (one per line)"""
        urls = []
        try:
            with open(filename, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#'):
                        urls.append(line)
        except IOError as e:
            print(f"Error reading file {filename}: {e}")
        
        return urls
    
    def load_urls_from_csv(self, filename, url_column='url'):
        """Load URLs from CSV file"""
        urls = []
        try:
            with open(filename, 'r') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    if url_column in row and row[url_column].strip():
                        urls.append(row[url_column].strip())
        except (IOError, KeyError) as e:
            print(f"Error reading CSV file {filename}: {e}")
        
        return urls
    
    def process_urls(self, urls, extract_type='all'):
        """Process a list of URLs"""
        total = len(urls)
        print(f"Processing {total} URLs...")
        
        for i, url in enumerate(urls, 1):
            print(f"[{i}/{total}] Processing: {url}")
            
            try:
                html_content = self.scraper.scrape_url(url)
                if not html_content:
                    self.results.append({
                        'url': url,
                        'status': 'failed',
                        'error': 'Failed to fetch content',
                        'timestamp': datetime.now().isoformat()
                    })
                    continue
                
                soup = self.scraper.parse_html(html_content)
                if not soup:
                    self.results.append({
                        'url': url,
                        'status': 'failed', 
                        'error': 'Failed to parse HTML',
                        'timestamp': datetime.now().isoformat()
                    })
                    continue
                
                result = {
                    'url': url,
                    'status': 'success',
                    'timestamp': datetime.now().isoformat()
                }
                
                if extract_type in ['all', 'text']:
                    result['text'] = self.scraper.extract_text(soup)
                
                if extract_type in ['all', 'links']:
                    result['links'] = self.scraper.extract_links(soup, url)
                    result['link_count'] = len(result.get('links', []))
                
                if extract_type in ['all', 'images']:
                    result['images'] = self.scraper.extract_images(soup, url)
                    result['image_count'] = len(result.get('images', []))
                
                self.results.append(result)
                
            except Exception as e:
                print(f"Error processing {url}: {e}")
                self.results.append({
                    'url': url,
                    'status': 'failed',
                    'error': str(e),
                    'timestamp': datetime.now().isoformat()
                })
            
            if i < total:
                time.sleep(self.config.get('delay', 1.0))
        
        print(f"Batch processing completed. {len([r for r in self.results if r['status'] == 'success'])} successful, {len([r for r in self.results if r['status'] == 'failed'])} failed.")
        return self.results
    
    def save_results(self, format='json', filename=None):
        """Save batch processing results"""
        if not self.results:
            print("No results to save")
            return
        
        if not filename:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"batch_results_{timestamp}"
        
        if format == 'json':
            return self.output_manager.save_as_json(self.results, f"{filename}.json")
        elif format == 'csv':
            return self.output_manager.save_as_csv(self.results, f"{filename}.csv")
        elif format == 'txt':
            text_data = []
            for result in self.results:
                text_data.append(f"URL: {result['url']}")
                text_data.append(f"Status: {result['status']}")
                if result['status'] == 'success':
                    if 'text' in result:
                        text_data.append(f"Text: {result['text'][:200]}...")
                    if 'link_count' in result:
                        text_data.append(f"Links: {result['link_count']}")
                else:
                    text_data.append(f"Error: {result.get('error', 'Unknown')}")
                text_data.append("-" * 50)
            
            return self.output_manager.save_as_txt('\n'.join(text_data), f"{filename}.txt")


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='Batch WebScraper')
    parser.add_argument('input_file', help='File containing URLs (txt or csv)')
    parser.add_argument('-c', '--config', help='Configuration file')
    parser.add_argument('-o', '--output', choices=['json', 'csv', 'txt'], 
                        default='json', help='Output format')
    parser.add_argument('-e', '--extract', choices=['all', 'text', 'links', 'images'],
                        default='all', help='What to extract')
    parser.add_argument('-f', '--filename', help='Output filename (without extension)')
    
    args = parser.parse_args()
    
    processor = BatchProcessor(args.config)
    
    if args.input_file.endswith('.csv'):
        urls = processor.load_urls_from_csv(args.input_file)
    else:
        urls = processor.load_urls_from_file(args.input_file)
    
    if not urls:
        print("No URLs found in input file")
        return
    
    processor.process_urls(urls, args.extract)
    processor.save_results(args.output, args.filename)


if __name__ == "__main__":
    main()