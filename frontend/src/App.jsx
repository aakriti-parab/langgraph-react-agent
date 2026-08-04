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

    // Show user message
    setMessages((prev) => [
      ...prev,
      {
        sender: "user",
        text: currentQuestion
      },
      {
        sender: "assistant",
        text: ""
      }
    ]);

    setQuestion("");

    try {

      const response = await fetch(

        `http://127.0.0.1:8000/stream?question=${encodeURIComponent(currentQuestion)}&session_id=${sessionId}`

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
              text: assistantReply
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
          text: "❌ Error connecting to backend."

        };

        return updated;

      });

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