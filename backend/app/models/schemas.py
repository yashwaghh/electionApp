from pydantic import BaseModel, Field
from typing import Optional

class ChatRequest(BaseModel):
    message: str = Field(..., description="User query.")
    session_id: str = Field(..., description="Session identifier.")
    language: str = Field(default="en", description="Target language code (e.g., 'es', 'hi').")
    image_base64: Optional[str] = Field(default=None, description="Base64 encoded image string.")

class ChatResponse(BaseModel):
    reply: str
    session_id: str
