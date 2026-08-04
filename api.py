from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
import logging

from graph import get_agent

# -------------------------------------------------
# Logging
# -------------------------------------------------

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)

# -------------------------------------------------
# FastAPI
# -------------------------------------------------

app = FastAPI(
    title="LangGraph ReAct API",
    version="1.0.0"
)

# -------------------------------------------------
# CORS
# -------------------------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------------------------------------
# LangGraph Agent
# -------------------------------------------------

agent = get_agent()

# -------------------------------------------------
# Models
# -------------------------------------------------

class QuestionRequest(BaseModel):
    question: str
    session_id: str


# -------------------------------------------------
# Home
# -------------------------------------------------

@app.get("/")
def home():
    return {
        "message": "LangGraph ReAct API is running!"
    }


# -------------------------------------------------
# Ask Endpoint
# -------------------------------------------------

@app.post("/ask")
def ask_question(request: QuestionRequest):

    if request.question.strip() == "":
        raise HTTPException(
            status_code=400,
            detail="Question cannot be empty."
        )

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

    except Exception:

        logger.exception("Agent execution failed")

        raise HTTPException(
            status_code=500,
            detail="Internal Server Error. Please try again."
        )


# -------------------------------------------------
# Streaming Generator
# -------------------------------------------------

def generate_stream(question: str, session_id: str):

    if question.strip() == "":
        yield "data: Error: Question cannot be empty.\n\n"
        return

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

    except Exception:

        logger.exception("Streaming failed")

        yield "data: Internal Server Error\n\n"


# -------------------------------------------------
# Stream Endpoint
# -------------------------------------------------

@app.get("/stream")
def stream(question: str, session_id: str):

    return StreamingResponse(
        generate_stream(question, session_id),
        media_type="text/event-stream"
    )