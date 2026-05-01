from google.cloud import firestore
import os

# Lazy-initialized Firestore client using the specific project ID
_db = None


def _get_db():
    """Lazily initialize Firestore client to avoid import-time GCP auth errors."""
    global _db
    if _db is None:
        project_id = os.getenv("GOOGLE_CLOUD_PROJECT", "election-project-096")
        _db = firestore.Client(project=project_id)
    return _db


def save_chat_turn(session_id: str, user_message: str, ai_response: str):
    """Saves a single turn of conversation to Firestore."""
    db = _get_db()
    doc_ref = db.collection("chat_sessions").document(session_id)
    # Using ArrayUnion to append to the conversation history
    doc_ref.set({
        "history": firestore.ArrayUnion([
            {"role": "user", "content": user_message},
            {"role": "model", "content": ai_response}
        ])
    }, merge=True)


def get_chat_history(session_id: str):
    """Retrieves the conversation history for a given session."""
    db = _get_db()
    doc = db.collection("chat_sessions").document(session_id).get()
    if doc.exists:
        return doc.to_dict().get("history", [])
    return []
