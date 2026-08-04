from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

from graph import get_agent

app = FastAPI(
    title="LangGraph ReAct API",
    version="1.0.0"
)

agent = get_agent()


class QuestionRequest(BaseModel):
    question: str
    session_id: str


@app.get("/")
def home():
    return {
        "message": "LangGraph ReAct API is running!"
    }


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


@app.get("/stream")
def stream(question: str, session_id: str):

    return StreamingResponse(
        generate_stream(question, session_id),
        media_type="text/event-stream"
    )