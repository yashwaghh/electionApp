import pytest
from unittest.mock import patch, MagicMock
from app.services.db_service import get_chat_history, save_chat_turn

@patch("app.services.db_service._get_db")
def test_get_chat_history(mock_get_db):
    """Test retrieving chat history."""
    # Mocking Firestore
    mock_db = MagicMock()
    mock_get_db.return_value = mock_db
    mock_collection = MagicMock()
    mock_document = MagicMock()
    mock_db.collection.return_value = mock_collection
    mock_collection.document.return_value = mock_document
    
    # Mocking Snapshot
    mock_doc_snap = MagicMock()
    mock_doc_snap.exists = True
    mock_doc_snap.to_dict.return_value = {
        "history": [
            {"role": "user", "content": "hello"},
            {"role": "model", "content": "hi there"}
        ]
    }
    mock_document.get.return_value = mock_doc_snap
    
    history = get_chat_history("session_123")
    assert len(history) == 2
    assert history[0]["role"] == "user"

@patch("app.services.db_service._get_db")
def test_get_chat_history_empty(mock_get_db):
    """Test retrieving chat history when no history exists."""
    mock_db = MagicMock()
    mock_get_db.return_value = mock_db
    mock_collection = MagicMock()
    mock_document = MagicMock()
    mock_db.collection.return_value = mock_collection
    mock_collection.document.return_value = mock_document
    
    mock_doc_snap = MagicMock()
    mock_doc_snap.exists = False
    mock_document.get.return_value = mock_doc_snap
    
    history = get_chat_history("session_456")
    assert history == []

@patch("app.services.db_service._get_db")
@patch("app.services.db_service.get_chat_history")
def test_save_chat_turn(mock_get_history, mock_get_db):
    """Test saving a new turn to history."""
    mock_get_history.return_value = []
    
    mock_db = MagicMock()
    mock_get_db.return_value = mock_db
    mock_collection = MagicMock()
    mock_document = MagicMock()
    mock_db.collection.return_value = mock_collection
    mock_collection.document.return_value = mock_document
    
    save_chat_turn("session_123", "user message", "ai response")
    
    # Verify set was called with correct data
    mock_document.set.assert_called_once()
    args, kwargs = mock_document.set.call_args
    data = args[0]
    
    # Depending on how the ArrayUnion mock interacts, it might just be the ArrayUnion object, 
    # but since this is a unit test of the db logic, we can verify set was called.
    assert "history" in data
