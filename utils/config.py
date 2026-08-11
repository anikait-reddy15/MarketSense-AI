import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Directory Structure
    BASE_DIR = Path(__file__).resolve().parent.parent
    DATA_DIR = BASE_DIR / "data"
    RAW_DATA_DIR = DATA_DIR / "raw"
    PROCESSED_DATA_DIR = DATA_DIR / "processed"
    VECTOR_STORE_DIR = DATA_DIR / "vector_store"

    # Cloud Model Settings (Swapped from Ollama to Groq)
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    LLM_MODEL_NAME = "llama-3.3-70b-versatile" # Groq's high-performance Llama 3 model
    LLM_TEMPERATURE = float(os.getenv("LLM_TEMPERATURE", "0.2"))
    
    # Embedding Settings
    EMBEDDING_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
    EMBEDDING_DEVICE = "cpu"

    VECTOR_SEARCH_TOP_K = 10
    VECTOR_COLLECTION_NAME = "marketsense_trends"

    @classmethod
    def ensure_directories(cls):
        cls.RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)
        cls.PROCESSED_DATA_DIR.mkdir(parents=True, exist_ok=True)
        cls.VECTOR_STORE_DIR.mkdir(parents=True, exist_ok=True)