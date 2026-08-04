from datetime import datetime

from langchain_core.tools import tool
from langchain_community.utilities import WikipediaAPIWrapper
from ddgs import DDGS
from pypdf import PdfReader

# -------------------------------------------------
# Wikipedia
# -------------------------------------------------

wiki = WikipediaAPIWrapper()

# -------------------------------------------------
# Calculator
# -------------------------------------------------

@tool
def calculator(expression: str) -> str:
    """
    Evaluate a mathematical expression.
    """

    try:

        result = eval(expression, {"__builtins__": {}}, {})

        return f"The answer is {result}"

    except Exception:

        return ""


# -------------------------------------------------
# Current Time
# -------------------------------------------------

@tool
def current_time(_: str = "") -> str:
    """
    Returns the current date and time.
    """

    return datetime.now().strftime("%d-%m-%Y %H:%M:%S")


# -------------------------------------------------
# Wikipedia Search
# -------------------------------------------------

@tool
def wikipedia_search(query: str) -> str:
    """
    Search Wikipedia for encyclopedia information.

    Use ONLY for:
    - Famous people
    - History
    - Countries
    - Science
    - Geography
    - Biology
    - Physics

    NOT for:
    - Programming
    - AI frameworks
    - GitHub
    - Software
    - Latest technology
    """

    try:

        result = wiki.run(query)

        if not result:
            return ""

        if "No good Wikipedia Search Result" in result:
            return ""

        if "Page:" not in result:
            return ""

        return result

    except Exception:

        return ""


# -------------------------------------------------
# Web Search
# -------------------------------------------------

@tool
def web_search(query: str) -> str:
    """
    Search the web.

    Use for:
    - Programming
    - LangGraph
    - LangChain
    - FastAPI
    - React
    - Docker
    - Python
    - GitHub
    - AI
    - Technology
    - News
    - Sports
    - Weather
    - Current events
    """

    try:

        with DDGS() as ddgs:

            results = list(
                ddgs.text(
                    query,
                    max_results=5
                )
            )

        if len(results) == 0:
            return ""

        answer = ""

        for i, result in enumerate(results, start=1):

            title = result.get("title", "")
            body = result.get("body", "")
            href = result.get("href", "")

            answer += (
                f"{i}. {title}\n"
                f"{body}\n"
                f"{href}\n\n"
            )

        return answer

    except Exception:

        return ""


# -------------------------------------------------
# PDF Reader
# -------------------------------------------------

@tool
def read_pdf(file_path: str, max_chars: int = 5000) -> str:
    """
    Read text from a PDF.
    """

    try:

        reader = PdfReader(file_path)

        text = ""

        for page in reader.pages:

            page_text = page.extract_text()

            if page_text:

                text += page_text + "\n"

        if not text.strip():

            return "No readable text found."

        if len(text) > max_chars:

            return text[:max_chars] + "\n\n[Output truncated]"

        return text

    except FileNotFoundError:

        return "PDF not found."

    except Exception as e:

        return f"PDF Reader Error: {e}"


# -------------------------------------------------
# Register Tools
# -------------------------------------------------
print("\n========== REGISTERED TOOLS ==========")
print(calculator.name)
print(current_time.name)
print(wikipedia_search.name)
print(web_search.name)
print(read_pdf.name)
print("======================================\n")
tools = [
    calculator,
    current_time,
    wikipedia_search,
    web_search,
    read_pdf,
]