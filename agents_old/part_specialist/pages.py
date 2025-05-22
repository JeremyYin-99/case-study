from selenium import webdriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from typing import List, Optional, Dict, Any

from selenium_locators import Locator, PartPageLocators, BrandPageLocators, AppliancePageLocators

MAX_WAIT = 15  # Max time for page to load
MAX_RETRY = 2  # Max number of retries for page to load



class BasePage:
    """Base page object with common functionality"""
    
    def __init__(self, driver: webdriver.Firefox):
        self.driver = driver
        self.wait = WebDriverWait(driver, MAX_WAIT)
        
    def find_element(self, locator: Locator) -> Optional[WebElement]:
        """Find element using Locator object with retry logic"""
        by, value = locator.get_locator()
        
        for _ in range(MAX_RETRY):
            try:
                element = self.wait.until(EC.presence_of_element_located((by, value)))
                return element
            except TimeoutException:
                print(f"Retry finding element: {locator}")
                
        print(f"Could not load element: {locator}")
        return None
    
    def find_elements(self, locator: Locator) -> List[WebElement]:
        """Find elements using Locator object with retry logic"""
        by, value = locator.get_locator()
        
        for _ in range(MAX_RETRY):
            try:
                elements = self.wait.until(EC.presence_of_all_elements_located((by, value)))
                if elements:
                    return elements
            except TimeoutException:
                print(f"Retry finding elements: {locator}")
                
        print(f"Could not load elements: {locator}")
        return []
    
    def get_attribute(self, element: WebElement, attribute: str) -> str:
        """Get attribute from element if exists"""
        if element:
            return element.get_attribute(attribute)
        return "Not Available"
    
    def get_text(self, element: WebElement) -> str:
        """Get text from element if exists"""
        if element:
            return element.text
        return "Not Available"

class AppliancePage(BasePage):
    """Page object for appliance brand listing page"""
    
    def get_brand_urls(self) -> List[str]:
        """Get list of brand URLs for a specific appliance"""

        # Had trouble selecting the brand items directly so the entry point begins at the container
        brand_container = self.find_element(AppliancePageLocators.BRAND_CONTAINER)
        if not brand_container:
            return []
        
        # Get the li elements in the unordered list
        brand_items = brand_container.find_elements(
            AppliancePageLocators.BRAND_LIST.get_by(), 
            AppliancePageLocators.BRAND_LIST.value
        )
        
        # Iterate through the list items and store the product URL
        urls = []
        for item in brand_items:
            try:
                link = item.find_element(
                    AppliancePageLocators.BRAND_LINK.get_by(), 
                    AppliancePageLocators.BRAND_LINK.value
                )
                url = self.get_attribute(link, "href")
                if url:
                    urls.append(url)
            except NoSuchElementException:
                continue
                
        return urls

class BrandPage(BasePage):
    """Page object for brand parts listing page"""
    
    def get_part_urls(self) -> List[str]:
        """Get list of part detail URLs for a specific brand"""
        part_elements = self.find_elements(BrandPageLocators.PART_LINK)
        
        urls = []
        for element in part_elements:
            url = self.get_attribute(element, "href")
            if url:
                urls.append(url)
                
        return urls

class PartPage(BasePage):
    """Page object for part detail page"""
    
    def get_part_info(self) -> Dict[str, Any]:
        """Extract information from each part page"""
        part_info = {}
        
        # Get part name
        part_name_element = self.find_element(PartPageLocators.PART_NAME)
        part_info['name'] = self.get_text(part_name_element)

        # Get part brand
        brand_name_element = self.find_element(PartPageLocators.BRAND_NAME)
        part_info['brand'] = self.get_text(brand_name_element)

        # Get stock status
        stock_status_element = self.find_element(PartPageLocators.INSTOCK)
        part_info['stock_status'] = self.get_text(stock_status_element)

        # Get applicable solutions
        solutions_element = self.find_element(PartPageLocators.SOLUTIONS)
        part_info['solutions'] = self.get_text(solutions_element)
        
        # Get review information
        # review_count_element = self.find_element(PartPageLocators.REVIEW_COUNT)
        # part_info['review_count'] = self.get_attribute(review_count_element, "content")
        
        # rating_element = self.find_element(PartPageLocators.RATING)
        # part_info['rating'] = self.get_attribute(rating_element, "content")
        
        # Get price
        price_element = self.find_element(PartPageLocators.PRICE)
        part_info['price'] = self.get_text(price_element)
        
        # Get installation info
        # difficulty_element = self.find_element(PartPageLocators.DIFFICULTY)
        # part_info['difficulty'] = self.get_text(difficulty_element)
        
        # Get expected time commitment 
        # time_element = self.find_element(PartPageLocators.TIME_COMMITMENT)
        # part_info['time_commitment'] = self.get_text(time_element)
        
        # Add current URL for reference
        part_info['url'] = self.driver.current_url
        
        return part_info