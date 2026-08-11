import os
import sys

# Dynamically append the project root to sys.path to resolve internal module imports
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.append(project_root)

from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

from utils.config import Config
from utils.logger import setup_logger
from agents.strategist import StrategistAgent

# Initialize structured logger
logger = setup_logger("MarketSenseOrchestrator")

class MarketSenseOrchestrator:
    def __init__(self):
        """Initializes the LLM, vector store retriever, logger, and sub-agents."""
        Config.ensure_directories()
        
        logger.info(f"Initializing local LLM: {Config.LLM_MODEL_NAME} via Ollama...")
        self.llm = ChatOllama(
            model=Config.LLM_MODEL_NAME, 
            temperature=Config.LLM_TEMPERATURE
        )
        self.output_parser = StrOutputParser()
        
        logger.info("Connecting to ChromaDB Vector Store...")
        self.embedding_function = HuggingFaceEmbeddings(
            model_name=Config.EMBEDDING_MODEL_NAME,
            model_kwargs={'device': Config.EMBEDDING_DEVICE}
        )
        
        self.vector_store = Chroma(
            collection_name=Config.VECTOR_COLLECTION_NAME,
            persist_directory=str(Config.VECTOR_STORE_DIR),
            embedding_function=self.embedding_function
        )
        
        self.retriever = self.vector_store.as_retriever(
            search_kwargs={"k": Config.VECTOR_SEARCH_TOP_K}
        )
        
        # Initialize modular sub-agent persona
        self.strategist_agent = StrategistAgent(llm=self.llm)
        
        self.chain = self._build_pipeline()

    def _build_trend_analyzer_prompt(self):
        """Defines the prompt for the Trend Analyzer agent."""
        return ChatPromptTemplate.from_messages([
            ("system", "You are an expert consumer intelligence analyst. "
                       "Analyze the provided raw social signals and identify the top 3 emerging trends. "
                       "Focus on ingredients, aesthetics, and consumer pain points."),
            ("user", "Raw Data Context:\n{context}\n\nExtract the core trends.")
        ])

    def _format_docs(self, docs):
        """Helper to format retrieved documents into a single string."""
        return "\n\n".join(doc.page_content for doc in docs)

    def _build_pipeline(self):
        """Chains vector retrieval, trend extraction, and modular strategy generation."""
        
        # Step 1: Extract trends from vector retrieval
        analyze_trends = (
            {"context": self.retriever | self._format_docs} 
            | self._build_trend_analyzer_prompt() 
            | self.llm 
            | self.output_parser
        )

        # Step 2: Route trend summary through the modular StrategistAgent
        formulate_strategy = analyze_trends | self.strategist_agent.chain

        return formulate_strategy

    def run(self, query: str) -> str:
        """Executes the orchestrator pipeline using a search query."""
        logger.info(f"Starting Orchestration Pipeline for query: '{query}'")
        
        try:
            result = self.chain.invoke(query)
            logger.info("Pipeline execution completed successfully.")
            return result
        except Exception as e:
            logger.error(f"Pipeline execution failed: {str(e)}", exc_info=True)
            return ""

if __name__ == "__main__":
    orchestrator = MarketSenseOrchestrator()
    target_query = "What are the latest consumer complaints and trends regarding sunscreen in India?"
    
    final_strategy = orchestrator.run(query=target_query)
    
    print("\n--- FINAL STRATEGY OUTPUT ---\n")
    print(final_strategy)