from unittest.mock import patch

from fastapi.testclient import TestClient

from api import app

client = TestClient(app)


# --------------------------------------------------
# Home Endpoint
# --------------------------------------------------

def test_home():

    response = client.get("/")

    assert response.status_code == 200

    assert response.json() == {
        "message": "LangGraph ReAct API is running!"
    }


# --------------------------------------------------
# Empty Question
# --------------------------------------------------

def test_empty_question():

    response = client.post(
        "/ask",
        json={
            "question": "",
            "session_id": "abc123"
        }
    )

    assert response.status_code == 400

    assert response.json()["detail"] == "Question cannot be empty."


# --------------------------------------------------
# Missing Session ID
# --------------------------------------------------

def test_missing_session_id():

    response = client.post(
        "/ask",
        json={
            "question": "Hello"
        }
    )

    assert response.status_code == 422


# --------------------------------------------------
# Mock Agent
# --------------------------------------------------

@patch("api.agent.invoke")
def test_valid_question(mock_invoke):

    class FakeMessage:

        content = "Hello from mocked agent"

    mock_invoke.return_value = {
        "messages": [
            FakeMessage()
        ]
    }

    response = client.post(
        "/ask",
        json={
            "question": "Hello",
            "session_id": "abc123"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["success"] is True

    assert data["answer"] == "Hello from mocked agent"