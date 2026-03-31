from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_health_endpoint_returns_ok_status() -> None:
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_chat_endpoint_returns_structured_response() -> None:
    response = client.post(
        "/api/chat",
        json={
            "question": "我最近有点头痛，需要注意什么？",
            "session_id": "session-1",
        },
    )

    assert response.status_code == 200

    payload = response.json()
    assert payload["mode"] == "answer"
    assert payload["risk_level"] == "medium"
    assert payload["answer"]
    assert payload["citations"] == []
    assert payload["follow_up_question"] is None
    assert payload["disclaimer"]
    assert payload["trace_id"]
