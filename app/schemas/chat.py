from pydantic import BaseModel,Field


class RequestChat(BaseModel):
    user_query : str = Field(...,min_length=1)
    session_id : str | None = None


class ResponseChat(BaseModel):
    session_id: str
    final_answer :str
    sources: list[str]
