from fastapi.testclient import TestClient
from app.main import app
from unittest.mock import patch

client = TestClient(app)


def test_health_check():
    """Verify health endpoint returns 200 OK and expected payload."""
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy", "service": "election-assistant-api"}


def test_chat_empty_message():
    """Verify empty message requests are rejected."""
    response = client.post(
        "/api/v1/chat",
        json={"session_id": "test_session_123", "message": " "}
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Message cannot be empty."


def test_chat_missing_session():
    """Verify missing session_id triggers a Pydantic validation error."""
    response = client.post(
        "/api/v1/chat",
        json={"message": "How do I vote?"}
    )
    assert response.status_code == 422


def test_chat_with_language_field():
    """Verify the language field is accepted by Pydantic."""
    response = client.post(
        "/api/v1/chat",
        json={"session_id": "test_lang", "message": " ", "language": "es"}
    )
    assert response.status_code == 400


def test_chat_with_invalid_image_base64():
    """Verify invalid base64 image strings are handled gracefully by the LLM service."""
    # We patch generate_election_response to ensure we don't actually hit the LLM API during this test, 
    # but since the validation happens inside the service, we can test it end-to-end with a mock.
    
    # Actually, the base64 decoding happens inside generate_election_response.
    # Let's test the endpoint directly to see if the exception is caught and returned.
    response = client.post(
        "/api/v1/chat",
        json={"session_id": "test_img", "message": "Analyze this", "image_base64": "invalid_base64_!@#"}
    )
    
    # It should return 200 OK, but the reply should be the error message from the try-except block
    assert response.status_code == 200
    assert "Error: Invalid image data provided." in response.json()["reply"]

