Oh my God, I totally and completely forgot about this project!! Please generate good notes I'd write for myself. This was so early on too :()

# META: GEMINI-CHAT

## Folder Structure

```plaintext
/Users/jasonnathan/Repos/gemini-chat
├── activate -> /Users/jasonnathan/.virtualenvs/gemini-chat/bin/activate
├── list.sh
└── main.py

1 directory, 3 files
```

## File: main.py

```py
from IPython.display import display
from IPython.display import Markdown
import textwrap
import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_google_genai import GoogleGenerativeAIEmbeddings


def to_markdown(text):
  text = text.replace('•', '  *')
  return Markdown(textwrap.indent(text, '> ', predicate=lambda _: True))

llm = ChatGoogleGenerativeAI(model="gemini-pro", google_api_key=os.environ.get("GOOGLE_API_KEY"))
result = llm.invoke("What is the best practice to keep fit?")
to_markdown(result.content)
```

## File: .server-python-test/app/api.py

```python
import os
import google.generativeai as genai

# Configuring the API Key for generativeai
def configure_api_key(api_key: str):
    os.environ["GOOGLE_API_KEY"] = api_key
    genai.configure(api_key=api_key)

# List available models
def get_available_models():
    return genai.models.list_models()

# Generate content from a provided prompt
def generate_content(prompt: str, model_name: str = 'gemini-pro'):
    generative_model = genai.GenerativeModel(model_name)
    response = generative_model.generate_content(prompt)
    return response.text
```

## File: .server-python-test/app/chatbot.py

```python
# Imports from langchain and google-generativeai should be organized at the top of the file
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain.vectorstores import DocArrayInMemorySearch
from langchain.schema.runnable import RunnableMap
from langchain.prompts import ChatPromptTemplate

# Function to generate content using Google Generative AI model
def generate_content_with_model(prompt: str, model_name: str = 'gemini-pro') -> str:
    """
    Generates content using the specified Generative AI model. This is an effectful function.
    
    Args:
        prompt: The input prompt for the model to generate content.
        model_name: The model name to use for content generation (defaulted to 'gemini-pro').
        
    Returns:
        The generated content as a string.
    """
    model = ChatGoogleGenerativeAI(model=model_name)
    response = model.generate_content(prompt)
    return response.text

# Function to set up embeddings vector store
def setup_embeddings(doc_texts: list, embedding_model: str = 'models/embedding-001'):
    """
    Sets up the embeddings vector store based on provided documents and a specified embedding model.
    
    Args:
        doc_texts: A list of strings representing text documents to be embedded.
        embedding_model: The name of the embedding model to use.
        
    Returns:
        A DocArrayInMemorySearch vector store instance.
    """
    embeddings = GoogleGenerativeAIEmbeddings(model=embedding_model)
    vectorstore = DocArrayInMemorySearch.from_texts(doc_texts, embeddings)
    return vectorstore

# Function to retrieve relevant documents
def retrieve_documents(retriever, query: str) -> list:
    """
    Retrieves documents relevant to the given query.
    
    Args:
        retriever: The retriever instance from a vector store.
        query: The query for which relevant documents should be found.
    
    Returns:
        A list of relevant documents.
    """
    return retriever.get_relevant_documents(query)

# Function to create a chat prompt template
def chat_prompt_from_template(template: str):
    """
    Creates a formatted chat prompt from the given template.
    
    Args:
        template: A string template that includes place holders for context and questions.
        
    Returns:
        A formatted chat prompt ready to interface with a generative model.
    """
    # Assuming you've instantiated a ChatPromptTemplate from a template string
    # ChatPromptTemplate should be defined elsewhere or imported if it's a third-party package
    return ChatPromptTemplate.from_template(template)

# Function to invoke a Runnable Map with models
def invoke_runnable_map(question: str, retriever):
    """
    Invokes the RunnableMap to process a chain of actions and generate a response to a question.
    
    Args:
        question: The question to provide context for and generate a response.
        retriever: The retriever instance to use for finding relevant documents.
        
    Returns:
        The result of invoking the RunnableMap, which includes the model's response.
    """
    chain = RunnableMap({
        "context": lambda x: retriever.get_relevant_documents(x["question"]),
        "question": lambda x: x["question"]
    }) # | prompt | model | output_parser
    # "| prompt | model | output_parser" - You should create or define these, assuming they are transformations or operations on the chain
    chain.invoke({"question": question})

# Assuming you have the retrieval mechanism and other necessary pieces ready, further refactoring would focus on the chain 
# of operations that transforms an incoming question into a response, which could involve the steps mocked out above.
```

## File: .server-python-test/app/embedder.py

```python
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
```

## File: .server-python-test/app/operations.py

```python
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
```

## File: .server-python-test/app/retriever.py

```python
from langchain.prompts import ChatPromptTemplate
from langchain.schema.runnable import RunnableMap


# Function to create a prompt template
def create_prompt_template(template_str: str):
    return ChatPromptTemplate.from_template(template_str)

# Function that sets up a retrievable process, acquiring context for questions
def make_retrievable(retriever, template_str: str):
    prompt = create_prompt_template(template_str)  # Now using ChatPromptTemplate
    
    # Define a lambda function for context retrieval
    context_retriever = lambda x: {'context': retriever.get_relevant_documents(x['question'])}
    
    # Using a lambda for question extraction
    question_extractor = lambda x: {'question': x['question']}
    
    # Combine the above functions into a runnable map for processing
    chain_context = RunnableMap({
        "context": context_retriever,
        "question": question_extractor
    }) | prompt.template
    
    return chain_context
```

## File: .server-python-test/test/test_api.py

```python
import unittest
import os
from unittest.mock import patch
from server.app.api import generate_content, configure_api_key, get_available_models

class TestAPI(unittest.TestCase):

    @patch('server.app.api.genai.GenerativeModel')
    def test_generate_content(self, mock_model):
        mock_response = mock_model.return_value.generate_content.return_value
        mock_response.text = 'This is a response'
        
        response = generate_content('Who are you?')
        
        assert response == 'This is a response'
        
    def test_configure_api_key(self):
        api_key = "my_api_key"
        
        configure_api_key(api_key)
        
        self.assertEqual(os.environ["GOOGLE_API_KEY"], api_key)

    @patch('genai.list_models')
    def test_get_available_models(self, mock_list_models):
        mock_list_models.return_value = ['model1', 'model2', 'model3']
        
        result = get_available_models()
        
        self.assertEqual(result, ['model1', 'model2', 'model3'])
        mock_list_models.assert_called_once()


if __name__ == '__main__':
    unittest.main()
```


## FIle: ./list.sh

```
#!/bin/bash

function list_structure() {
  local dir="$1"
  for entry in "$dir"/*; do
    if [[ -d "$entry" && "$entry" != "venv" ]]; then
      if [[ ! "$entry" =~ (lib|bin|include) ]]; then
        echo "│  $entry"
        list_structure "$entry"
      fi
    else
      echo "└── $entry"
    fi
  done
}

list_structure .
```

## Git Repository

```plaintext
origin	https://github.com/jasonnathan/gemini-chat.git (fetch)
origin	https://github.com/jasonnathan/gemini-chat.git (push)
```


