from pydantic import BaseModel
from typing import List, Dict, Optional

class ChatRequest(BaseModel):
    query: str
    session_id: Optional[str] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "query": "What is Azure Cognitive Search?",
                "session_id": "session_123"
            }
        }

class ChatResponse(BaseModel):
    message: str
    sources: List[Dict] = []
    
    class Config:
        json_schema_extra = {
            "example": {
                "message": "Azure Cognitive Search is...",
                "sources": [
                    {
                        "content": "...",
                        "metadata": {},
                        "score": 0.95
                    }
                ]
            }
        }
