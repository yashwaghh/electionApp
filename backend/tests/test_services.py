import pytest
from unittest.mock import patch, MagicMock
from app.services.llm_service import generate_election_response, route_intent

@pytest.mark.asyncio
async def test_route_intent_with_image():
    """Verify that providing an image overrides keyword routing."""
    intent = route_intent("when is the deadline", has_image=True)
    assert intent == "document"

@pytest.mark.asyncio
async def test_route_intent_timeline():
    """Verify timeline keywords route to the timeline specialist."""
    intent = route_intent("What is the registration deadline?", has_image=False)
    assert intent == "timeline"

@pytest.mark.asyncio
async def test_route_intent_default():
    """Verify normal queries route to the default agent."""
    intent = route_intent("How does the electoral college work?", has_image=False)
    assert intent == "default"

@pytest.mark.asyncio
@patch("app.services.llm_service.get_chat_history")
@patch("app.services.llm_service.save_chat_turn")
@patch("app.services.llm_service.get_model")
async def test_generate_election_response_success(mock_get_model, mock_save, mock_get_history):
    """Test standard response generation without translation."""
    # Mocking DB
    mock_get_history.return_value = []
    
    # Mocking Vertex AI
    mock_chat = MagicMock()
    # Important: Since we use `await chat.send_message_async()`, the mock must return a coroutine
    async def mock_send_message_async(*args, **kwargs):
        mock_response = MagicMock()
        mock_response.text = "You must register 30 days prior."
        return mock_response
        
    mock_chat.send_message_async = mock_send_message_async
    
    mock_model = MagicMock()
    mock_model.start_chat.return_value = mock_chat
    mock_get_model.return_value = mock_model
    
    response = await generate_election_response("test_session", "How to vote?", "en", None)
    assert response == "You must register 30 days prior."
    mock_save.assert_called_once_with("test_session", "How to vote?", "You must register 30 days prior.")

@pytest.mark.asyncio
@patch("app.services.llm_service.get_chat_history")
@patch("app.services.llm_service.save_chat_turn")
@patch("app.services.llm_service.get_model")
@patch("app.services.llm_service.get_translate_client")
async def test_generate_election_response_with_translation(mock_translate_client, mock_get_model, mock_save, mock_get_history):
    """Test generation followed by Google Cloud translation."""
    # Mocking DB
    mock_get_history.return_value = []
    
    # Mocking Vertex AI
    mock_chat = MagicMock()
    async def mock_send_message_async(*args, **kwargs):
        mock_response = MagicMock()
        mock_response.text = "Hello."
        return mock_response
    mock_chat.send_message_async = mock_send_message_async
    
    mock_model = MagicMock()
    mock_model.start_chat.return_value = mock_chat
    mock_get_model.return_value = mock_model
    
    # Mocking Translation Client
    mock_client_instance = MagicMock()
    mock_translation_result = MagicMock()
    mock_translation = MagicMock()
    mock_translation.translated_text = "Hola."
    mock_translation_result.translations = [mock_translation]
    mock_client_instance.translate_text.return_value = mock_translation_result
    mock_translate_client.return_value = mock_client_instance
    
    response = await generate_election_response("test_session", "Hello.", "es", None)
    assert response == "Hola."
    mock_save.assert_called_once_with("test_session", "Hello.", "Hola.")
