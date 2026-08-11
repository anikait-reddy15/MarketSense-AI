import os
import sys
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

def initialize_system():
    """Initializes the orchestrator in Streamlit's session state to prevent reloading."""
    if "orchestrator" not in st.session_state:
        with st.spinner("Initializing Local Llama-3 and Vector Database... Please wait."):
            st.session_state.orchestrator = MarketSenseOrchestrator()

def ingest_live_data(query: str):
    """Scrapes live data and injects it into ChromaDB dynamically."""
    Config.ensure_directories()
    
    # Initialize the keyless scraper and vector manager
    scraper = TrendIngestionEngine()
    db_manager = VectorDatabaseManager(persist_directory=str(Config.VECTOR_STORE_DIR))
    
    # Step 1: Scrape the web for the user's specific query
    scraped_data = scraper.fetch_web_trends(query, max_results=10)
    
    if not scraped_data:
        raise ValueError("Failed to retrieve any live data for this topic.")
        
    # Step 2: Save temporarily to pass to the vector pipeline
    temp_filename = "live_dashboard_scrape.json"
    scraper.save_to_json(scraped_data, temp_filename)
    
    # Step 3: Embed into ChromaDB
    filepath = os.path.join(Config.RAW_DATA_DIR, temp_filename)
    db_manager.build_vector_store([filepath])
    
def main():
    # Load backend models on startup
    initialize_system()

    # Sidebar Configuration
    with st.sidebar:
        st.title("MarketSense AI")
        st.write("Think9 Consumer Intelligence Engine")
        st.markdown("---")
        st.write("System Status:")
        st.markdown("**[ACTIVE]** Vector Database Connected")
        st.markdown("**[ACTIVE]** Local Llama-3 Model Loaded")
        st.markdown("---")
        
        # Add the toggle for On-Demand Ingestion
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
            # Handle Live Scraping if the user toggled it on
            if use_live_scrape:
                with st.spinner("Scraping live internet data and embedding into ChromaDB..."):
                    ingest_live_data(query_input)
                    st.success("Successfully ingested fresh market data!")
            
            # Execute RAG strategy generation
            with st.spinner("Querying vector store and generating strategy..."):
                final_strategy = st.session_state.orchestrator.run(query=query_input)
                st.markdown(final_strategy)
                
        except Exception as e:
            st.markdown(f"**[ERROR]** An error occurred: {str(e)}")

if __name__ == "__main__":
    main()