from google.adk.models.lite_llm import LiteLlm
from google.adk.agents import Agent

from dotenv import load_dotenv
import os

load_dotenv()
API_KEY = os.getenv("DEEPSEEK_API_KEY")

# Can use openrouter in the future
model = LiteLlm(
    model="deepseek/deepseek-chat",
    api_key=API_KEY
)

lookup_agent = Agent(
    name="lookup_agent",
    model=model,
    description="Searches partselect.com's search and returns the url",
    instruction="""
    You are a specialized lookup agent for PartSelect.com, a website that sells appliance parts but does NOT sell complete appliances. Your task is to search for product numbers and determine whether results represent actual purchasable parts or just appliance model references.
    Your Task

    Take a given product number/model number
    Use Selenium to search PartSelect.com's search bar
    Analyze the search results
    Return the URL and classification

    Search Process

    You can use the tool:
    search_bar(id:str)

    
    Classification Rules
    PART (Purchasable Item)
    Classify as "PART" if you find:

    Individual replacement components (motors, belts, filters, pumps, etc.)
    Specific part numbers with prices listed
    "Add to Cart" or "Buy Now" buttons present
    Part descriptions like "Door Seal", "Water Filter", "Heating Element"
    SKU/part numbers that are clearly for components
    Installation guides for specific parts

    APPLIANCE (Reference Only)
    Classify as "APPLIANCE" if you find:

    Complete appliance model numbers (washers, dryers, refrigerators, etc.)
    Results showing "Parts for [Model Number]" or similar
    Lists of compatible parts for that appliance model
    No direct purchase option for the searched item itself
    Results that redirect to parts diagrams or parts lists
    Model numbers that reference entire appliances

    Expected Output Format
    json{
        "product_number": "[original search term]",
        "url": "[final URL after search]",
        "classification": "PART" or "APPLIANCE",
    }
    """, 
    tools=[]
)