#!/usr/bin/env python3
"""
Command line interface for WebScraper
"""

import argparse
import sys
from scraper import WebScraper
from output import OutputManager


def print_banner():
    print("WebScraper v1.0.0")
    print("A simple tool for web scraping")
    print("-" * 30)


def main():
    parser = argparse.ArgumentParser(description='WebScraper - Extract data from websites')
    parser.add_argument('url', help='URL to scrape')
    parser.add_argument('-o', '--output', choices=['json', 'csv', 'txt'], 
                        default='json', help='Output format (default: json)')
    parser.add_argument('-f', '--file', help='Output filename')
    parser.add_argument('-d', '--delay', type=float, default=1.0,
                        help='Delay between requests in seconds (default: 1.0)')
    parser.add_argument('--text-only', action='store_true',
                        help='Extract only text content')
    parser.add_argument('--links-only', action='store_true', 
                        help='Extract only links')
    parser.add_argument('--quiet', action='store_true',
                        help='Suppress banner and verbose output')
    
    args = parser.parse_args()
    
    if not args.quiet:
        print_banner()
    
    scraper = WebScraper(delay=args.delay)
    output_manager = OutputManager()
    
    if not args.quiet:
        print(f"Scraping {args.url}...")
    
    html_content = scraper.scrape_url(args.url)
    if not html_content:
        print("Failed to scrape URL")
        sys.exit(1)
    
    soup = scraper.parse_html(html_content)
    if not soup:
        print("Failed to parse HTML")
        sys.exit(1)
    
    if args.text_only:
        data = scraper.extract_text(soup)
        if args.output == 'txt':
            output_manager.save_as_txt(data, args.file)
        else:
            output_manager.save_as_json({'text': data}, args.file)
    
    elif args.links_only:
        data = scraper.extract_links(soup, args.url)
        if args.output == 'json':
            output_manager.save_as_json({'links': data}, args.file)
        elif args.output == 'csv':
            csv_data = [{'url': link} for link in data]
            output_manager.save_as_csv(csv_data, args.file)
        else:
            output_manager.save_as_txt(data, args.file)
    
    else:
        text = scraper.extract_text(soup)
        links = scraper.extract_links(soup, args.url)
        
        data = {
            'url': args.url,
            'text': text,
            'links': links,
            'link_count': len(links)
        }
        
        if args.output == 'json':
            output_manager.save_as_json(data, args.file)
        elif args.output == 'csv':
            csv_data = [data]
            output_manager.save_as_csv(csv_data, args.file)
        else:
            output_manager.save_as_txt(f"URL: {data['url']}\n\nText:\n{data['text']}\n\nLinks ({data['link_count']}):\n" + '\n'.join(data['links']), args.file)
    
    if not args.quiet:
        print("Scraping completed!")


if __name__ == "__main__":
    main()