# 🤖 LangGraph ReAct AI Agent

An intelligent command-line AI assistant built using **LangGraph**, **LangChain**, and **Groq LLM**. The agent follows the ReAct (Reason + Act) paradigm, enabling it to reason, use tools, retain conversation memory, and answer user queries efficiently.

---

## 🚀 Features

- 🧠 ReAct AI Agent powered by LangGraph
- 💬 Conversation Memory using `MemorySaver`
- ➗ Calculator Tool
- 🕒 Current Date & Time Tool
- 📚 Wikipedia Search Tool
- 📄 PDF Reader & Summarizer
- ⚡ Fast inference using Groq LLM
- 💻 Interactive Command Line Interface

---

## 🛠️ Tech Stack

- **Python**
- **LangGraph**
- **LangChain**
- **Groq API**
- **Llama 3.3 70B Versatile**
- **LangChain-Groq**
- WikipediaAPIWrapper
- **PyPDF**
- **Python Dotenv**

---

## 📂 Project Structure

```
langgraph-react-agent/
│
├── agents/
│   └── react_agent.py
│
├── app.py
├── graph.py
├── tools.py
├── requirements.txt
├── README.md
├── .env.example
├── .gitignore
└── .venv/
```

---

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/langgraph-react-agent.git
cd langgraph-react-agent
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

### 3. Activate the virtual environment

**Windows**

```bash
.venv\Scripts\activate
```

**macOS/Linux**

```bash
source .venv/bin/activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Configure the environment

Create a `.env` file in the project root.

```
GROQ_API_KEY=your_groq_api_key
```

### 6. Run the project

```bash
python app.py
```

---

## 💬 Example Prompts

### Calculator

```
Calculate 45 * 23
```

### Time

```
What is the current time?
```

### Wikipedia

```
Search Wikipedia for Artificial Intelligence
```

### Memory

```
My name is Aakriti.
```

Later ask:

```
What is my name?
```

### PDF Summarization

```
Summarize this PDF:
/Users/username/Documents/sample.pdf
```

---

## 🧠 How It Works

1. User enters a query.
2. LangGraph ReAct Agent analyzes the request.
3. The agent decides whether to use one or more tools.
4. The selected tool executes the task.
5. The LLM generates the final response.
6. Conversation memory is stored using `MemorySaver`.

---

## 🔧 Available Tools

| Tool | Description |
|------|-------------|
| Calculator | Evaluates mathematical expressions |
| Current Time | Returns the current date and time |
| Wikipedia Search | Retrieves information from Wikipedia |
| PDF Reader | Extracts and summarizes text from PDF files |

---

## 📌 Future Improvements

- Web Search Integration
- Document Question Answering
- Streamlit or React Web Interface
- Multi-file PDF Support
- Database-backed Memory
- Voice Assistant Integration

---

## 📷 Sample Interaction

```
============================================================
🤖 AI Research Assistant (LangGraph ReAct Agent)
Type 'exit' to quit.
============================================================

You: My name is Aakriti.

Agent: Nice to meet you, Aakriti!

You: What is my name?

Agent: Your name is Aakriti.

You: Calculate 24 * 18

Agent: 432
```

---

## 👩‍💻 Author

**Aakriti Arun Parab**

B.Tech – Artificial Intelligence & Robotics  
Manipal University Jaipur

---

## 📄 License

This project is developed for educational purposes as part of a college assignment.