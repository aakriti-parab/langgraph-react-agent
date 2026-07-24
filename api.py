from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

from graph import get_agent

app = FastAPI(
    title="LangGraph ReAct API",
    version="1.0.0"
)

agent = get_agent()

config = {
    "configurable": {
        "thread_id": "user-1"
    }
}


class QuestionRequest(BaseModel):
    question: str


@app.get("/")
def home():
    return {
        "message": "LangGraph ReAct API is running!"
    }


@app.post("/ask")
def ask_question(request: QuestionRequest):
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
            "question": request.question,
            "answer": answer
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


def generate_stream(question: str):
    """
    Streams the AI response token by token using LangGraph + SSE.
    """

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

            # Ignore empty chunks
            if not chunk.content:
                continue

            yield f"data: {chunk.content}\n\n"

        # Notify browser that streaming has finished
        yield "data: [DONE]\n\n"

    except Exception as e:
        yield f"data: Error: {str(e)}\n\n"


@app.get("/stream")
def stream(question: str):
    return StreamingResponse(
        generate_stream(question),
        media_type="text/event-stream"
    )