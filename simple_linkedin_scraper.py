import requests
from bs4 import BeautifulSoup
import urllib.parse
import time
import re
import json
import random

class SimpleLinkedInScraper:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        })
    
    def search_google(self, query):
        """Search Google for LinkedIn profiles"""
        search_url = f"https://www.google.com/search?q={urllib.parse.quote_plus(query)}&num=10"
        
        try:
            print(f"Searching: {query}")
            response = self.session.get(search_url)
            response.raise_for_status()
            return response.text
        except requests.RequestException as e:
            print(f"Error searching Google: {e}")
            return None
    
    def extract_linkedin_profiles(self, html_content):
        """Extract LinkedIn profiles from Google search results"""
        soup = BeautifulSoup(html_content, 'html.parser')
        profiles = []
        
        # Find all links
        for link in soup.find_all('a', href=True):
            href = link.get('href')
            
            if href and 'linkedin.com/in/' in href:
                # Clean up Google's redirect URL
                if href.startswith('/url?q='):
                    href = href.split('/url?q=')[1].split('&')[0]
                elif href.startswith('https://www.google.com/url?q='):
                    href = href.split('https://www.google.com/url?q=')[1].split('&')[0]
                
                if 'linkedin.com/in/' in href and not href.startswith('http'):
                    href = 'https://' + href
                
                # Extract title from the link or nearby elements
                title = ""
                title_element = link.find('h3')
                if not title_element:
                    title_element = link.find_parent().find('h3')
                if title_element:
                    title = title_element.get_text().strip()
                
                # Extract description from nearby elements
                description = ""
                desc_element = link.find_parent().find('div', class_='VwiC3b')
                if not desc_element:
                    desc_element = link.find_parent().find('span', class_='aCOpRe')
                if desc_element:
                    description = desc_element.get_text().strip()
                
                # Extract additional info
                additional_info = ""
                info_element = link.find_parent().find('div', class_='YrbPuc')
                if info_element:
                    additional_info = info_element.get_text().strip()
                
                profile = {
                    'url': href,
                    'title': title,
                    'description': description,
                    'additional_info': additional_info
                }
                
                # Avoid duplicates
                if not any(p['url'] == href for p in profiles):
                    profiles.append(profile)
                    print(f"Found: {title if title else href}")
        
        return profiles
    
    def scrape_linkedin_profiles(self):
        """Main scraping method"""
        search_query = '(CEO OR COO OR "Chief Operating Officer" OR "Managing Director" OR "Sales Director" OR "Head of Sales" OR "Marketing Director" OR Founder OR "Co-Founder" OR Partner OR "Managing Partner") "APM - Australian Property Management" site:linkedin.com/in'
        
        print("LinkedIn Profile Scraper")
        print("=" * 80)
        
        # Search Google
        html_content = self.search_google(search_query)
        if not html_content:
            print("Failed to search Google")
            return []
        
        # Extract profiles
        profiles = self.extract_linkedin_profiles(html_content)
        
        if not profiles:
            print("No LinkedIn profiles found")
            return []
        
        print(f"\nFound {len(profiles)} LinkedIn profiles")
        print("=" * 80)
        
        return profiles
    
    def display_results(self, profiles):
        """Display results"""
        for i, profile in enumerate(profiles, 1):
            print(f"\n{i}. {profile['url']}")
            if profile['title']:
                print(f"   Title: {profile['title']}")
            if profile['description']:
                print(f"   Description: {profile['description']}")
            if profile['additional_info']:
                print(f"   Additional Info: {profile['additional_info']}")
            print("-" * 60)
    
    def save_results(self, profiles, filename="linkedin_profiles.json"):
        """Save results to JSON file"""
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(profiles, f, indent=2, ensure_ascii=False)
        print(f"\nResults saved to {filename}")

def main():
    scraper = SimpleLinkedInScraper()
    profiles = scraper.scrape_linkedin_profiles()
    
    if profiles:
        scraper.display_results(profiles)
        scraper.save_results(profiles)
    else:
        print("No profiles found")

if __name__ == "__main__":
    main()
