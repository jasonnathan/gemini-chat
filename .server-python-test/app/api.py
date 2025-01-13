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