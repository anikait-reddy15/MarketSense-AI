import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    # Directory Structure
    BASE_DIR = Path(__file__).resolve().parent.parent
    DATA_DIR = BASE_DIR / "data"
    RAW_DATA_DIR = DATA_DIR / "raw"
    PROCESSED_DATA_DIR = DATA_DIR / "processed"
    VECTOR_STORE_DIR = DATA_DIR / "vector_store"

    # Model Settings
    LLM_MODEL_NAME = os.getenv("LLM_MODEL_NAME", "llama3")
    LLM_TEMPERATURE = float(os.getenv("LLM_TEMPERATURE", "0.2"))
    EMBEDDING_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
    EMBEDDING_DEVICE = "cpu"  # Forced CPU to prevent GPU VRAM lockup with Ollama

    # Search & Retrieval Parameters
    VECTOR_SEARCH_TOP_K = 10
    VECTOR_COLLECTION_NAME = "marketsense_trends"

    # Scraping Parameters
    DEFAULT_REGION = "in-en"
    MAX_SCRAPE_RESULTS = 10

    @classmethod
    def ensure_directories(cls):
        """Creates required data directories if they do not exist."""
        cls.RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)
        cls.PROCESSED_DATA_DIR.mkdir(parents=True, exist_ok=True)
        cls.VECTOR_STORE_DIR.mkdir(parents=True, exist_ok=True)