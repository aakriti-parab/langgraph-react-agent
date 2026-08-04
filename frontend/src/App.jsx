import "./App.css";
import { useEffect, useRef, useState } from "react";

function App() {
  const [question, setQuestion] = useState("");
  const [loading, setLoading] = useState(false);

  const chatEndRef = useRef(null);

  const [messages, setMessages] = useState([
    {
      sender: "assistant",
      text: "Hello! Ask me anything.",
      time: new Date().toLocaleTimeString([], {
        hour: "2-digit",
        minute: "2-digit",
      }),
    },
  ]);

  const [sessionId] = useState(() => crypto.randomUUID());

  useEffect(() => {
    chatEndRef.current?.scrollIntoView({
      behavior: "smooth",
    });
  }, [messages]);

  const suggestions = [
    "Who is Albert Einstein?",
    "What is today's date and time?",
    "Calculate 234 × 98",
    "Explain LangGraph",
  ];

  async function sendMessage(customQuestion = null) {
    const currentQuestion = customQuestion || question;

    if (currentQuestion.trim() === "") return;

    const time = new Date().toLocaleTimeString([], {
      hour: "2-digit",
      minute: "2-digit",
    });

    setMessages((prev) => [
      ...prev,
      {
        sender: "user",
        text: currentQuestion,
        time,
      },
      {
        sender: "assistant",
        text: "",
        time,
      },
    ]);

    setQuestion("");
    setLoading(true);

    try {
      const response = await fetch(
        `http://127.0.0.1:8000/stream?question=${encodeURIComponent(
          currentQuestion
        )}&session_id=${sessionId}`
      );

      const reader = response.body.getReader();
      const decoder = new TextDecoder();

      let assistantReply = "";

      while (true) {
        const { done, value } = await reader.read();

        if (done) break;

        const chunk = decoder.decode(value);

        const lines = chunk.split("\n");

        for (let line of lines) {
          if (!line.startsWith("data: ")) continue;

          const token = line.replace("data: ", "");

          if (token === "[DONE]") continue;

          assistantReply += token;

          setMessages((prev) => {
            const updated = [...prev];

            updated[updated.length - 1] = {
              sender: "assistant",
              text: assistantReply,
              time,
            };

            return updated;
          });
        }
      }
    } catch (error) {
      setMessages((prev) => {
        const updated = [...prev];

        updated[updated.length - 1] = {
          sender: "assistant",
          text: "❌ Error connecting to backend.",
          time,
        };

        return updated;
      });
    }

    setLoading(false);
  }

  return (
    <div className="container">
      <header className="header">
        <h1>🤖 LangGraph AI Assistant</h1>

        <p className="subtitle">
          Powered by LangGraph • Groq • FastAPI • React
        </p>
      </header>

      {messages.length === 1 && (
        <div className="suggestions">
          {suggestions.map((item, index) => (
            <button
              key={index}
              onClick={() => sendMessage(item)}
            >
              {item}
            </button>
          ))}
        </div>
      )}

      <div className="chat-box">
        {messages.map((msg, index) => (
          <div
            key={index}
            className={`chat-row ${msg.sender}`}
          >
            <div className="avatar">
              {msg.sender === "assistant" ? "🤖" : "👤"}
            </div>

            <div className={`message ${msg.sender}`}>
              <div>{msg.text}</div>

              <span className="time">
                {msg.time}
              </span>
            </div>
          </div>
        ))}

        {loading && (
          <div className="chat-row assistant">
            <div className="avatar">🤖</div>

            <div className="message assistant">
              <div className="typing">
                <span></span>
                <span></span>
                <span></span>
              </div>
            </div>
          </div>
        )}

        <div ref={chatEndRef}></div>
      </div>

      <div className="input-area">
        <textarea
          rows="2"
          placeholder="Ask anything..."
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          onKeyDown={(e) => {
            if (e.key === "Enter" && !e.shiftKey) {
              e.preventDefault();
              sendMessage();
            }
          }}
        />

        <button
          onClick={() => sendMessage()}
          disabled={loading}
        >
          {loading ? "Thinking..." : "➤"}
        </button>
      </div>
    </div>
  );
}

export default App;