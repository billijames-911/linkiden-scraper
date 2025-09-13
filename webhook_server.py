from flask import Flask, request, jsonify
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
import logging
from datetime import datetime
import threading
import queue
import os

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = Flask(__name__)

class LinkedInWebhookScraper:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        })
        self.driver = None
        self.driver_lock = threading.Lock()
        
    def setup_browser(self):
        """Setup undetected Chrome browser in headless mode for Render"""
        try:
            logger.info("Setting up undetected Chrome driver in headless mode...")
            
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
            
            # HEADLESS MODE - Essential for Render
            options.add_argument("--headless")
            options.add_argument("--disable-web-security")
            options.add_argument("--disable-features=VizDisplayCompositor")
            
            # Additional stealth options
            options.add_argument("--disable-blink-features=AutomationControlled")
            options.add_argument("--disable-extensions")
            options.add_argument("--disable-plugins")
            options.add_argument("--allow-running-insecure-content")
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
            
            logger.info("Undetected Chrome driver setup completed successfully in headless mode")
            return True
        except Exception as e:
            logger.error(f"Error setting up undetected Chrome driver: {e}")
            return False
    
    def human_like_delay(self, min_seconds=1, max_seconds=3):
        """Add human-like random delay"""
        delay = random.uniform(min_seconds, max_seconds)
        time.sleep(delay)

    def search_google_with_browser(self, query):
        """Search Google using browser automation with advanced human-like behavior"""
        try:
            logger.info(f"Searching Google for: {query}")
            
            # First, visit a random page to appear more human
            self.driver.get("https://www.google.com")
            self.human_like_delay(3, 6)
            
            # Wait for search box to be present
            wait = WebDriverWait(self.driver, 15)
            search_box = wait.until(EC.presence_of_element_located((By.NAME, "q")))
            
            # Click on search box first (human behavior)
            search_box.click()
            self.human_like_delay(0.5, 1)
            
            # Human-like typing with random delays and mistakes
            logger.info("Typing search query...")
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
            logger.info("Waiting for search results to load...")
            self.human_like_delay(4, 8)
            
            # Check if we got search results or a challenge page
            page_title = self.driver.title
            logger.info(f"Page title: {page_title}")
            
            # Check for CAPTCHA or challenge pages
            if any(word in page_title.lower() for word in ["captcha", "verify", "robot", "automated", "unusual traffic", "suspicious", "blocked"]):
                logger.warning("CAPTCHA or robot detection detected!")
                return None
            
            # Check for consent/cookie pages
            elif "consent" in page_title.lower() or "cookies" in page_title.lower():
                logger.info("Detected consent/cookie page, trying to accept...")
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
                            logger.info("Clicked accept button")
                            self.human_like_delay(2, 4)
                            break
                        except:
                            continue
                except:
                    logger.warning("Could not find accept button, continuing...")
            
            # Scroll down to see more results (human behavior)
            self.driver.execute_script("window.scrollTo(0, 600);")
            self.human_like_delay(1, 2)
            
            # Scroll back up a bit
            self.driver.execute_script("window.scrollTo(0, 200);")
            self.human_like_delay(1, 2)
            
            # Get the page source
            page_source = self.driver.page_source
            logger.info(f"Search completed. Page length: {len(page_source)} characters")
            
            return page_source
            
        except Exception as e:
            logger.error(f"Error searching Google with browser: {e}")
            return None
    
    def extract_linkedin_profiles(self, html_content):
        """Extract LinkedIn profile URLs and metadata from Google search results"""
        soup = BeautifulSoup(html_content, 'html.parser')
        linkedin_profiles = []
        
        logger.info(f"HTML content length: {len(html_content)} characters")
        
        # First, try to find LinkedIn URLs using regex in the raw HTML
        linkedin_pattern = r'https?://(?:www\.)?linkedin\.com/in/[a-zA-Z0-9\-_]+/?'
        linkedin_urls = re.findall(linkedin_pattern, html_content)
        
        logger.info(f"Found {len(linkedin_urls)} LinkedIn URLs using regex")
        
        # Also try to find URLs in href attributes
        all_links = soup.find_all('a', href=True)
        logger.info(f"Found {len(all_links)} total links")
        
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
                        logger.info(f"Found new LinkedIn URL: {href}")
        
        # Remove duplicates
        unique_urls = list(set(linkedin_urls))
        logger.info(f"Unique LinkedIn URLs found: {len(unique_urls)}")
        
        # For each LinkedIn URL, try to find associated metadata
        for url in unique_urls:
            logger.info(f"Processing URL: {url}")
            
            # Find the parent container that contains this URL
            url_element = soup.find('a', href=lambda x: x and url in x)
            
            title = ""
            description = ""
            additional_info = ""
            
            if url_element:
                logger.info(f"Found URL element for: {url}")
                
                # Try to find title in h3 tag
                title_element = url_element.find('h3')
                if not title_element:
                    # Look in parent containers
                    parent = url_element.find_parent()
                    if parent:
                        title_element = parent.find('h3')
                        if not title_element:
                            # Try other parent levels
                            grandparent = parent.find_parent()
                            if grandparent:
                                title_element = grandparent.find('h3')
                
                if title_element:
                    title = title_element.get_text().strip()
                    logger.info(f"Found title: {title}")
                
                # Try to find description
                desc_element = url_element.find_parent().find('div', class_='VwiC3b')
                if not desc_element:
                    desc_element = url_element.find_parent().find('span', class_='aCOpRe')
                if not desc_element:
                    desc_element = url_element.find_parent().find('div', class_='yXK7lf')
                if desc_element:
                    description = desc_element.get_text().strip()
                    logger.info(f"Found description: {description[:100]}...")
                
                # Try to find additional info
                info_element = url_element.find_parent().find('div', class_='YrbPuc')
                if info_element:
                    additional_info = info_element.get_text().strip()
                    logger.info(f"Found additional info: {additional_info}")
            else:
                logger.warning(f"Could not find URL element for: {url}")
            
            profile_data = {
                'url': url,
                'meta_title': title,
                'description': description,
                'additional_info': additional_info,
                'headings': [title] if title else []
            }
            
            linkedin_profiles.append(profile_data)
            logger.info(f"Added profile: {title if title else url}")
        
        logger.info(f"Total LinkedIn profiles found: {len(linkedin_profiles)}")
        return linkedin_profiles
    
    def scrape_linkedin_profiles_fallback(self, search_query):
        """Fallback method using requests with different approach"""
        try:
            logger.info("Trying fallback method with requests...")
            
            # Use different search engines or approaches
            search_urls = [
                f"https://www.google.com/search?q={urllib.parse.quote(search_query)}",
                f"https://www.bing.com/search?q={urllib.parse.quote(search_query)}",
                f"https://duckduckgo.com/?q={urllib.parse.quote(search_query)}"
            ]
            
            for search_url in search_urls:
                try:
                    logger.info(f"Trying search URL: {search_url}")
                    
                    # Use different headers for each attempt
                    headers = {
                        'User-Agent': random.choice([
                            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
                        ]),
                        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                        'Accept-Language': 'en-US,en;q=0.5',
                        'Accept-Encoding': 'gzip, deflate',
                        'Connection': 'keep-alive',
                        'Upgrade-Insecure-Requests': '1',
                    }
                    
                    response = self.session.get(search_url, headers=headers, timeout=30)
                    
                    if response.status_code == 200:
                        logger.info(f"Successfully got response from {search_url}")
                        linkedin_profiles = self.extract_linkedin_profiles(response.text)
                        if linkedin_profiles:
                            logger.info(f"Fallback method found {len(linkedin_profiles)} profiles")
                            return linkedin_profiles
                    
                    time.sleep(random.uniform(2, 5))  # Random delay between attempts
                    
                except Exception as e:
                    logger.warning(f"Fallback attempt failed for {search_url}: {e}")
                    continue
            
            logger.error("All fallback methods failed")
            return None
            
        except Exception as e:
            logger.error(f"Error in fallback method: {e}")
            return None

    def scrape_linkedin_profiles(self, search_query):
        """Main method to scrape LinkedIn profiles using browser automation with fallback"""
        logger.info(f"Starting LinkedIn profile search for: {search_query}")
        
        # Setup browser if not already done
        with self.driver_lock:
            if not self.driver:
                if not self.setup_browser():
                    logger.error("Failed to setup browser")
                    return None
        
        try:
            # Search Google using browser
            html_content = self.search_google_with_browser(search_query)
            if not html_content:
                logger.error("Failed to search Google with browser, trying fallback...")
                return self.scrape_linkedin_profiles_fallback(search_query)
            
            # Extract LinkedIn profiles with metadata
            linkedin_profiles = self.extract_linkedin_profiles(html_content)
            
            # If no profiles found, try fallback
            if not linkedin_profiles:
                logger.warning("No profiles found with browser method, trying fallback...")
                return self.scrape_linkedin_profiles_fallback(search_query)
            
            return linkedin_profiles
            
        except Exception as e:
            logger.error(f"Error in scrape_linkedin_profiles: {e}")
            logger.info("Trying fallback method...")
            return self.scrape_linkedin_profiles_fallback(search_query)
    
    def close_browser(self):
        """Close the browser"""
        if self.driver:
            try:
                self.driver.quit()
                logger.info("Browser closed")
            except Exception as e:
                logger.error(f"Error closing browser: {e}")
            finally:
                self.driver = None

# Global scraper instance
scraper = LinkedInWebhookScraper()

@app.route('/webhook/linkedin-search', methods=['POST'])
def linkedin_search_webhook():
    """Webhook endpoint for LinkedIn profile search"""
    try:
        # Get JSON data from request
        data = request.get_json()
        
        if not data:
            return jsonify({
                'success': False,
                'error': 'No JSON data provided',
                'timestamp': datetime.now().isoformat()
            }), 400
        
        # Extract search query from request
        search_query = data.get('search_query', '')
        company_name = data.get('company_name', '')
        job_titles = data.get('job_titles', [])
        
        if not search_query and not company_name:
            return jsonify({
                'success': False,
                'error': 'Either search_query or company_name must be provided',
                'timestamp': datetime.now().isoformat()
            }), 400
        
        # Construct search query if not provided
        if not search_query:
            if job_titles:
                titles_str = ' OR '.join([f'"{title}"' for title in job_titles])
                search_query = f'({titles_str}) "{company_name}" site:linkedin.com/in'
            else:
                search_query = f'"{company_name}" site:linkedin.com/in'
        
        logger.info(f"Received search request: {search_query}")
        
        # Perform the search
        results = scraper.scrape_linkedin_profiles(search_query)
        
        if results is None:
            return jsonify({
                'success': False,
                'error': 'Failed to perform search - possible bot detection',
                'timestamp': datetime.now().isoformat()
            }), 500
        
        # Prepare response
        response_data = {
            'success': True,
            'query': search_query,
            'results_count': len(results),
            'profiles': results,
            'timestamp': datetime.now().isoformat()
        }
        
        logger.info(f"Search completed successfully. Found {len(results)} profiles")
        return jsonify(response_data), 200
        
    except Exception as e:
        logger.error(f"Error in webhook: {e}")
        return jsonify({
            'success': False,
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }), 500

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat()
    }), 200

@app.route('/test', methods=['GET'])
def test_endpoint():
    """Test endpoint to check if the service is working"""
    try:
        # Test basic functionality
        test_query = '"APM - Australian Property Management" site:linkedin.com/in'
        logger.info("Running test search...")
        
        # Try to get a simple response
        results = scraper.scrape_linkedin_profiles(test_query)
        
        return jsonify({
            'status': 'test_completed',
            'query': test_query,
            'results_found': len(results) if results else 0,
            'timestamp': datetime.now().isoformat()
        }), 200
        
    except Exception as e:
        logger.error(f"Test failed: {e}")
        return jsonify({
            'status': 'test_failed',
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }), 500

@app.route('/', methods=['GET'])
def root():
    """Root endpoint with API documentation"""
    return jsonify({
        'message': 'LinkedIn Profile Search Webhook API',
        'endpoints': {
            'POST /webhook/linkedin-search': 'Search for LinkedIn profiles',
            'GET /health': 'Health check',
            'GET /test': 'Test endpoint to verify functionality',
            'GET /': 'This documentation'
        },
        'example_request': {
            'search_query': '(CEO OR COO OR "Managing Director") "APM - Australian Property Management" site:linkedin.com/in',
            'company_name': 'APM - Australian Property Management',
            'job_titles': ['CEO', 'COO', 'Managing Director', 'Sales Director']
        }
    }), 200

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))
    
    logger.info("Starting LinkedIn Profile Search Webhook Server...")
    logger.info(f"Server will be available at: http://0.0.0.0:{port}")
    logger.info(f"Webhook endpoint: http://0.0.0.0:{port}/webhook/linkedin-search")
    
    try:
        app.run(host='0.0.0.0', port=port, debug=False, threaded=True)
    except KeyboardInterrupt:
        logger.info("Shutting down server...")
    finally:
        scraper.close_browser()