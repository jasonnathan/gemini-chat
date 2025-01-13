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