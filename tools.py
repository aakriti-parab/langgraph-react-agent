from datetime import datetime

from langchain_core.tools import tool
from langchain_community.utilities import WikipediaAPIWrapper
from duckduckgo_search import DDGS
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

    except Exception as e:
        return f"Calculator Error: {e}"


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
    Search Wikipedia for encyclopedia-style information.
    """

    try:

        result = wiki.run(query)

        if not result:
            return "No Wikipedia results found."

        return result

    except Exception as e:

        return f"Wikipedia Search Error: {e}"


# -------------------------------------------------
# DuckDuckGo Web Search
# -------------------------------------------------

@tool
def web_search(query: str) -> str:
    """
    Search the internet for recent information,
    current events, sports, news, weather,
    technology and live information.
    """

    try:

        with DDGS() as ddgs:

            results = list(ddgs.text(query, max_results=5))

        if len(results) == 0:
            return "No search results found."

        answer = ""

        for i, result in enumerate(results, start=1):

            answer += (
                f"{i}. {result['title']}\n"
                f"{result['body']}\n"
                f"{result['href']}\n\n"
            )

        return answer

    except Exception as e:

        return f"Web Search Error: {e}"


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

tools = [
    calculator,
    current_time,
    wikipedia_search,
    web_search,
    read_pdf,
]