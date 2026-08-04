import "./App.css";
import { useState } from "react";

function App() {

  const [question, setQuestion] = useState("");

  const [messages, setMessages] = useState([
    {
      sender: "assistant",
      text: "Hello! Ask me anything."
    }
  ]);

  // One session per browser tab
  const [sessionId] = useState(() => crypto.randomUUID());

  async function sendMessage() {

    if (question.trim() === "") return;

    const currentQuestion = question;

    // Show user's message immediately
    setMessages((prev) => [
      ...prev,
      {
        sender: "user",
        text: currentQuestion
      }
    ]);

    setQuestion("");

    try {

      const response = await fetch("http://127.0.0.1:8000/ask", {

        method: "POST",

        headers: {
          "Content-Type": "application/json"
        },

        body: JSON.stringify({

          question: currentQuestion,
          session_id: sessionId

        })

      });

      const data = await response.json();

      setMessages((prev) => [

        ...prev,

        {
          sender: "assistant",
          text: data.answer
        }

      ]);

    } catch (error) {

      setMessages((prev) => [

        ...prev,

        {
          sender: "assistant",
          text: "❌ Could not connect to backend."
        }

      ]);

    }

  }

  return (

    <div className="container">

      <h1>🤖 LangGraph AI Assistant</h1>

      <div className="chat-box">

        {messages.map((msg, index) => (

          <div
            key={index}
            className={`message ${msg.sender}`}
          >

            {msg.text}

          </div>

        ))}

      </div>

      <div className="input-area">

        <input
          type="text"
          placeholder="Type your question..."
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          onKeyDown={(e) => {

            if (e.key === "Enter") {

              sendMessage();

            }

          }}
        />

        <button onClick={sendMessage}>
          Send
        </button>

      </div>

    </div>

  );

}

export default App;