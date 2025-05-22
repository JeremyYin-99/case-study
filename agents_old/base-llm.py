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

agent = Agent(
    name='BaseAgent',
    model=model,
    description="Some description",
    instruction="Some Prompt"
)
    

