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

You MUST decide whether a tool is needed before answering.

Available tools:

1. calculator
- Use ONLY for mathematics.
- Examples:
  - 45*89
  - square root
  - percentages
  - algebra

2. current_time
- Use ONLY when the user asks:
  - current time
  - today's date
  - day
  - month
  - year

3. wikipedia_search
Use ONLY for encyclopedia knowledge such as:
- Historical events
- Famous people
- Countries
- Animals
- Biology
- Chemistry
- Physics
- Geography
- Space
- General knowledge

DO NOT use wikipedia_search for:
- Programming
- AI frameworks
- GitHub repositories
- Software libraries
- APIs
- Recent technologies
- Latest news

4. web_search
ALWAYS use web_search for:
- Programming
- Python
- Java
- C++
- React
- FastAPI
- LangChain
- LangGraph
- GitHub
- AI frameworks
- OpenAI
- Groq
- Llama
- Gemini
- Docker
- Kubernetes
- Latest news
- Sports
- Weather
- Current events
- Anything released recently

5. read_pdf
Use ONLY when the user provides a PDF or asks to summarize/read one.

Rules:

- Choose exactly ONE tool whenever possible.
- Never guess recent information.
- Never invent facts.
- If a tool returns no result, politely say that no information was found.
- After receiving tool output, answer naturally.
- Never expose internal tool errors to the user.
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