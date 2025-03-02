from dotenv import load_dotenv
import os

load_dotenv()

class Config:
    API_KEY = os.getenv("API_KEY")
    EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL")
    LLM_MODEL_LLAMA = os.getenv("LLM_MODEL_LLAMA")
    LLM_MODEL_DEEP_SEEK = os.getenv("LLM_MODEL_DEEP_SEEK")