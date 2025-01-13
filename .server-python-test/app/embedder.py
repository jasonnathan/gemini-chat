from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain.vectorstores import DocArrayInMemorySearch

# Setting up embeddings using GoogleGenerativeAI Embeddings
def get_embeddings(model_name: str = 'embedding-001'):
    return GoogleGenerativeAIEmbeddings(model=model_name)

# Create vector store
def create_vector_store(texts: list, embeddings):
    vectorstore = DocArrayInMemorySearch.from_texts(texts, embedding=embeddings)
    return vectorstore

# Retrieve relevant documents based on query using vector store
def get_relevant_documents(vectorstore, query: str):
    retriever = vectorstore.as_retriever()
    return retriever.get_relevant_documents(query)