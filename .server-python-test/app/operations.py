# server/app/chain_operations.py

import os
from typing import Dict, Any, List
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain.vectorstores import DocArrayInMemorySearch
from langchain.schema.runnable import RunnableMap

# Configure the API key
def configure_api_key(api_key: str) -> None:
    """
    Configures and sets the API key for service access.
    
    Args:
    - api_key: str
    
    Side Effects:
    - Sets the API key in the environment, which is required for langchain calls
    """
    os.environ["GOOGLE_API_KEY"] = api_key

# Get embeddings function - effects are unavoidable due to IO operations
def get_google_genai_embeddings(model_name: str) -> GoogleGenerativeAIEmbeddings:
    """
    Initializes the embeddings model.
    
    Args:
    - model_name: str
    
    Returns: GoogleGenerativeAIEmbeddings
    
    Side Effects:
    - Instantiates a GoogleGenerativeAIEmbeddings model which loads embeddings from an external service
    """
    return GoogleGenerativeAIEmbeddings(model=model_name)

# Embedding document texts - effects are unavoidable due to IO operations
def embed_documents(texts: List[str], embeddings_model: GoogleGenerativeAIEmbeddings) -> DocArrayInMemorySearch:
    """
    Embeds provided document texts.
    
    Args:
    - texts: List[str]
    - embeddings_model: GoogleGenerativeAIEmbeddings
    
    Returns: DocArrayInMemorySearch
    
    Side Effects:
    - Creates a vector store with embeddings generated from an external service
    """
    vectorstore = DocArrayInMemorySearch.from_texts(texts, embeddings_model)
    return vectorstore

# RunnableMap setup
def setup_runnable_map(model_name: str, temperature: float) -> RunnableMap:
    """
    Sets up a RunnableMap using a particular model.
    
    Args:
    - model_name: str
    - temperature: float
    
    Returns: RunnableMap
    """
    chat_model = ChatGoogleGenerativeAI(model=model_name, temperature=temperature)
    return RunnableMap({
        "model": chat_model
    })

# Chain invocation - involves effects due to IO operations
def invoke_chain(question: str, vectorstore: DocArrayInMemorySearch, chain: RunnableMap) -> Any:
    """
    Invokes the chain to process input and generate a response.
    
    Args:
    - question: str
    - vectorstore: DocArrayInMemorySearch
    - chain: RunnableMap
    
    Returns: The response from invoking the chain
    
    Side Effects:
    - Runs through the RunnableMap which performs IO operations to generate a response
    """
    context = vectorstore.get_relevant_documents(question)  # Retrieves document context (effectful)
    
    # Transform the input question to the format expected by the chain
    formatted_input = {
        "context": context,
        "question": question
    }
    
    # Invoke the chain with the formatted input
    response = chain.invoke(formatted_input)
    
    return response