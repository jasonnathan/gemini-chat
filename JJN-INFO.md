# JJN-INFO: GEMINI-CHAT 🚀  

## What the Hell is This?  
This is one of my **earliest experiments** with **Google’s Generative AI** (`gemini-pro`) using `langchain`.  

I clearly got excited about:
- **LLM-powered chat**
- **Embeddings & retrieval workflows**
- **Chaining operations** (`RunnableMap`)  

Did it go anywhere?  
No.  
Was it fun?  
Absolutely.  

Now that I’ve rediscovered this relic, **let’s document it properly** before I forget it *again*.  

---

## Why I Built This (Past Me’s Thought Process)  

1. **Test Driving Gemini-Pro**:  
   - First encounter with **Google’s GenAI models** and how they handle chat prompts.  

2. **Embedding & Retrieval Pipeline**:  
   - *"What if I could store document embeddings and use them for context retrieval?"*  
   - Introduced **vector search** (`DocArrayInMemorySearch`) to **find relevant context for queries.**  

3. **RunnableMap Shenanigans**:  
   - Started messing with `RunnableMap` to **chain operations together dynamically.**  

4. **Markdown Formatting for Readability**:  
   - Because **chatbot responses in plain text are boring.**  

---

## Project Structure (What’s Inside)  

```plaintext
/Users/jasonnathan/Repos/gemini-chat
├── activate                          # Symlink to virtual env (was I using Python virtualenv?)
├── list.sh                           # Placeholder or some forgotten script?
└── main.py                           # The original "Chat with Gemini" script
```

**Inside `.server-python-test/` (which sounds like a crime scene):**  
```plaintext
.server-python-test/
├── app/
│   ├── api.py                        # API key setup + basic Gemini interactions
│   ├── chatbot.py                     # Chat functions + embeddings
│   ├── embedder.py                     # Handles document embeddings
│   ├── operations.py                   # Handles chain invocation
│   ├── retriever.py                    # Retrieval mechanism using prompts
└── test/
    ├── test_api.py                     # Some rare test cases?!
```

---

## Breakdown of Key Components  

### 1️⃣ main.py — The First Experiment
- This was my **first test** of `gemini-pro` inside `langchain`.  
- **What It Does**:
  - Loads **Google’s Generative AI model**.
  - Fetches the `GOOGLE_API_KEY` from the environment.
  - Sends a **basic prompt** and **formats the response as Markdown**.  

#### Example Code
```python
from IPython.display import display, Markdown
import textwrap
import os
from langchain_google_genai import ChatGoogleGenerativeAI

def to_markdown(text):
  text = text.replace('•', '  *')
  return Markdown(textwrap.indent(text, '> ', predicate=lambda _: True))

llm = ChatGoogleGenerativeAI(model="gemini-pro", google_api_key=os.environ.get("GOOGLE_API_KEY"))
result = llm.invoke("What is the best practice to keep fit?")
to_markdown(result.content)
```
✅ **Results looked clean in a Jupyter Notebook.**  
❌ **Not much more than a proof of concept.**  

---

### 2️⃣ .server-python-test/api.py — Basic API Wrapper
- **Sets up Google’s API key.**
- **Lists available Gemini models.**
- **Handles basic chat queries.**  

#### Example
```python
import os
import google.generativeai as genai

def configure_api_key(api_key: str):
    os.environ["GOOGLE_API_KEY"] = api_key
    genai.configure(api_key=api_key)

def get_available_models():
    return genai.models.list_models()

def generate_content(prompt: str, model_name: str = 'gemini-pro'):
    generative_model = genai.GenerativeModel(model_name)
    response = generative_model.generate_content(prompt)
    return response.text
```
💡 **Not bad for a basic API setup!**  

---

### 3️⃣ chatbot.py — Embeddings + Vector Search
- **This is where I got ambitious.**  
- Introduces **`GoogleGenerativeAIEmbeddings` + `DocArrayInMemorySearch`** to **store and retrieve embeddings**.  
- **RunnableMap kicks in here!**  

#### Example
```python
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain.vectorstores import DocArrayInMemorySearch
from langchain.schema.runnable import RunnableMap

def setup_embeddings(doc_texts: list, embedding_model: str = 'models/embedding-001'):
    embeddings = GoogleGenerativeAIEmbeddings(model=embedding_model)
    vectorstore = DocArrayInMemorySearch.from_texts(doc_texts, embeddings)
    return vectorstore

def invoke_runnable_map(question: str, retriever):
    chain = RunnableMap({
        "context": lambda x: retriever.get_relevant_documents(x["question"]),
        "question": lambda x: x["question"]
    }) 
    chain.invoke({"question": question})
```
💡 **Idea was to retrieve relevant documents, embed them, and use them for better responses.**  
❌ **Never fully wired this up.**  

---

### 4️⃣ retriever.py — Retrieval & Prompt Chaining
- Used `ChatPromptTemplate` to format prompts.  
- Wrapped a **retrieval system** inside a `RunnableMap`.  

#### Example
```python
from langchain.prompts import ChatPromptTemplate
from langchain.schema.runnable import RunnableMap

def make_retrievable(retriever, template_str: str):
    prompt = ChatPromptTemplate.from_template(template_str)
    
    chain_context = RunnableMap({
        "context": lambda x: retriever.get_relevant_documents(x['question']),
        "question": lambda x: x['question']
    }) | prompt.template
    
    return chain_context
```
💡 **This could have powered a chatbot with memory and context!**  
❌ **Never fully tested.**  

---

### 5️⃣ test/test_api.py — Wait… Did I Actually Write Tests?!
- A rare case where **I wrote unit tests**.  
- **Mocks Gemini’s API responses** and **checks API key handling**.  

#### Example
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
```
💡 **Not bad for an early project!**  

---

## What’s Good Here?  

✅ **Embeddings + Vector Search** → The idea was solid.  
✅ **RunnableMap Integration** → Great for chaining LLM logic.  
✅ **Basic API Wrapper** → Clean setup for Gemini.  
✅ **Markdown Output** → Results looked polished.  

---

## What Could Be Improved?  

❌ **Codebase is Messy** → `.server-python-test` is a weird name. Needs restructuring.  
❌ **Lack of Full Integration** → Some parts were never wired together.  
❌ **RunnableMap Logic is Half-Baked** → Great idea, but unfinished.  
❌ **Docs + README Missing** → Had no idea what this was until I dug into it.  

---

## Next Steps (If I Ever Revisit This)  

1. **Refactor the Codebase**  
   - Move `.server-python-test/` into proper `src/` structure.  

2. **Complete the Chatbot Pipeline**  
   - Actually **connect embeddings + retrieval + LLM chaining.**  

3. **Improve the Prompt Chaining**  
   - Fully utilize `RunnableMap` and `ChatPromptTemplate`.  

4. **Dockerize for Portability**  
   - If I want to deploy this, make it easy to spin up.  

---

## Repo Link
```plaintext
origin	https://github.com/jasonnathan/gemini-chat.git
```

This was **one of my earliest LLM experiments**, and it had potential. If I ever get bored, I might **finish it properly**. But for now, it remains a **fun, forgotten sandbox**. 🚀