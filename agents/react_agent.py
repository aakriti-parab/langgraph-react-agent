import os
from dotenv import load_dotenv

from langchain_groq import ChatGroq
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import MemorySaver

from tools import tools

load_dotenv()

# -------------------------------------------------
# Memory
# -------------------------------------------------

memory = MemorySaver()

# -------------------------------------------------
# LLM
# -------------------------------------------------

llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    api_key=os.getenv("GROQ_API_KEY"),
    temperature=0,
)

# -------------------------------------------------
# System Prompt
# -------------------------------------------------

SYSTEM_PROMPT = """
You are an intelligent AI assistant.

You have access to the following tools:

1. calculator
- Perform mathematical calculations.

2. current_time
- Get the current date and time.

3. wikipedia_search
- Use for historical facts, people, science,
places and encyclopedia knowledge.

4. web_search
- Use for current events, latest news,
sports, technology and anything recent.

5. read_pdf
- Read and summarize PDF files.

Always use the correct tool whenever necessary.
"""

# -------------------------------------------------
# Create Agent
# -------------------------------------------------

agent = create_react_agent(
    model=llm,
    tools=tools,
    checkpointer=memory,
    prompt=SYSTEM_PROMPT,
)