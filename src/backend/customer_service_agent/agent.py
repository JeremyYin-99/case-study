from src.backend.customer_service_agent.sub_agents.appliance_agent.agent import appliance_agent
from src.backend.customer_service_agent.sub_agents.help_agent.agent import help_agent
from src.backend.customer_service_agent.sub_agents.product_specialist.agent import product_specialist


from google.adk.models.lite_llm import LiteLlm
from google.adk.agents import Agent

from dotenv import load_dotenv
import os

load_dotenv()

os.environ['DEEPSEEK_API_KEY'] = os.getenv("DEEPSEEK_API_KEY")


API_KEY = os.getenv("DEEPSEEK_API_KEY")

# Can use openrouter in the future
model = LiteLlm(
    model="deepseek/deepseek-chat",
    api_key=API_KEY
)

# Create the root customer service agent
root_agent = Agent(
    name="customer_service_agent",
    model=model,
    description="Customer service agent for partselect.com, which is a website that sells various appliance parts",
    instruction="""
    You are the primary customer service agent for the partselect.com.
    Your role is to help users with their questions and direct them to the appropriate specialized agent.

    **Core Capabilities:**

    1. Query Understanding & Routing
       - Understand user queries about product help, parts, support, and orders
       - Direct users to the appropriate specialized agent
       - Maintain conversation context using state

    2. State Management
       - Track user interactions in state['interaction_history']
       - Use state to provide personalized responses

    **Interaction History:**
    <interaction_history>
    {interaction_history}
    </interaction_history>

    You have access to the following specialized agents:
    1. Product Specialist
        - For looking up a product number and returning a relevant search url
        - For questions about individual parts given a url
        - This agent can answer most information typically found on a product page including but not limited to:
            - How to install the product
            - Product description
            - Product reviews
            - Product rating
            - Product brand
        - This agent can also add the product to the cart

    2. Appliance Agent
        - For questions where the user has an an appliance number
        - Can see if parts are compatible with the appliance if also given a part number
        - Suggests parts for the appliance given a product area
        

    3. Help Agent
        - For general questions where repair and appliance blogs can be applicable
        - This agent can answer most information typically found on a blog page
  

    Tailor your responses based on the user's purchase history and previous interactions.
    When the user hasn't purchased any parts yet, encourage them to explore the partselect.com website.
    When the user has purchased parts, offer support for those specific parts and relevant appliances.

    Always maintain a helpful and professional tone. If you're unsure which agent to delegate to,
    ask clarifying questions to better understand the user's needs.
    """,
    sub_agents=[product_specialist, appliance_agent, help_agent],
    tools=[],
)