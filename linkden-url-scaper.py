import requests
from bs4 import BeautifulSoup
import urllib.parse
import time
import re
from urllib.parse import urljoin, urlparse
import json
import random
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class LinkedInScraper:
    def __init__(self):
        self.session = requests.Session()
        # Use more realistic headers and rotate user agents
        user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/121.0'
        ]
        self.session.headers.update({
            'User-Agent': random.choice(user_agents),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        })
        self.driver = None
        
    def setup_browser(self):
        """Setup undetected Chrome browser"""
        try:
            print("Setting up undetected Chrome driver...")
            
            # Randomize window size
            window_sizes = [
                (1366, 768), (1920, 1080), (1440, 900), (1536, 864), 
                (1280, 720), (1600, 900), (1024, 768), (1280, 1024)
            ]
            width, height = random.choice(window_sizes)
            
            # Create undetected Chrome driver
            options = uc.ChromeOptions()
            
            # Basic options
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--disable-gpu")
            options.add_argument(f"--window-size={width},{height}")
            options.add_argument("--start-maximized")
            
            # Additional stealth options
            options.add_argument("--disable-blink-features=AutomationControlled")
            options.add_argument("--disable-extensions")
            options.add_argument("--disable-plugins")
            options.add_argument("--disable-web-security")
            options.add_argument("--allow-running-insecure-content")
            options.add_argument("--disable-features=VizDisplayCompositor")
            options.add_argument("--disable-background-timer-throttling")
            options.add_argument("--disable-backgrounding-occluded-windows")
            options.add_argument("--disable-renderer-backgrounding")
            options.add_argument("--disable-features=TranslateUI")
            options.add_argument("--disable-ipc-flooding-protection")
            options.add_argument("--disable-hang-monitor")
            options.add_argument("--disable-prompt-on-repost")
            options.add_argument("--disable-sync")
            options.add_argument("--disable-default-apps")
            options.add_argument("--disable-component-extensions-with-background-pages")
            options.add_argument("--disable-background-networking")
            options.add_argument("--disable-client-side-phishing-detection")
            options.add_argument("--disable-sync-preferences")
            options.add_argument("--disable-translate")
            options.add_argument("--hide-scrollbars")
            options.add_argument("--mute-audio")
            options.add_argument("--no-first-run")
            options.add_argument("--disable-logging")
            options.add_argument("--disable-gpu-logging")
            options.add_argument("--silent")
            options.add_argument("--log-level=3")
            
            # Randomize user agent
            user_agents = [
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36",
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
                "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
            ]
            selected_ua = random.choice(user_agents)
            options.add_argument(f"--user-agent={selected_ua}")
            
            # Randomize language
            options.add_argument(f"--lang={random.choice(['en-US', 'en-GB', 'en-CA', 'en-AU'])}")
            
            # Create undetected Chrome driver with version detection
            self.driver = uc.Chrome(options=options, version_main=135)
            
            # Additional stealth measures
            self.driver.execute_script("""
                // Remove webdriver property
                Object.defineProperty(navigator, 'webdriver', {
                    get: () => undefined,
                });
                
                // Override plugins
                Object.defineProperty(navigator, 'plugins', {
                    get: () => [1, 2, 3, 4, 5],
                });
                
                // Override languages
                Object.defineProperty(navigator, 'languages', {
                    get: () => ['en-US', 'en'],
                });
                
                // Override platform
                Object.defineProperty(navigator, 'platform', {
                    get: () => 'Win32',
                });
                
                // Override hardware concurrency
                Object.defineProperty(navigator, 'hardwareConcurrency', {
                    get: () => 8,
                });
                
                // Override device memory
                Object.defineProperty(navigator, 'deviceMemory', {
                    get: () => 8,
                });
                
                // Override screen properties
                Object.defineProperty(screen, 'width', {
                    get: () => """ + str(width) + """,
                });
                Object.defineProperty(screen, 'height', {
                    get: () => """ + str(height) + """,
                });
                Object.defineProperty(screen, 'availWidth', {
                    get: () => """ + str(width) + """,
                });
                Object.defineProperty(screen, 'availHeight', {
                    get: () => """ + str(height - 40) + """,
                });
                Object.defineProperty(screen, 'colorDepth', {
                    get: () => 24,
                });
                Object.defineProperty(screen, 'pixelDepth', {
                    get: () => 24,
                });
                
                // Override Chrome object
                window.chrome = {
                    runtime: {},
                    loadTimes: function() {
                        return {
                            requestTime: Date.now() / 1000 - Math.random() * 1000,
                            startLoadTime: Date.now() / 1000 - Math.random() * 1000,
                            commitLoadTime: Date.now() / 1000 - Math.random() * 1000,
                            finishDocumentLoadTime: Date.now() / 1000 - Math.random() * 1000,
                            finishLoadTime: Date.now() / 1000 - Math.random() * 1000,
                            firstPaintTime: Date.now() / 1000 - Math.random() * 1000,
                            firstPaintAfterLoadTime: 0,
                            navigationType: 'Other',
                            wasFetchedViaSpdy: false,
                            wasNpnNegotiated: false,
                            npnNegotiatedProtocol: 'unknown',
                            wasAlternateProtocolAvailable: false,
                            connectionInfo: 'http/1.1'
                        };
                    }
                };
                
                // Override permissions
                Object.defineProperty(navigator, 'permissions', {
                    get: () => ({
                        query: () => Promise.resolve({ state: 'granted' }),
                    }),
                });
                
                // Override getBattery
                Object.defineProperty(navigator, 'getBattery', {
                    get: () => () => Promise.resolve({
                        charging: true,
                        chargingTime: 0,
                        dischargingTime: Infinity,
                        level: 1
                    }),
                });
                
                // Override connection
                Object.defineProperty(navigator, 'connection', {
                    get: () => ({
                        effectiveType: '4g',
                        rtt: 50,
                        downlink: 10,
                        saveData: false
                    }),
                });
            """)
            
            print("Undetected Chrome driver setup completed successfully")
            return True
        except Exception as e:
            print(f"Error setting up undetected Chrome driver: {e}")
            print("Make sure Chrome browser is installed on your system")
            return False
    
    def human_like_delay(self, min_seconds=1, max_seconds=3):
        """Add human-like random delay"""
        delay = random.uniform(min_seconds, max_seconds)
        time.sleep(delay)

    def simulate_human_behavior(self):
        """Simulate various human-like behaviors"""
        try:
            # Random mouse movements
            self.driver.execute_script("""
                // Simulate mouse movement
                const event = new MouseEvent('mousemove', {
                    'view': window,
                    'bubbles': true,
                    'cancelable': true,
                    'clientX': Math.random() * window.innerWidth,
                    'clientY': Math.random() * window.innerHeight
                });
                document.dispatchEvent(event);
            """)
            
            # Random scroll
            scroll_amount = random.randint(100, 500)
            self.driver.execute_script(f"window.scrollTo(0, {scroll_amount});")
            
            # Random pause
            time.sleep(random.uniform(0.5, 2))
            
        except Exception as e:
            pass  # Ignore errors in simulation

    def search_google_with_browser(self, query):
        """Search Google using browser automation with advanced human-like behavior"""
        try:
            print("Opening Google in browser...")
            
            # First, visit a random page to appear more human
            self.driver.get("https://www.google.com")
            self.human_like_delay(3, 6)
            
            # Simulate human behavior before searching
            self.simulate_human_behavior()
            
            # Wait for search box to be present
            wait = WebDriverWait(self.driver, 15)
            search_box = wait.until(EC.presence_of_element_located((By.NAME, "q")))
            
            # Click on search box first (human behavior)
            search_box.click()
            self.human_like_delay(0.5, 1)
            
            # Human-like typing with random delays and mistakes
            print("Typing search query...")
            search_box.clear()
            self.human_like_delay(0.5, 1)
            
            # Type character by character with random delays and occasional pauses
            for i, char in enumerate(query):
                search_box.send_keys(char)
                
                # Random pause between characters
                time.sleep(random.uniform(0.05, 0.25))
                
                # Occasionally pause longer (like thinking)
                if random.random() < 0.1:  # 10% chance
                    time.sleep(random.uniform(0.5, 1.5))
                
                # Occasionally backspace and retype (like making a mistake)
                if random.random() < 0.05 and i > 5:  # 5% chance after 5 characters
                    search_box.send_keys(Keys.BACKSPACE)
                    time.sleep(random.uniform(0.1, 0.3))
                    search_box.send_keys(char)
            
            # Pause before pressing enter (like reviewing the query)
            self.human_like_delay(1, 3)
            
            # Press Enter
            search_box.send_keys(Keys.RETURN)
            
            # Wait for results to load
            print("Waiting for search results to load...")
            self.human_like_delay(4, 8)
            
            # Simulate human behavior while waiting
            self.simulate_human_behavior()
            
            # Check if we got search results or a challenge page
            page_title = self.driver.title
            print(f"Page title: {page_title}")
            print(f"Current URL: {self.driver.current_url}")
            print(f"Page source length: {len(self.driver.page_source)} characters")

            # Check if we're on the right page
            if "google.com/search" not in self.driver.current_url:
                print("⚠️  Not on Google search results page!")
                print(f"Current URL: {self.driver.current_url}")
            
            page_title = self.driver.title
            print(f"Page title: {page_title}")
            
            # Check for CAPTCHA or challenge pages
            if any(word in page_title.lower() for word in ["captcha", "verify", "robot", "automated", "unusual traffic", "suspicious", "blocked"]):
                print("⚠️  CAPTCHA or robot detection detected!")
                print("The browser will stay open for you to solve the CAPTCHA manually.")
                print("After solving, press Enter in this terminal to continue...")
                input("Press Enter after solving CAPTCHA...")
                self.human_like_delay(2, 4)
            
            # Check for consent/cookie pages
            elif "consent" in page_title.lower() or "cookies" in page_title.lower():
                print("Detected consent/cookie page, trying to accept...")
                try:
                    # Try multiple possible accept button selectors
                    accept_selectors = [
                        "//button[contains(text(), 'Accept')]",
                        "//button[contains(text(), 'I agree')]",
                        "//button[contains(text(), 'Accept all')]",
                        "//button[contains(text(), 'I accept')]",
                        "//div[@id='L2AGLb']",  # Google's accept button
                        "//button[@id='L2AGLb']",
                        "//button[contains(@class, 'accept')]",
                        "//div[contains(@class, 'accept')]//button"
                    ]
                    
                    for selector in accept_selectors:
                        try:
                            accept_button = self.driver.find_element(By.XPATH, selector)
                            # Simulate human click
                            self.driver.execute_script("arguments[0].click();", accept_button)
                            print("Clicked accept button")
                            self.human_like_delay(2, 4)
                            break
                        except:
                            continue
                except:
                    print("Could not find accept button, continuing...")
            
            # Simulate human browsing behavior
            self.simulate_human_behavior()
            
            # Scroll down to see more results (human behavior)
            self.driver.execute_script("window.scrollTo(0, 600);")
            self.human_like_delay(1, 2)
            
            # Scroll back up a bit
            self.driver.execute_script("window.scrollTo(0, 200);")
            self.human_like_delay(1, 2)
            
            # Get the page source
            page_source = self.driver.page_source
            print(f"Search completed. Page length: {len(page_source)} characters")
            
            # Save page source for debugging
            with open("debug_page_source.html", "w", encoding="utf-8") as f:
                f.write(page_source)
            print("Page source saved to debug_page_source.html for inspection")
            
            return page_source
            
        except Exception as e:
            print(f"Error searching Google with browser: {e}")
            return None
    
    def close_browser(self):
        """Close the browser"""
        if self.driver:
            self.driver.quit()
            print("Browser closed")
    
    def extract_linkedin_profiles(self, html_content):
        """Extract LinkedIn profile URLs and metadata from Google search results"""
        soup = BeautifulSoup(html_content, 'html.parser')
        linkedin_profiles = []
        
        print(f"HTML content length: {len(html_content)} characters")
        
        # First, try to find LinkedIn URLs using regex in the raw HTML
        linkedin_pattern = r'https?://(?:www\.)?linkedin\.com/in/[a-zA-Z0-9\-_]+/?'
        linkedin_urls = re.findall(linkedin_pattern, html_content)
        
        print(f"Found {len(linkedin_urls)} LinkedIn URLs using regex")
        
        # Also try to find URLs in href attributes
        all_links = soup.find_all('a', href=True)
        print(f"Found {len(all_links)} total links")
        
        # Debug: Show some sample links
        print("Sample links found:")
        for i, link in enumerate(all_links[:10]):
            href = link.get('href')
            print(f"  {i+1}. {href}")
        
        for link in all_links:
            href = link.get('href')
            if href and 'linkedin.com/in/' in href:
                # Clean up Google's redirect URL
                if href.startswith('/url?q='):
                    href = href.split('/url?q=')[1].split('&')[0]
                elif href.startswith('https://www.google.com/url?q='):
                    href = href.split('https://www.google.com/url?q=')[1].split('&')[0]
                elif href.startswith('/search?q='):
                    continue
                
                if 'linkedin.com/in/' in href:
                    if not href.startswith('http'):
                        href = 'https://' + href
                    
                    # Add to our list if not already present
                    if href not in linkedin_urls:
                        linkedin_urls.append(href)
                        print(f"Found new LinkedIn URL: {href}")
        
        # Remove duplicates
        unique_urls = list(set(linkedin_urls))
        print(f"Unique LinkedIn URLs found: {len(unique_urls)}")
        
        # For each LinkedIn URL, try to find associated metadata
        for url in unique_urls:
            # Find the parent container that contains this URL
            url_element = soup.find('a', href=lambda x: x and url in x)
            
            title = ""
            description = ""
            additional_info = ""
            
            if url_element:
                # Try to find title in h3 tag
                title_element = url_element.find('h3')
                if not title_element:
                    # Look in parent containers
                    parent = url_element.find_parent()
                    if parent:
                        title_element = parent.find('h3')
                if title_element:
                    title = title_element.get_text().strip()
                
                # Try to find description
                desc_element = url_element.find_parent().find('div', class_='VwiC3b')
                if not desc_element:
                    desc_element = url_element.find_parent().find('span', class_='aCOpRe')
                if desc_element:
                    description = desc_element.get_text().strip()
                
                # Try to find additional info
                info_element = url_element.find_parent().find('div', class_='YrbPuc')
                if info_element:
                    additional_info = info_element.get_text().strip()
            
            profile_data = {
                'url': url,
                'meta_title': title,
                'description': description,
                'additional_info': additional_info,
                'headings': [title] if title else []
            }
            
            linkedin_profiles.append(profile_data)
            print(f"Found LinkedIn profile: {title if title else url}")
        
        print(f"LinkedIn profiles found: {len(linkedin_profiles)}")
        return linkedin_profiles
    
    def get_page_metadata(self, url):
        """Extract meta title and headings from a LinkedIn profile page"""
        try:
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract meta title
            meta_title = ""
            title_tag = soup.find('title')
            if title_tag:
                meta_title = title_tag.get_text().strip()
            
            # Extract headings (h1, h2, h3)
            headings = []
            for tag in soup.find_all(['h1', 'h2', 'h3']):
                heading_text = tag.get_text().strip()
                if heading_text and heading_text not in headings:
                    headings.append(heading_text)
            
            return {
                'url': url,
                'meta_title': meta_title,
                'headings': headings
            }
            
        except requests.RequestException as e:
            print(f"Error fetching {url}: {e}")
            return {
                'url': url,
                'meta_title': 'Error loading page',
                'headings': []
            }
    
    def get_sample_linkedin_urls(self):
        """Get some sample LinkedIn URLs for testing when search fails"""
        # These are some sample LinkedIn URLs for testing
        sample_urls = [
            "https://www.linkedin.com/in/sample-ceo-apm/",
            "https://www.linkedin.com/in/sample-managing-director/",
            "https://www.linkedin.com/in/sample-sales-director/",
            "https://www.linkedin.com/in/sample-marketing-director/",
            "https://www.linkedin.com/in/sample-founder-apm/"
        ]
        return sample_urls

    def scrape_linkedin_profiles(self):
        """Main method to scrape LinkedIn profiles using browser automation"""
        # Construct the search query
        search_query = '(CEO OR COO OR "Chief Operating Officer" OR "Managing Director" OR "Sales Director" OR "Head of Sales" OR "Marketing Director" OR Founder OR "Co-Founder" OR Partner OR "Managing Partner") "APM - Australian Property Management" site:linkedin.com/in'
        
        print(f"Searching for: {search_query}")
        print("=" * 80)
        
        # Setup browser
        if not self.setup_browser():
            print("Failed to setup browser")
            return
        
        try:
            # Search Google using browser
            html_content = self.search_google_with_browser(search_query)
            if not html_content:
                print("Failed to search Google with browser")
                return
            
            # Extract LinkedIn profiles with metadata
            linkedin_profiles = self.extract_linkedin_profiles(html_content)
            
            if not linkedin_profiles:
                print("No LinkedIn profiles found in search results")
                print("You can manually search for LinkedIn profiles and add them to the script.")
                
                # Ask user if they want to use sample URLs for testing
                use_samples = input("Would you like to use sample LinkedIn URLs for testing? (y/n): ").lower().strip()
                if use_samples == 'y':
                    sample_urls = self.get_sample_linkedin_urls()
                    linkedin_profiles = [{'url': url, 'meta_title': 'Sample Profile', 'description': '', 'additional_info': '', 'headings': []} for url in sample_urls]
                    print(f"Using {len(linkedin_profiles)} sample URLs for testing")
                else:
                    return
            
            print(f"Found {len(linkedin_profiles)} LinkedIn profiles")
            print("=" * 80)
            
            return linkedin_profiles
            
        finally:
            # Always close the browser
            self.close_browser()
    
    def display_results(self, results):
        """Display the scraping results in a formatted way"""
        print("\n" + "=" * 80)
        print("SCRAPING RESULTS")
        print("=" * 80)
        
        for i, result in enumerate(results, 1):
            print(f"\n{i}. URL: {result['url']}")
            print(f"   Title: {result['meta_title']}")
            if result['description']:
                print(f"   Description: {result['description']}")
            if result['additional_info']:
                print(f"   Additional Info: {result['additional_info']}")
            if result['headings']:
                print(f"   Headings:")
                for heading in result['headings']:
                    print(f"     - {heading}")
            print("-" * 60)
    
    def save_results(self, results, filename="linkedin_scraping_results.json"):
        """Save results to a JSON file"""
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(results, f, indent=2, ensure_ascii=False)
            print(f"\nResults saved to {filename}")
        except Exception as e:
            print(f"Error saving results: {e}")

def main():
    """Main function to run the scraper"""
    scraper = LinkedInScraper()
    
    print("LinkedIn Profile Scraper")
    print("Searching for APM - Australian Property Management executives...")
    print("=" * 80)
    
    # Scrape LinkedIn profiles
    results = scraper.scrape_linkedin_profiles()
    
    if results:
        # Display results
        scraper.display_results(results)
        
        # Save results to file
        scraper.save_results(results)
        
        print(f"\nScraping completed! Found {len(results)} profiles.")
    else:
        print("No results found.")

if __name__ == "__main__":
    main()
