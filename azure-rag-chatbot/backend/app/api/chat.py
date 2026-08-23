from fastapi import APIRouter, HTTPException
from app.models.chat import ChatRequest, ChatResponse
from app.services.azure_search import AzureSearchService
from app.services.azure_foundry import AzureFoundryService

router = APIRouter()

@router.post("/", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Handle chat requests with RAG (Retrieval-Augmented Generation)
    """
    try:
        # Retrieve relevant documents from Azure Search
        search_service = AzureSearchService()
        documents = search_service.search(request.query)
        
        # Generate response using Azure OpenAI
        foundry_service = AzureFoundryService()
        response = foundry_service.generate_response(
            query=request.query,
            context=documents
        )
        
        return ChatResponse(
            message=response,
            sources=documents
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
