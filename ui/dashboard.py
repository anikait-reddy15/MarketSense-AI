import os
import sys
import streamlit as st

# Add the project root to the system path to allow importing backend modules
project_root = os.path.dirname(os.path.dirname(__file__))
sys.path.append(project_root)

from agents.orchestrator import MarketSenseOrchestrator

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
        st.write("This dashboard queries the local ChromaDB for ingested consumer trends and generates actionable product strategies.")

    # Main Dashboard Area
    st.title("Central Consumer Intelligence Engine")
    st.markdown("Transform raw social signals into localized product strategies.")

    # Input section
    st.subheader("Market Research Query")
    query_input = st.text_input(
        "Enter a topic to analyze:",
        value="What are the latest consumer complaints and trends regarding sunscreen in India?"
    )

    generate_button = st.button("Generate Product Strategy", type="primary")

    if generate_button and query_input:
        st.markdown("---")
        st.subheader("AI Strategic Output")
        
        with st.spinner("Querying vector store and generating strategies..."):
            try:
                # Execute the RAG pipeline using the session state orchestrator
                final_strategy = st.session_state.orchestrator.run(query=query_input)
                
                # Display the output directly on the dashboard
                st.markdown(final_strategy)
            except Exception as e:
                # Using standard markdown to strictly prevent automatic emoji rendering
                st.markdown(f"**[ERROR]** An error occurred during generation: {str(e)}")

if __name__ == "__main__":
    main()