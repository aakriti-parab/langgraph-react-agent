# 🤖 LangGraph ReAct AI Agent

An intelligent AI assistant built using **LangGraph**, **LangChain**, **Groq LLM**, and **FastAPI**. The agent follows the **ReAct (Reason + Act)** paradigm, allowing it to reason, use tools, retain conversation memory, expose REST APIs, and stream responses in real time using **Server-Sent Events (SSE)**.

---

# 🚀 Features

- 🧠 ReAct AI Agent powered by LangGraph
- 💬 Conversation Memory using MemorySaver
- ➗ Calculator Tool
- 🕒 Current Date & Time Tool
- 📚 Wikipedia Search Tool
- 📄 PDF Reader & Summarizer
- ⚡ Groq Llama 3.3 70B Versatile LLM
- 🌐 FastAPI REST API
- 📖 Interactive Swagger Documentation
- 🔄 Real-time Response Streaming using Server-Sent Events (SSE)
- 💻 Interactive Command Line Interface

---

# 🛠️ Tech Stack

- Python
- LangGraph
- LangChain
- FastAPI
- Uvicorn
- Groq API
- Llama 3.3 70B Versatile
- LangChain-Groq
- Pydantic
- PyPDF
- WikipediaAPIWrapper
- Python Dotenv

---

# 📂 Project Structure

```text
langgraph-react-agent/
│
├── agents/
│   └── react_agent.py
│
├── app.py
├── api.py
├── graph.py
├── tools.py
├── requirements.txt
├── README.md
├── .env.example
├── .gitignore
└── .venv/
```

---

# ⚙️ Installation

## 1. Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/langgraph-react-agent.git

cd langgraph-react-agent
```

---

## 2. Create Virtual Environment

```bash
python -m venv .venv
```

---

## 3. Activate Virtual Environment

### Windows

```bash
.venv\Scripts\activate
```

### macOS/Linux

```bash
source .venv/bin/activate
```

---

## 4. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 5. Configure Environment Variables

Create a `.env` file.

```text
GROQ_API_KEY=your_groq_api_key
```

---

# ▶️ Running the Application

## Command Line Interface

```bash
python app.py
```

---

## FastAPI Server

```bash
uvicorn api:app --reload
```

---

## Swagger Documentation

Open:

```text
http://127.0.0.1:8000/docs
```

---

# 🌐 REST API Endpoints

## Home

```
GET /
```

Returns a welcome message.

---

## Ask AI

```
POST /ask
```

### Request

```json
{
    "question": "What is Artificial Intelligence?"
}
```

### Response

```json
{
    "success": true,
    "question": "What is Artificial Intelligence?",
    "answer": "Artificial Intelligence..."
}
```

---

# 🔄 SSE Streaming Endpoint

```
GET /stream?question=Tell me a joke
```

Example Output

```text
data: I'd

data: be

data: happy

data: to

data: tell

data: you

...

data: [DONE]
```

---

# 💬 Example Prompts

### Calculator

```
Calculate 45 * 23
```

---

### Time

```
What is the current time?
```

---

### Wikipedia

```
Search Wikipedia for Artificial Intelligence
```

---

### Memory

```
My name is Aakriti
```

Later ask

```
What is my name?
```

---

### PDF Reader

```
Summarize this PDF

/path/to/sample.pdf
```

---

# 🧠 How It Works

1. User sends a query.
2. LangGraph ReAct Agent analyzes the request.
3. The agent reasons whether tool usage is required.
4. Appropriate tool(s) execute.
5. Groq LLM generates the response.
6. MemorySaver stores conversation history.
7. FastAPI exposes the functionality through REST APIs.
8. Responses can also be streamed in real time using SSE.

---

# 🔧 Available Tools

| Tool | Description |
|------|-------------|
| Calculator | Evaluates mathematical expressions |
| Current Time | Returns current date and time |
| Wikipedia Search | Retrieves information from Wikipedia |
| PDF Reader | Reads and summarizes PDF documents |

---

# 📌 Future Improvements

- Authentication
- Web Search Integration
- React Frontend
- Streamlit Interface
- Database-backed Memory
- Multi-user Sessions
- Voice Assistant

---

# 📷 Sample CLI Interaction

```text
============================================================
🤖 AI Research Assistant (LangGraph ReAct Agent)
Type 'exit' to quit.
============================================================

You: Calculate 24 * 18

Agent: 432

You: My name is Aakriti

Agent: Nice to meet you, Aakriti!

You: What is my name?

Agent: Your name is Aakriti.
```

---

# 👩‍💻 Author

**Aakriti Arun Parab**

B.Tech – Artificial Intelligence & Robotics

Manipal University Jaipur

---

# 📄 License

Developed for educational purposes as part of a college assignment.