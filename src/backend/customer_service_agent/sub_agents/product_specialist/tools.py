# selenium webscraping
import re
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

BASE_URL = "https://www.partselect.com/"

def get_url(product_number: str) -> str:
    """
    Get the URL for a given product number from PartSelect.com.
    
    Args:
        product_number (str): The product number to search for.
        
    Returns:
        str: The URL of the product page on PartSelect.com.
    """
    # Initialize WebDriver
    options = Options()
    # options.add_argument("--headless")  # Run in headless mode
    driver = webdriver.Chrome(options=options)
    
    try:
        # Construct the search URL
        driver.get(BASE_URL)
        input_element = driver.find_element(by=By.XPATH, value="/html/body/header/div[6]/div/div/div[2]/div[2]/div[1]/input")
        input_element.send_keys(product_number)
        input_element.send_keys(Keys.ENTER)  # Wait for up to 10 seconds
        # Get the current URL
        # Wait for the page to load and the URL to change
        wait = WebDriverWait(driver, 5).until(EC.url_changes(BASE_URL))
        product_url = driver.current_url
        
    finally:
        # Close the WebDriver
        driver.quit()
    
    return product_url

def read_page(url: str) -> str:
    """
    Read the content of a page given its URL.
    
    Args:
        url (str): The URL of the page to read.
        
    Returns:
        str: The content of the page.
    """
    # Initialize WebDriver
    options = Options()
    # options.add_argument("--headless")  # Run in headless mode
    driver = webdriver.Chrome(options=options)
    
    try:
        # Open the URL
        driver.get(url)
        # Wait for the page to load
        wait = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        page_content = driver.find_element(By.ID, "main").text
        page_content = re.sub("\s{2,}"," ",page_content)
        
    finally:
        # Close the WebDriver
        driver.quit()
    
    return page_content

def add_product_to_cart(url: str) -> str:
    """
    Add a product to the cart given its URL.
    
    Args:
        url (str): The URL of the product page.
        
    Returns:
        str: Confirmation message or status.
    """
    # Initialize WebDriver
    options = Options()
    # options.add_argument("--headless")  # Run in headless mode
    driver = webdriver.Chrome(options=options)
    
    try:
        # Open the URL
        driver.get(url)
        # Wait for the page to load
        wait = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        add_to_cart_button = driver.find_element(By.XPATH, "//*[@id='mainAddToCart']/form/div/button")
        add_to_cart_button.click()
        confirmation_message = "Product added to cart successfully."
        
    finally:
        # Close the WebDriver
        driver.quit()
    
    return confirmation_message