from openai import AzureOpenAI
from app.config import settings
from typing import List, Dict

class AzureFoundryService:
    def __init__(self):
        self.client = AzureOpenAI(
            api_key=settings.AZURE_OPENAI_KEY,
            api_version=settings.AZURE_OPENAI_API_VERSION,
            azure_endpoint=settings.AZURE_OPENAI_ENDPOINT
        )
        self.deployment = settings.AZURE_OPENAI_DEPLOYMENT
    
    def generate_response(self, query: str, context: List[Dict]) -> str:
        """
        Generate a response using Azure OpenAI with RAG context
        """
        try:
            # Prepare context from retrieved documents
            context_text = "\n\n".join([
                f"Source {i+1}:\n{doc.get('content', '')}"
                for i, doc in enumerate(context)
            ])
            
            # Construct the prompt
            system_prompt = """You are a helpful AI assistant. 
Answer questions based on the provided context. 
If the answer is not in the context, say so."""
            
            user_prompt = f"""Context:
{context_text}

Question: {query}

Answer:"""
            
            # Call Azure OpenAI
            response = self.client.chat.completions.create(
                model=self.deployment,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.7,
                max_tokens=1000
            )
            
            return response.choices[0].message.content
        except Exception as e:
            print(f"Error generating response: {str(e)}")
            return "I encountered an error while processing your request."
