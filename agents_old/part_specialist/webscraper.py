from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time
import pandas as pd
from typing import List, Dict, Any
from pages import BrandPage, PartPage, AppliancePage

# Constants
BASE_URL = "https://www.partselect.com/{}-Parts.htm"
APPLIANCES = ["Refrigerator", "Dishwasher"]  # Scope of the Case Study
REST = 5  # Seconds rest between queries to avoid over scraping/overloading site


class PartselectScraper:
    """Main scraper class to orchestrate the web scraping process"""
    
    def __init__(self):
        """Initialize the scraper with Firefox WebDriver"""

        # Add options

        options = Options()
        # proxy = "103.247.14.51:9285"
        # options.add_argument(f"--proxy-server={proxy}")
        agent = 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'
        options.add_argument(f'user-agent={agent}')
        options.add_argument('--accept-language=en-US,en;q=0.9')
        options.add_argument('--accept=text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8')
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-notifications")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_experimental_option("excludeSwitches", ["enable-automation"]) 
        options.add_experimental_option("useAutomationExtension", False) 


        self.driver = webdriver.Chrome(options=options)
        self.results = []
        
    def close(self):
        """Close the WebDriver"""
        if self.driver:
            self.driver.quit()
            
    def scrape_appliance(self, appliance: str, max_brands: int = None, max_parts: int = None) -> List[Dict[str, Any]]:
        """
        Scrape parts data for a specific appliance
        
        Args:
            appliance: Appliance type (e.g., "Refrigerator")
            max_brands: Maximum number of brands to scrape (for testing)
            max_parts: Maximum number of parts per brand to scrape (for testing)
            
        Returns:
            List of dictionaries containing part information
        """
        appliance_url = BASE_URL.format(appliance)
        self.driver.get(appliance_url)
        
        # Get brand URLs
        appliance_page = AppliancePage(self.driver)
        brand_urls = appliance_page.get_brand_urls()
        
        if max_brands:
            brand_urls = brand_urls[:max_brands]
            
        print(f"Found {len(brand_urls)} brand URLs for {appliance}")
        
        all_parts = []
        
        # Process each brand
        for i, brand_url in enumerate(brand_urls):
            print(f"Processing brand {i+1}/{len(brand_urls)}: {brand_url}")
            
            self.driver.get(brand_url)
            time.sleep(REST)  # Respect the site by waiting between requests
            
            # Get part URLs
            brand_page = BrandPage(self.driver)
            part_urls = brand_page.get_part_urls()
            
            if max_parts:
                part_urls = part_urls[:max_parts]
                
            print(f"Found {len(part_urls)} part URLs for this brand")
            
            # Process each part
            for j, part_url in enumerate(part_urls):
                print(f"Processing part {j+1}/{len(part_urls)}")
                
                self.driver.get(part_url)
                time.sleep(REST)  # Respect the site by waiting between requests
                
                # Get part information
                part_page = PartPage(self.driver)
                part_info = part_page.get_part_info()
                part_info['appliance'] = appliance
                
                all_parts.append(part_info)
                
        return all_parts
    
    def save_to_csv(self, filename: str):
        """Save results to CSV file"""
        if self.results:
            df = pd.DataFrame(self.results)
            df.to_csv(filename, index=False)
            print(f"Saved {len(self.results)} records to {filename}")
        else:
            print("No results to save")



if __name__ == "__main__":
    scraper = PartselectScraper()
    
    try:
        all_parts = []
        
        for appliance in APPLIANCES:
            print(f"Starting to scrape {appliance} parts...")
            parts = scraper.scrape_appliance(appliance)
            all_parts.extend(parts)
            
        scraper.results = all_parts
        scraper.save_to_csv("appliance_parts.csv")
        
    finally:
        # Ensure the WebDriver is closed properly
        scraper.close()