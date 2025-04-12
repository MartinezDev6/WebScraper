"""
Output formatting module for WebScraper
"""

import json
import csv
import os
from datetime import datetime


class OutputManager:
    def __init__(self, output_dir="output"):
        self.output_dir = output_dir
        self.create_output_dir()
    
    def create_output_dir(self):
        """Create output directory if it doesn't exist"""
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
    
    def save_as_json(self, data, filename=None):
        """Save data as JSON file"""
        if not filename:
            filename = f"scraped_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        filepath = os.path.join(self.output_dir, filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        print(f"Data saved to {filepath}")
        return filepath
    
    def save_as_csv(self, data, filename=None, fieldnames=None):
        """Save data as CSV file"""
        if not filename:
            filename = f"scraped_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        
        filepath = os.path.join(self.output_dir, filename)
        
        if isinstance(data, list) and data:
            if not fieldnames:
                fieldnames = data[0].keys() if isinstance(data[0], dict) else ['data']
            
            with open(filepath, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                for item in data:
                    if isinstance(item, dict):
                        writer.writerow(item)
                    else:
                        writer.writerow({'data': item})
        
        print(f"Data saved to {filepath}")
        return filepath
    
    def save_as_txt(self, data, filename=None):
        """Save data as plain text file"""
        if not filename:
            filename = f"scraped_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        
        filepath = os.path.join(self.output_dir, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            if isinstance(data, (list, tuple)):
                for item in data:
                    f.write(f"{item}\n")
            else:
                f.write(str(data))
        
        print(f"Data saved to {filepath}")
        return filepath