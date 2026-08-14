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

  // One session ID for this browser tab
  const [sessionId] = useState(() => crypto.randomUUID());

  // Automatically scroll to the latest message
  useEffect(() => {
    chatEndRef.current?.scrollIntoView({
      behavior: "smooth",
    });
  }, [messages]);

  // Suggested questions
  const suggestions = [
    "Who is Albert Einstein?",
    "What is today's date and time?",
    "Calculate 234 × 98",
    "Explain LangGraph",
  ];

  async function sendMessage(customQuestion = null) {
    const currentQuestion = customQuestion || question;

    if (currentQuestion.trim() === "") {
      return;
    }

    const time = new Date().toLocaleTimeString([], {
      hour: "2-digit",
      minute: "2-digit",
    });

    // Add user's message
    // Add an empty assistant message which will be filled while streaming
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
      // -------------------------------------------------
      // POST request
      // -------------------------------------------------

      const response = await fetch("http://127.0.0.1:8000/stream", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          question: currentQuestion,
          session_id: sessionId,
        }),
      });

      // -------------------------------------------------
      // Handle HTTP errors
      // -------------------------------------------------

      if (!response.ok) {
        let errorMessage = "Something went wrong.";

        try {
          const errorData = await response.json();

          if (errorData.detail) {
            errorMessage = errorData.detail;
          }
        } catch {
          errorMessage = "Server returned an error.";
        }

        setMessages((prev) => {
          const updated = [...prev];

          updated[updated.length - 1] = {
            sender: "assistant",
            text: `❌ ${errorMessage}`,
            time,
          };

          return updated;
        });

        return;
      }

      // -------------------------------------------------
      // Read streaming response
      // -------------------------------------------------

      if (!response.body) {
        throw new Error("No response body received from server.");
      }

      const reader = response.body.getReader();
      const decoder = new TextDecoder();

      let assistantReply = "";
      let buffer = "";

      while (true) {
        const { done, value } = await reader.read();

        if (done) {
          break;
        }

        // Decode incoming bytes
        buffer += decoder.decode(value, {
          stream: true,
        });

        // Split complete SSE lines
        const lines = buffer.split("\n");

        // Keep the last incomplete line in buffer
        buffer = lines.pop() || "";

        for (let line of lines) {
          line = line.trim();

          if (!line.startsWith("data:")) {
            continue;
          }

          const token = line.replace(/^data:\s?/, "");

          // Streaming finished
          if (token === "[DONE]") {
            continue;
          }

          assistantReply += token;

          // Update the last assistant message
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

      // Process any remaining buffered data
      if (buffer.trim().startsWith("data:")) {
        const token = buffer
          .trim()
          .replace(/^data:\s?/, "");

        if (token !== "[DONE]") {
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
      console.error("Frontend error:", error);

      setMessages((prev) => {
        const updated = [...prev];

        updated[updated.length - 1] = {
          sender: "assistant",
          text: "❌ Unable to connect to the backend.",
          time,
        };

        return updated;
      });
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="container">

      {/* -------------------------------------------------
          Header
      ------------------------------------------------- */}

      <header className="header">
        <h1>🤖 LangGraph AI Assistant</h1>

        <p className="subtitle">
          Powered by LangGraph • Groq • FastAPI • React
        </p>
      </header>


      {/* -------------------------------------------------
          Suggestions
      ------------------------------------------------- */}

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


      {/* -------------------------------------------------
          Chat
      ------------------------------------------------- */}

      <div className="chat-box">

        {messages.map((msg, index) => (
          <div
            key={index}
            className={`chat-row ${msg.sender}`}
          >

            {/* Avatar */}

            <div className="avatar">
              {msg.sender === "assistant"
                ? "🤖"
                : "👤"}
            </div>


            {/* Message */}

            <div
              className={`message ${msg.sender}`}
            >
              <div>
                {msg.text}
              </div>

              <span className="time">
                {msg.time}
              </span>
            </div>

          </div>
        ))}


        {/* Typing indicator */}

        {loading && (
          <div className="chat-row assistant">

            <div className="avatar">
              🤖
            </div>

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


      {/* -------------------------------------------------
          Input
      ------------------------------------------------- */}

      <div className="input-area">

        <textarea
          rows="2"
          placeholder="Ask anything..."
          value={question}
          onChange={(e) =>
            setQuestion(e.target.value)
          }
          onKeyDown={(e) => {

            if (
              e.key === "Enter" &&
              !e.shiftKey
            ) {
              e.preventDefault();
              sendMessage();
            }

          }}
        />


        <button
          onClick={() => sendMessage()}
          disabled={loading}
        >
          {loading
            ? "Thinking..."
            : "➤"}
        </button>

      </div>

    </div>
  );
}

export default App;