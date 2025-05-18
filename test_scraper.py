#!/usr/bin/env python3
"""
Simple tests for WebScraper
"""

from scraper import WebScraper
from output import OutputManager
import os
import tempfile


def test_basic_scraping():
    """Test basic scraping functionality"""
    scraper = WebScraper()
    
    # Test with a simple HTML string
    test_html = """
    <html>
        <head><title>Test Page</title></head>
        <body>
            <h1>Hello World</h1>
            <p>This is a test page.</p>
            <a href="https://example.com">Example</a>
            <a href="/relative">Relative Link</a>
            <img src="https://example.com/image.jpg" alt="Test Image">
        </body>
    </html>
    """
    
    soup = scraper.parse_html(test_html)
    assert soup is not None
    
    text = scraper.extract_text(soup)
    assert "Hello World" in text
    assert "This is a test page." in text
    
    links = scraper.extract_links(soup, "https://test.com")
    assert "https://example.com" in links
    assert "https://test.com/relative" in links
    
    images = scraper.extract_images(soup)
    assert "https://example.com/image.jpg" in images
    
    print("✓ Basic scraping tests passed")


def test_output_manager():
    """Test output functionality"""
    output_manager = OutputManager()
    
    test_data = {
        "url": "https://example.com",
        "text": "Sample text content",
        "links": ["https://link1.com", "https://link2.com"]
    }
    
    # Test JSON output
    with tempfile.TemporaryDirectory() as temp_dir:
        output_manager.output_dir = temp_dir
        json_file = output_manager.save_as_json(test_data, "test.json")
        assert os.path.exists(json_file)
    
    print("✓ Output manager tests passed")


if __name__ == "__main__":
    print("Running WebScraper tests...")
    test_basic_scraping()
    test_output_manager()
    print("All tests passed! ✅")