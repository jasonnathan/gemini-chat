# JJN-INFO: GEMINI-CHAT

---

## **What This Is**
- A super early project where I dabbled with **Google’s Generative AI** (`gemini-pro`) using `langchain`.  
- It’s essentially a playground for integrating LLM-powered chat and embedding workflows.  
- Not polished or production-ready, but it works as a personal sandbox for testing ideas.  

---

## **Folder Layout**

```plaintext
/Users/jasonnathan/Repos/gemini-chat
├── activate                          # Symlink to the virtual environment's activate script
├── list.sh                           # Placeholder or utility script
└── main.py                           # Core script using langchain-google-genai
```

---

## **Core Components**

### **main.py**
- **Purpose**: Quick test of the **Google Generative AI model** (`gemini-pro`) with Markdown output.  
- **What It Does**:
  - Instantiates a chat model using `ChatGoogleGenerativeAI`.
  - Fetches the `GOOGLE_API_KEY` from the environment variables.
  - Sends a basic prompt (`"What is the best practice to keep fit?"`) and renders the response as Markdown.  
- **Notes**:
  - Great for proof of concept but doesn’t do much else.
  - `to_markdown()` is a simple but nice touch to make results look clean in a Jupyter notebook.

---

### **.server-python-test**
- **Purpose**: This folder seems like an experimental server setup for API and embedding workflows.
- **Key Files**:
  - **api.py**:
    - Handles API configuration (`configure_api_key`), model listing, and text generation using `gemini-pro`.
  - **chatbot.py**:
    - Implements embeddings with `GoogleGenerativeAIEmbeddings` and vector stores (`DocArrayInMemorySearch`).
    - Outlines how to use `RunnableMap` for chaining operations.
  - **embedder.py**:
    - Sets up embeddings for document retrieval. A building block for more advanced functionality.
  - **operations.py**:
    - Contains utility functions for chain setups and embeddings, including a way to invoke `RunnableMap`.
  - **retriever.py**:
    - Focused on prompt templates and integrating context retrieval into the pipeline.

---

### **Noteworthy Functionality**
- **Markdown Rendering** (`main.py`):  
  Converts LLM responses into clean Markdown format for easier readability.  

- **Embedding Workflow**:
  - Uses `GoogleGenerativeAIEmbeddings` to create document embeddings.  
  - Supports vectorized search with `DocArrayInMemorySearch`.  
  - Great for building a retriever pipeline.  

- **RunnableMap Setup**:
  - Combines context retrieval, question extraction, and prompt templating into a flexible chain.  
  - The `RunnableMap` is a promising way to test modular pipelines.  

---

## **How to Run**
1. **Setup**:
   - Install dependencies and activate the virtual environment:
     ```bash
     source activate
     pip install -r requirements.txt
     ```
   - Export the **Google API Key**:
     ```bash
     export GOOGLE_API_KEY="your_api_key"
     ```

2. **Run the Main Script**:
   ```bash
   python main.py
   ```
   - Sends a sample prompt to `gemini-pro` and formats the response in Markdown.

3. **API Server Test**:
   - Use `api.py` or other files in `.server-python-test` for further experimentation.

---

## **What I Like**
- **Markdown Output**: Clean results are always a win for debugging and presentations.  
- **LangChain Integration**: Early exploration of chaining, embeddings, and retrievers.  
- **RunnableMap Concept**: Modular design for chaining LLM operations—definitely worth revisiting.  

---

## **What Could Be Better**
1. **Better Organization**:  
   The `.server-python-test` folder feels chaotic. Refactor into clearer modules.  

2. **README Needed**:  
   There’s no explanation of what this project does, its dependencies, or how to use it.  

3. **Expand Pipelines**:  
   The `RunnableMap` concept is great but not fully utilized. Could extend to support multi-turn chat or document QA.  

4. **Unified Workflow**:  
   Combine the chatbot, embeddings, and retriever into a single pipeline to showcase end-to-end functionality.  

5. **Docs for Functions**:  
   There are docstrings, but they could be more detailed about inputs/outputs and expected side effects.  

---

## **Repo Link**
```plaintext
origin	https://github.com/jasonnathan/gemini-chat.git
```

---

## **Final Thoughts**
This was an ambitious early attempt at integrating LLMs with retrieval and embeddings. While not polished, it laid the foundation for more structured projects later. Definitely worth revisiting if I want to experiment with `langchain` pipelines or Google’s LLMs again.
