from fastapi import APIRouter, HTTPException
from app.models.schemas import ChatRequest, ChatResponse
from app.services.llm_service import generate_election_response

router = APIRouter()

@router.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    if not request.message.strip():
        raise HTTPException(status_code=400, detail="Message cannot be empty.")

    reply_text = await generate_election_response(
        session_id=request.session_id,
        message=request.message,
        target_language=request.language,
        image_base64=request.image_base64
    )

    return ChatResponse(reply=reply_text, session_id=request.session_id)

@router.get("/health")
async def health_check():
    return {"status": "healthy", "service": "election-assistant-api"}
