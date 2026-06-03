
import os
from dotenv import load_dotenv

from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()  # Load environment variables from .env file

model = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0.5,  
    max_tokens=None,  
    timeout=None,
    max_retries=2,
)
