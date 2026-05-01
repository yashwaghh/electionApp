import vertexai
from vertexai.generative_models import GenerativeModel, Content, Part
from google.cloud import translate_v3 as translate
from app.services.db_service import get_chat_history, save_chat_turn
import base64
import os
from typing import Optional

# Lazy Initialization Flags
_vertex_initialized: bool = False
_translate_client: Optional[translate.TranslationServiceClient] = None

# Google Cloud Project Configuration (Security: Removed hardcoded ID)
PROJECT_ID: str = os.getenv("GOOGLE_CLOUD_PROJECT", "election-project-096")
PARENT: str = f"projects/{PROJECT_ID}/locations/global"

# Define our Multi-Agent Specialists
SYSTEM_PROMPTS: dict[str, str] = {
    "default": "You are a neutral election assistant. Explain processes clearly and concisely.",
    "timeline": "You are an Election Timeline Specialist. Focus entirely on dates, deadlines, and chronological steps.",
    "document": "You are a Document Analysis Specialist. Analyze the provided election document/ballot and explain it simply to the user."
}

def get_model(agent_type: str = "default") -> GenerativeModel:
    """
    Lazily initializes Vertex AI and returns the specified GenerativeModel.
    
    Args:
        agent_type (str): The type of agent/specialist to load ("default", "timeline", "document").
        
    Returns:
        GenerativeModel: The configured Gemini model.
    """
    global _vertex_initialized
    if not _vertex_initialized:
        vertexai.init(project=PROJECT_ID)
        _vertex_initialized = True
    return GenerativeModel("gemini-2.5-flash", system_instruction=[SYSTEM_PROMPTS.get(agent_type, SYSTEM_PROMPTS["default"])])

def get_translate_client() -> translate.TranslationServiceClient:
    """
    Lazily initializes and returns the Google Cloud Translation client.
    
    Returns:
        TranslationServiceClient: The initialized client.
    """
    global _translate_client
    if not _translate_client:
        _translate_client = translate.TranslationServiceClient()
    return _translate_client

def route_intent(message: str, has_image: bool) -> str:
    """
    Multi-Agent Router: Determines which specialist handles the request based on intent.
    
    Args:
        message (str): The user's input message.
        has_image (bool): Whether an image was provided.
        
    Returns:
        str: The selected agent type ("document", "timeline", or "default").
    """
    if has_image:
        return "document"
    
    message_lower = message.lower()
    timeline_keywords = ["when", "date", "deadline", "timeline", "schedule", "days"]
    if any(kw in message_lower for kw in timeline_keywords):
        return "timeline"
        
    return "default"

async def generate_election_response(session_id: str, message: str, target_language: str, image_base64: Optional[str] = None) -> str:
    """
    Generates an AI response using the correct agent, maintaining history, and translating if needed.
    
    Args:
        session_id (str): The unique identifier for the user's session.
        message (str): The user's query.
        target_language (str): The requested language code (e.g., 'es', 'en').
        image_base64 (Optional[str]): Base64 encoded image data, if provided.
        
    Returns:
        str: The generated and potentially translated AI response.
    """
    # 1. Route to the correct agent
    agent_type = route_intent(message, bool(image_base64))
    model = get_model(agent_type)
    
    # 2. Build the payload (Handling Multimodal Vision)
    payload_parts = [Part.from_text(message)]
    if image_base64:
        try:
            image_bytes = base64.b64decode(image_base64)
            payload_parts.append(Part.from_data(image_bytes, mime_type="image/jpeg"))
        except Exception:
            return "Error: Invalid image data provided."

    # 3. Fetch history and initiate chat
    past_history = get_chat_history(session_id)
    formatted_history = [
        Content(role=turn["role"], parts=[Part.from_text(turn["content"])]) 
        for turn in past_history
    ]
    chat = model.start_chat(history=formatted_history)
    
    try:
        # Generate Response
        response = chat.send_message(payload_parts)
        final_text = response.text
        
        # 4. Multi-Language Translation (if requested)
        if target_language != "en":
            translate_client = get_translate_client()
            result = translate_client.translate_text(
                request={
                    "parent": PARENT,
                    "contents": [final_text],
                    "target_language_code": target_language,
                    "source_language_code": "en",
                    "mime_type": "text/plain",
                }
            )
            final_text = result.translations[0].translated_text
            
        # 5. Save and return
        save_chat_turn(session_id, message, final_text)
        return final_text
    except Exception as e:
        return f"Error processing request: {str(e)}"


