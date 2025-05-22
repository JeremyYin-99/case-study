import json

from dotenv import load_dotenv
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService  # Still needed for Runner, but not for state
from google.genai import types
from src.backend.customer_service_agent.agent import root_agent
import uuid

load_dotenv()

APP_NAME = "Customer Service"
USER_ID = "customer"
SESSION_ID = str(uuid.uuid4())  # For real use, make this user-specific

session_service_stateful = InMemorySessionService()

initial_state = {
    'interaction_history': []
}

def save_state_to_file(session_id, state):
    with open(f"chat_logs/state_{session_id}.json", "w") as f:
        json.dump(state, f, indent=4)

def load_state_from_file(session_id):
    try:
        with open(f"chat_logs/state_{session_id}.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return initial_state.copy()

# # Ensure state file exists
# save_state_to_file(SESSION_ID, initial_state)

# ----------- Chat Function ------------

async def chat_with_agent(user_message):
    # Load the interaction history from the json file
    try:
        state = load_state_from_file(SESSION_ID)
    except Exception as e:
        print(f"Error loading state: {e}")
        print("Creating a new interaction log from scratch.")
        state = initial_state.copy()
        save_state_to_file(SESSION_ID, state)
    interaction_history = state.get('interaction_history', [])

    stateful_session = await session_service_stateful.create_session(
        app_name=APP_NAME,
        user_id=USER_ID,
        session_id=SESSION_ID,
        state=initial_state,
    )

    # Add the user's message to the interaction history
    interaction_history.append({'role': 'user', 'message': user_message})


    # Create the message using types and include the interaction history
    new_message = types.Content(
        role="user",
        parts=[
            types.Part(text=f"{msg['role'].capitalize()}: {msg['message']}")
            for msg in interaction_history
        ]
    )

    # We still need a session service for the Runner, but its state is unused
    runner = Runner(
        agent=root_agent,
        app_name=APP_NAME,
        session_service=session_service_stateful,
    )
    print("Running the agent...")

    response = ""
    for event in runner.run(
        user_id=USER_ID,
        session_id=SESSION_ID,
        new_message=new_message,
    ):
        if event.is_final_response() and event.content and event.content.parts:
            response = event.content.parts[0].text

    # Add the agent's response to the interaction history
    interaction_history.append({'role': 'agent', 'message': response})

    # Save the updated interaction history to the json file
    state['interaction_history'] = interaction_history
    save_state_to_file(SESSION_ID, state)

    return response

# Example usage
if __name__ == "__main__":
    import asyncio
    asyncio.run(chat_with_agent("Hello, what can you do?"))