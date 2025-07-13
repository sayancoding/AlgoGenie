from dotenv import load_dotenv
import os
from autogen_ext.models.openai import OpenAIChatCompletionClient

"""loading env variables"""
load_dotenv()

def llm_model():
    GEMINI_API_KEY = os.getenv('GOOGLE_API_KEY')
    if not GEMINI_API_KEY:
        raise ValueError("GEMINI API Key is not pres")
    
    llm_client = OpenAIChatCompletionClient(model='gemini-2.5-flash',api_key=GEMINI_API_KEY)
    return llm_client