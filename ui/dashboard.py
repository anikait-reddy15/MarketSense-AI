import os
import sys
import time
import subprocess
import requests
import streamlit as st

# Add the project root to the system path to allow importing backend modules
project_root = os.path.dirname(os.path.dirname(__file__))
if project_root not in sys.path:
    sys.path.append(project_root)

from agents.orchestrator import MarketSenseOrchestrator
from ingestion.trend_scraper import TrendIngestionEngine
from ingestion.data_pipeline import VectorDatabaseManager
from utils.config import Config

# Configure the Streamlit page layout
st.set_page_config(
    page_title="MarketSense AI Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

@st.cache_resource
def manage_ollama_lifecycle():
    """Starts Ollama and preloads the model on startup, unloads them on exit."""
    
    # 1. Start the Ollama server in the background
    ollama_process = subprocess.Popen(
        ["ollama", "serve"], 
        stdout=subprocess.DEVNULL, 
        stderr=subprocess.DEVNULL
    )
    
    # Give the server 2 seconds to initialize
    time.sleep(2)
    
    # 2. Preload Llama-3 into GPU memory (keep_alive: -1 keeps it loaded indefinitely)
    try:
        requests.post(
            "http://localhost:11434/api/generate", 
            json={"model": Config.LLM_MODEL_NAME, "keep_alive": -1},
            timeout=5
        )
    except Exception:
        pass

    # Yield control back to Streamlit (The app runs normally here)
    yield ollama_process

    # 3. TEARDOWN: Runs automatically when you press Ctrl+C to stop the dashboard
    print(f"\n[INFO] Dashboard stopping... Unloading {Config.LLM_MODEL_NAME} to free GPU memory.")
    try:
        # Force unload the model from VRAM using the Ollama CLI
        subprocess.run(
            ["ollama", "stop", Config.LLM_MODEL_NAME], 
            stdout=subprocess.DEVNULL, 
            stderr=subprocess.DEVNULL
        )
        # Fallback API call to drop memory
        requests.post(
            "http://localhost:11434/api/generate", 
            json={"model": Config.LLM_MODEL_NAME, "keep_alive": 0},
            timeout=2
        )
    except Exception:
        pass
        
    # 4. Terminate the background Ollama server
    print("[INFO] Shutting down Ollama background server.")
    ollama_process.terminate()

def initialize_system():
    """Initializes the background processes and orchestrator state."""
    
    # Register the Ollama lifecycle hook
    manage_ollama_lifecycle()
    
    # Initialize the LLM orchestrator
    if "orchestrator" not in st.session_state:
        with st.spinner("Initializing Local Llama-3 and Vector Database... Please wait."):
            st.session_state.orchestrator = MarketSenseOrchestrator()

def ingest_live_data(query: str):
    """Scrapes live data and injects it into ChromaDB dynamically, resetting stale data."""
    Config.ensure_directories()
    
    scraper = TrendIngestionEngine()
    db_manager = VectorDatabaseManager(persist_directory=str(Config.VECTOR_STORE_DIR))
    
    scraped_data = scraper.fetch_web_trends(query, max_results=10)
    
    if not scraped_data:
        raise ValueError("Failed to retrieve any live data for this topic.")
        
    temp_filename = "live_dashboard_scrape.json"
    scraper.save_to_json(scraped_data, temp_filename)
    
    filepath = os.path.join(Config.RAW_DATA_DIR, temp_filename)
    
    # Pass reset=True to wipe old beverage/sunscreen vectors during live scraping
    db_manager.build_vector_store([filepath], reset=True)
    
def main():
    initialize_system()

    # Sidebar Configuration
    with st.sidebar:
        st.title("MarketSense AI")
        st.write("Think9 Consumer Intelligence Engine")
        st.markdown("---")
        st.write("System Status:")
        st.markdown("**[ACTIVE]** Vector Database Connected")
        st.markdown("**[ACTIVE]** Local Llama-3 Server Managed")
        st.markdown("---")
        
        st.subheader("Data Strategy")
        use_live_scrape = st.toggle("Enable Live Web Scraping", value=False)
        st.caption("If enabled, the system will scrape the internet for fresh data before answering your query. If disabled, it searches existing database memory.")

    # Main Dashboard Area
    st.title("Central Consumer Intelligence Engine")
    st.markdown("Transform raw social signals into localized product strategies.")

    # Input section
    st.subheader("Market Research Query")
    query_input = st.text_input(
        "Enter a topic to analyze:",
        value="What are the latest consumer complaints regarding sunscreen in India?"
    )

    generate_button = st.button("Generate Product Strategy", type="primary")

    if generate_button and query_input:
        st.markdown("---")
        st.subheader("AI Strategic Output")
        
        try:
            if use_live_scrape:
                with st.spinner("Scraping live internet data and embedding into ChromaDB..."):
                    ingest_live_data(query_input)
                    st.markdown("**[SUCCESS]** Successfully ingested fresh market data!")
            
            with st.spinner("Querying vector store and generating strategy..."):
                final_strategy = st.session_state.orchestrator.run(query=query_input)
                st.markdown(final_strategy)
                
        except Exception as e:
            st.markdown(f"**[ERROR]** An error occurred: {str(e)}")

if __name__ == "__main__":
    main()