from azure.search.documents import SearchClient
from azure.core.credentials import AzureKeyCredential
from app.config import settings
from typing import List, Dict

class AzureSearchService:
    def __init__(self):
        self.endpoint = settings.AZURE_SEARCH_ENDPOINT
        self.key = settings.AZURE_SEARCH_KEY
        self.index_name = settings.AZURE_SEARCH_INDEX
        
        # Initialize the search client
        self.client = SearchClient(
            endpoint=self.endpoint,
            index_name=self.index_name,
            credential=AzureKeyCredential(self.key)
        )
    
    def search(self, query: str, top_k: int = 5) -> List[Dict]:
        """
        Search for relevant documents in Azure Search
        """
        try:
            results = self.client.search(
                search_text=query,
                top=top_k,
                include_total_count=True
            )
            
            documents = []
            for result in results:
                documents.append({
                    "content": result.get("content", ""),
                    "metadata": result.get("metadata", {}),
                    "score": result.get("@search.score", 0)
                })
            
            return documents
        except Exception as e:
            print(f"Error searching Azure Search: {str(e)}")
            return []
