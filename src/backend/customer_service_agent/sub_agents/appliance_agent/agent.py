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

appliance_agent = Agent(
    name="appliance_agent",
    model=model,
    description="Searches partselect.com's appliance section when given an appliance catagory and check if part is compatible with the appliance",
    instruction="""
    """, 
    tools=[]
)