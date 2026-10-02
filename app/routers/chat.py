import uuid
from fastapi import APIRouter,HTTPException,Depends


from app.services.rag_service import answer_question
from app.schemas.chat import RequestChat,ResponseChat
from app.services.redis_service import get_conversation, get_chat_sessions
from app.services.redis_service import add_conversation
from app.services.auth_service import get_current_user


chat_app = APIRouter(prefix="/chat",tags=["Main_Chat"])

@chat_app.get("/sessions")
def get_chat_sessions_api(
    current_user: dict = Depends(get_current_user)
):
    return get_chat_sessions()

@chat_app.get("/sessions/{session_id}")
def get_chat_session(
    session_id: str,
    current_user: dict = Depends(get_current_user)
):
    conversation = get_conversation(session_id)

    return {
        "session_id": session_id,
        "conversation": conversation
    }

@chat_app.post("/main_chat",response_model=ResponseChat)
def main_chat(request_chat : RequestChat,current_user: dict = Depends(get_current_user)):
    session_id =request_chat.session_id
    # if session_id ==None or session_id=="" :
    if not session_id:
        session_id = str(uuid.uuid4())
    conversation_history = get_conversation(session_id)

    answer, retrieved_chunks = answer_question(
        request_chat.user_query,
        conversation_history
    )
    if retrieved_chunks !=[]:
        sources = [
            f"{chunk['source']} - Page {chunk['page']}"
            for chunk in retrieved_chunks
        ]
    else:
        sources =[]
    add_conversation(
        session_id,
        request_chat.user_query,
        answer
    )
    return {
        "session_id":session_id,
        "final_answer":answer,
        "sources":sources

        }