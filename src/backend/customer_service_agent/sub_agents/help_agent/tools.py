# selenium webscraping
import re
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

BASE_URL = "https://www.partselect.com/blog/"

def get_blog_urls(question: str) -> str:
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
        input_element = driver.find_element(by=By.XPATH, value="/html/body/main/div[2]/div[1]/div/div[2]/input")
        input_element.send_keys(question)
        input_element.send_keys(Keys.ENTER)  # Wait for up to 10 seconds
        # Get the current URL
        # Wait for the page to load and the URL to change
        wait = WebDriverWait(driver, 5).until(EC.url_changes(BASE_URL))
        blog_search_url = driver.current_url

        # Extract the top 5 URLs from the search results
        url_elements = driver.find_elements(By.CLASS_NAME, "blog__search__result__content")
        
        # Extract the blog title and get the urls from the first 5 elements
        title_urls = []
        for element in url_elements[:5]:
            title_element = element.find_element(By.TAG_NAME, "a")
            title = title_element.text
            url = title_element.get_attribute("href")
            title_urls.append((title, url))

        
    finally:
        # Close the WebDriver
        driver.quit()
    
    return title_urls

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
        page_content = driver.find_element(By.CLASS_NAME, "blog__article-page__content").text
        page_content = re.sub("\s{2,}"," ",page_content)
        
    finally:
        # Close the WebDriver
        driver.quit()
    
    return page_content