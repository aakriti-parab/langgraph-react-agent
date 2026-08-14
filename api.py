from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
import logging

from langchain_core.messages import AIMessageChunk
from graph import get_agent


# =================================================
# Logging
# =================================================

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


# =================================================
# FastAPI
# =================================================

app = FastAPI(
    title="LangGraph ReAct API",
    version="1.0.0"
)


# =================================================
# CORS
# =================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# =================================================
# LangGraph Agent
# =================================================

agent = get_agent()


# =================================================
# Request Model
# =================================================

class QuestionRequest(BaseModel):
    question: str
    session_id: str


# =================================================
# Home Endpoint
# =================================================

@app.get("/")
def home():
    return {
        "message": "LangGraph ReAct API is running!"
    }


# =================================================
# Ask Endpoint
# =================================================

@app.post("/ask")
def ask_question(request: QuestionRequest):

    # ---------------------------------------------
    # Validate question
    # ---------------------------------------------

    if not request.question.strip():

        logger.warning(
            "Empty question received. session_id=%s",
            request.session_id
        )

        raise HTTPException(
            status_code=400,
            detail="Question cannot be empty."
        )

    # ---------------------------------------------
    # Validate session ID
    # ---------------------------------------------

    if not request.session_id.strip():

        logger.warning(
            "Missing session_id received."
        )

        raise HTTPException(
            status_code=400,
            detail="Session ID is required."
        )

    # ---------------------------------------------
    # LangGraph configuration
    # ---------------------------------------------

    config = {
        "configurable": {
            "thread_id": request.session_id
        }
    }

    try:

        logger.info(
            "Processing question. session_id=%s",
            request.session_id
        )

        # -----------------------------------------
        # Run agent
        # -----------------------------------------

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

        # -----------------------------------------
        # Get final answer
        # -----------------------------------------

        answer = response["messages"][-1].content

        logger.info(
            "Question processed successfully. session_id=%s",
            request.session_id
        )

        return {
            "success": True,
            "session_id": request.session_id,
            "question": request.question,
            "answer": answer
        }

    except Exception:

        # -----------------------------------------
        # Log complete traceback on backend
        # -----------------------------------------

        logger.exception(
            "Agent execution failed. session_id=%s",
            request.session_id
        )

        # -----------------------------------------
        # Do NOT expose raw exception
        # -----------------------------------------

        raise HTTPException(
            status_code=500,
            detail="Something went wrong while processing your request. Please try again."
        )


# =================================================
# Streaming Generator
# =================================================

def generate_stream(
    question: str,
    session_id: str
):

    config = {
        "configurable": {
            "thread_id": session_id
        }
    }

    try:

        logger.info(
            "Starting streaming request. session_id=%s",
            session_id
        )

        # -----------------------------------------
        # Stream LangGraph response
        # -----------------------------------------

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

            # -------------------------------------
            # Only process AI message chunks
            # -------------------------------------

            if not isinstance(chunk, AIMessageChunk):
                continue

            if not chunk.content:
                continue

            # -------------------------------------
            # Send token to frontend
            # -------------------------------------

            yield f"data: {chunk.content}\n\n"

        # -----------------------------------------
        # Streaming completed
        # -----------------------------------------

        logger.info(
            "Streaming completed successfully. session_id=%s",
            session_id
        )

        yield "data: [DONE]\n\n"

    except Exception:

        # -----------------------------------------
        # Log complete traceback
        # -----------------------------------------

        logger.exception(
            "Streaming failed. session_id=%s",
            session_id
        )

        # -----------------------------------------
        # Do NOT expose raw exception
        # -----------------------------------------

        yield (
            "event: error\n"
            "data: Something went wrong while processing your request. "
            "Please try again.\n\n"
        )


# =================================================
# Streaming Endpoint
# =================================================

@app.post("/stream")
def stream(request: QuestionRequest):

    # ---------------------------------------------
    # Validate question BEFORE streaming starts
    # ---------------------------------------------

    if not request.question.strip():

        logger.warning(
            "Empty streaming question received. session_id=%s",
            request.session_id
        )

        raise HTTPException(
            status_code=400,
            detail="Question cannot be empty."
        )

    # ---------------------------------------------
    # Validate session ID BEFORE streaming starts
    # ---------------------------------------------

    if not request.session_id.strip():

        logger.warning(
            "Missing session_id for streaming request."
        )

        raise HTTPException(
            status_code=400,
            detail="Session ID is required."
        )

    # ---------------------------------------------
    # Log request
    # ---------------------------------------------

    logger.info(
        "Stream endpoint called. session_id=%s",
        request.session_id
    )

    # ---------------------------------------------
    # Start streaming response
    # ---------------------------------------------

    return StreamingResponse(
        generate_stream(
            request.question,
            request.session_id
        ),
        media_type="text/event-stream"
    )