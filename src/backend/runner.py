import uuid
import asyncio

from dotenv import load_dotenv
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types
from src.backend.customer_service_agent.agent import root_agent

# Create a session service
session_service_stateful = InMemorySessionService()

async def chat_with_agent(user_message):
    print(user_message)
    # Prepare state and IDs
    initial_state = {
        'purchased_parts': [],
        'purchased_appliances': [],
        'interaction_history': []
    }
    APP_NAME = "Customer Service"
    USER_ID = "customer"
    SESSION_ID = str(uuid.uuid4())

    # Create session
    stateful_session = await session_service_stateful.create_session(
        app_name=APP_NAME,
        user_id=USER_ID,
        session_id=SESSION_ID,
        state=initial_state,
    )

    runner = Runner(
        agent=root_agent,
        app_name=APP_NAME,
        session_service=session_service_stateful,
    )

    new_message = types.Content(
        role="user",
        parts=[types.Part(text=user_message)]
    )

    response = ""
    # Run the agent and get the response
    for event in runner.run(
        user_id=USER_ID,
        session_id=SESSION_ID,
        new_message=new_message,
    ):
        if event.is_final_response():
            if event.content and event.content.parts:
                response = event.content.parts[0].text

    return response