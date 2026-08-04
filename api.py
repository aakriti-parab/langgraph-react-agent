from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

from graph import get_agent

app = FastAPI(
    title="LangGraph ReAct API",
    version="1.0.0"
)

# -------------------------------------------------------
# CORS CONFIGURATION
# Allows the React frontend to communicate with FastAPI
# -------------------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

agent = get_agent()


# -------------------------------------------------------
# REQUEST MODEL
# -------------------------------------------------------
class QuestionRequest(BaseModel):
    question: str
    session_id: str


# -------------------------------------------------------
# HOME ROUTE
# -------------------------------------------------------
@app.get("/")
def home():
    return {
        "message": "LangGraph ReAct API is running!"
    }


# -------------------------------------------------------
# NORMAL CHAT ENDPOINT
# -------------------------------------------------------
@app.post("/ask")
def ask_question(request: QuestionRequest):

    config = {
        "configurable": {
            "thread_id": request.session_id
        }
    }

    try:

        response = agent.invoke(
            {
                "messages": [
                    {
                        "role": "user",
                        "content": request.question
                    }
                ]
            },
            config=config
        )

        answer = response["messages"][-1].content

        return {
            "success": True,
            "session_id": request.session_id,
            "question": request.question,
            "answer": answer
        }

    except Exception as e:

        return {
            "success": False,
            "error": str(e)
        }


# -------------------------------------------------------
# STREAMING GENERATOR
# -------------------------------------------------------
def generate_stream(question: str, session_id: str):

    config = {
        "configurable": {
            "thread_id": session_id
        }
    }

    try:

        for chunk, metadata in agent.stream(
            {
                "messages": [
                    {
                        "role": "user",
                        "content": question
                    }
                ]
            },
            config=config,
            stream_mode="messages"
        ):

            if not chunk.content:
                continue

            yield f"data: {chunk.content}\n\n"

        yield "data: [DONE]\n\n"

    except Exception as e:

        yield f"data: Error: {str(e)}\n\n"


# -------------------------------------------------------
# STREAM ENDPOINT
# -------------------------------------------------------
@app.get("/stream")
def stream(question: str, session_id: str):

    return StreamingResponse(
        generate_stream(question, session_id),
        media_type="text/event-stream"
    )