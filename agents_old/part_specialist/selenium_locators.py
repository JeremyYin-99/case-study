from selenium.webdriver.common.by import By
from enum import Enum, auto


class LocatorType(Enum):
    """Enum for locator types to improve code readability"""
    ID = auto()
    NAME = auto()
    XPATH = auto()
    CSS_SELECTOR = auto()
    CLASS_NAME = auto()
    TAG_NAME = auto()
    LINK_TEXT = auto()
    PARTIAL_LINK_TEXT = auto()

class Locator:
    """Class for storing and accessing locators"""
    
    def __init__(self, locator_type: LocatorType, value: str, description: str = ""):
        self.locator_type = locator_type
        self.value = value
        self.description = description
        
    def get_by(self) -> str:
        """Convert LocatorType enum to Selenium By class"""
        mapping = {
            LocatorType.ID: By.ID,
            LocatorType.NAME: By.NAME,
            LocatorType.XPATH: By.XPATH,
            LocatorType.CSS_SELECTOR: By.CSS_SELECTOR,
            LocatorType.CLASS_NAME: By.CLASS_NAME,
            LocatorType.TAG_NAME: By.TAG_NAME,
            LocatorType.LINK_TEXT: By.LINK_TEXT,
            LocatorType.PARTIAL_LINK_TEXT: By.PARTIAL_LINK_TEXT
        }
        return mapping[self.locator_type]
    
    def get_locator(self) -> tuple:
        """Return tuple of (By, value) for Selenium"""
        return (self.get_by(), self.value)
    
    def __str__(self) -> str:
        """String representation for debugging"""
        return f"{self.locator_type.name}: {self.value} ({self.description})"

class AppliancePageLocators:
    """Container class for appliance page locators"""
    BRAND_CONTAINER = Locator(LocatorType.XPATH, "/html/body/main/div[2]/ul[1]", "Container of brand listings on appliance page")
    BRAND_LIST = Locator(LocatorType.TAG_NAME, "li", "List items containing brand links")
    BRAND_LINK = Locator(LocatorType.TAG_NAME, "a", "Brand link element")

class BrandPageLocators:
    """Container class for brand page locators"""
    PART_LINK = Locator(LocatorType.CLASS_NAME, "nf__part__detail__title", "Link to part details on Brand-Appliance page")

class PartPageLocators:
    """Container class for part detail page locators"""
    PART_NAME = Locator(LocatorType.TAG_NAME, "h1", "Part name heading")
    BRAND_NAME = Locator(LocatorType.CSS_SELECTOR, "span[itemprop='brand']", "Part Manufacturer")
    SOLUTIONS = Locator(LocatorType.XPATH, "/html/body/main/div[2]/div[5]/div[2]/div[1]", "List of problems that this product solves")
    APPLICABLE_PRODUCTS = Locator(LocatorType.XPATH, "/html/body/main/div[2]/div[1]/div[3]/div[8]/span[2]", "Applicance manufactures that can use this product")
    REVIEW_COUNT = Locator(LocatorType.CSS_SELECTOR, "meta[itemprop='reviewCount']", "Review count metadata")
    RATING = Locator(LocatorType.CSS_SELECTOR, "meta[itemprop='ratingValue']", "Rating value metadata")
    INSTOCK = Locator(LocatorType.CSS_SELECTOR, "span[itemprop='availability']", "Check whether the item is in stock or on order")
    PRICE = Locator(LocatorType.CLASS_NAME, "js-partPrice", "Part price element")
    DIFFICULTY = Locator(LocatorType.XPATH, "/html/body/main/div[2]/div[1]/div[3]/div[2]/div[1]/div[1]/div[2]/div[1]/p", "Installation difficulty")
    TIME_COMMITMENT = Locator(LocatorType.XPATH, "/html/body/main/div[2]/div[1]/div[3]/div[2]/div[1]/div[1]/div[2]/div[2]/p", "Time commitment information")