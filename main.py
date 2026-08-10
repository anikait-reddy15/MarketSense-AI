import os
import sys

# Import the modular components from our project structure
from ingestion.trend_scraper import TrendIngestionEngine
from ingestion.data_pipeline import VectorDatabaseManager
from agents.orchestrator import MarketSenseOrchestrator

def main():
    print("==================================================")
    print("      Think9 MarketSense AI - Core Execution      ")
    print("==================================================\n")

    # Phase 1: Data Ingestion
    print(">>> PHASE 1: DATA INGESTION")
    scraper = TrendIngestionEngine()
    
    # Define the consumer signals we want to track for Think9
    skincare_query = "Indian skincare sunscreen complaints sticky white cast"
    ingredient_query = "ashwagandha matcha focus drink trends India"
    
    # Execute the keyless DuckDuckGo scraper
    skincare_data = scraper.fetch_web_trends(skincare_query, max_results=10)
    ingredient_data = scraper.fetch_web_trends(ingredient_query, max_results=10)
    
    # Save the scraped data locally
    scraper.save_to_json(skincare_data, "skincare_trends.json")
    scraper.save_to_json(ingredient_data, "ingredient_trends.json")
    print("\n")

    # Phase 2: Vector Embedding & Storage
    print(">>> PHASE 2: VECTOR EMBEDDING & STORAGE")
    base_dir = os.path.dirname(os.path.abspath(__file__))
    raw_data_dir = os.path.join(base_dir, "data", "raw")
    vector_store_dir = os.path.join(base_dir, "data", "vector_store")
    
    files_to_process = [
        os.path.join(raw_data_dir, "skincare_trends.json"),
        os.path.join(raw_data_dir, "ingredient_trends.json")
    ]
    
    # Process the JSON files into ChromaDB
    db_manager = VectorDatabaseManager(persist_directory=vector_store_dir)
    db_manager.build_vector_store(files_to_process)
    print("\n")

    # Phase 3: Agentic Strategy Generation
    print(">>> PHASE 3: AGENTIC STRATEGY GENERATION")
    
    # Define a broad query that requires the AI to synthesize both data sources
    target_query = "What are the latest consumer complaints regarding sunscreen in India, and what ingredients are trending for focus?"
    
    # Run the LangChain RAG pipeline
    orchestrator = MarketSenseOrchestrator()
    final_strategy = orchestrator.run(query=target_query)
    
    # Output the final result
    print("\n==================================================")
    print("             FINAL STRATEGY OUTPUT                ")
    print("==================================================\n")
    print(final_strategy)

if __name__ == "__main__":
    main()