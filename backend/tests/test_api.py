from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_health_check():
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy", "service": "election-assistant-api"}


def test_chat_empty_message():
    response = client.post(
        "/api/v1/chat",
        json={"session_id": "test_session_123", "message": " "}
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Message cannot be empty."


def test_chat_missing_session():
    response = client.post(
        "/api/v1/chat",
        json={"message": "How do I vote?"}
    )
    # Pydantic should catch the missing session_id
    assert response.status_code == 422


def test_chat_with_language_field():
    """Verify the new language field is accepted by Pydantic."""
    response = client.post(
        "/api/v1/chat",
        json={"session_id": "test_lang", "message": " ", "language": "es"}
    )
    # Should still fail on empty message validation, not schema
    assert response.status_code == 400


def test_chat_with_image_field():
    """Verify the new image_base64 field is accepted by Pydantic."""
    response = client.post(
        "/api/v1/chat",
        json={"session_id": "test_img", "message": " ", "image_base64": "abc123"}
    )
    # Should still fail on empty message validation, not schema
    assert response.status_code == 400
