# WebScraper

A simple Python web scraping tool for extracting data from websites.

## Features
- Extract text content from web pages
- Extract all links from pages
- Extract images from pages
- Support multiple output formats (JSON, CSV, TXT)
- Command line interface
- Configurable request delays
- User-agent rotation

## Installation

```bash
pip install -r requirements.txt
```

## Usage

### Command Line Interface

Basic usage:
```bash
python cli.py https://example.com
```

Extract only text:
```bash
python cli.py https://example.com --text-only -o txt
```

Extract only links as CSV:
```bash
python cli.py https://example.com --links-only -o csv
```

Custom output file and delay:
```bash
python cli.py https://example.com -f my_data.json -d 2.0
```

### Python Module

```python
from scraper import WebScraper
from output import OutputManager

scraper = WebScraper(delay=1.5)
output_manager = OutputManager()

html = scraper.scrape_url('https://example.com')
soup = scraper.parse_html(html)

text = scraper.extract_text(soup)
links = scraper.extract_links(soup, 'https://example.com')

data = {'text': text, 'links': links}
output_manager.save_as_json(data)
```

## Options

- `-o, --output`: Output format (json, csv, txt)
- `-f, --file`: Custom output filename  
- `-d, --delay`: Delay between requests in seconds
- `--text-only`: Extract only text content
- `--links-only`: Extract only links