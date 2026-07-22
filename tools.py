from langchain_core.tools import tool
from langchain_community.utilities import WikipediaAPIWrapper
from datetime import datetime
from pypdf import PdfReader

wiki = WikipediaAPIWrapper()


@tool
def calculator(expression: str) -> str:
    """
    Evaluate a mathematical expression.
    """
    try:
        result = eval(expression)
        return f"The answer is {result}"
    except Exception as e:
        return f"Error: {e}"


@tool
def current_time(_: str = "") -> str:
    """
    Returns the current date and time.
    """
    return datetime.now().strftime("%d-%m-%Y %H:%M:%S")


@tool
def wikipedia_search(query: str) -> str:
    """
    Search Wikipedia and return a summary.
    """
    try:
        return wiki.run(query)
    except Exception as e:
        return f"Wikipedia search failed: {e}"


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
        return f"Error reading PDF: {e}"


tools = [
    calculator,
    current_time,
    wikipedia_search,
    read_pdf,
]