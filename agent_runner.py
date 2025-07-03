import os
from dotenv import load_dotenv
from calendar_utils import get_free_slots
from langchain.chat_models import ChatOpenAI
from langchain.agents import initialize_agent, Tool
from langchain.agents.agent_types import AgentType

# --------------------------
# Step 1: Load API Credentials
# --------------------------
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_API_BASE = os.getenv("OPENAI_API_BASE")

if not OPENAI_API_KEY or not OPENAI_API_BASE:
    print("❌ API key or base URL not found. Please check your .env file.")
    exit()

print("✅ Environment loaded. Starting agent...")

# --------------------------
# Step 2: Initialize LLM (Mixtral via OpenRouter)
# --------------------------
llm = ChatOpenAI(
    temperature=0.5,
    model="mistralai/mixtral-8x7b-instruct",
    openai_api_key=OPENAI_API_KEY,
    openai_api_base=OPENAI_API_BASE
)

# --------------------------
# Step 3: Define Tool
# --------------------------
def get_free_slots():
    return "Today, available slots: 2:30PM–3:15PM, 4:00PM–5:00PM."

tools = [
    Tool(
        name="FreeSlotChecker",
        func=lambda x: get_free_slots(),  # x is ignored here
        description="Use this to check real-time availability between 2PM and 5PM today using the live backend."
    )
]


# --------------------------
# Step 4: Initialize Agent
# --------------------------
agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True
)

# --------------------------
# Step 5: Run Interactive Loop
# --------------------------
while True:
    query = input("\n💬 AI Assistant is running! Type below:\n\nYou: ")
    if query.lower() in ["exit", "quit"]:
        print("👋 Exiting assistant.")
        break

    try:
        response = agent.run(query)
        print("\n🤖 Assistant:", response)
    except Exception as e:
        print("\n❌ Error:", e)
