import os
from dotenv import load_dotenv
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

# Load environment variables
load_dotenv()

class MarketSenseOrchestrator:
    def __init__(self, model_name="llama3", temperature=0.2):
        """Initializes the LLM, vector store retriever, and agent prompts."""
        print(f"[INFO] Initializing local LLM: {model_name} via Ollama...")
        self.llm = ChatOllama(model=model_name, temperature=temperature)
        self.output_parser = StrOutputParser()
        
        # Set up Vector Store and Retriever
        print("[INFO] Connecting to ChromaDB Vector Store...")
        base_dir = os.path.dirname(os.path.dirname(__file__))
        vector_store_dir = os.path.join(base_dir, "data", "vector_store")
        
        self.embedding_function = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )
        
        self.vector_store = Chroma(
            collection_name="marketsense_trends",
            persist_directory=vector_store_dir,
            embedding_function=self.embedding_function
        )
        
        # Configure retriever to fetch the top 10 most relevant text chunks
        self.retriever = self.vector_store.as_retriever(search_kwargs={"k": 10})
        
        self.chain = self._build_pipeline()

    def _build_trend_analyzer_prompt(self):
        """Defines the prompt for the Trend Analyzer agent."""
        return ChatPromptTemplate.from_messages([
            ("system", "You are an expert consumer intelligence analyst. "
                       "Analyze the provided raw social signals and identify the top 3 emerging trends. "
                       "Focus on ingredients, aesthetics, and consumer pain points."),
            ("user", "Raw Data Context:\n{context}\n\nExtract the core trends.")
        ])

    def _build_strategist_prompt(self):
        """Defines the prompt for the Brand Strategist agent."""
        return ChatPromptTemplate.from_messages([
            ("system", "You are a Chief Strategy Officer for an Indian consumer brand portfolio. "
                       "Given emerging global trends, formulate 2 highly actionable product development "
                       "or marketing strategies tailored specifically for the Indian market."),
            ("user", "Emerging Trends:\n{trends}\n\nGenerate the actionable strategies.")
        ])

    def _format_docs(self, docs):
        """Helper to format retrieved documents into a single string."""
        return "\n\n".join(doc.page_content for doc in docs)

    def _build_pipeline(self):
        """Chains the RAG retrieval and agents together using LCEL."""
        
        # Step 1: Retrieval Augmented Generation (RAG) & Trend Analysis
        # The chain starts by passing the input query to the retriever
        analyze_trends = (
            {"context": self.retriever | self._format_docs} 
            | self._build_trend_analyzer_prompt() 
            | self.llm 
            | self.output_parser
        )

        # Step 2: Strategy Generation based on Step 1 output
        formulate_strategy = (
            {"trends": analyze_trends} 
            | self._build_strategist_prompt() 
            | self.llm 
            | self.output_parser
        )

        return formulate_strategy

    def run(self, query: str) -> str:
        """Executes the orchestrator pipeline using a search query."""
        print(f"[INFO] Starting Orchestration Pipeline for query: '{query}'...")
        print("[INFO] Retrieving relevant data from ChromaDB...")
        
        try:
            # The pipeline now expects a string query instead of hard-coded context
            result = self.chain.invoke(query)
            print("[SUCCESS] Pipeline execution complete.")
            return result
        except Exception as e:
            print(f"[ERROR] Pipeline failed: {str(e)}")
            return ""

if __name__ == "__main__":
    orchestrator = MarketSenseOrchestrator()
    
    # Instead of injecting mock data, we ask the orchestrator to research a topic.
    # It will dynamically search ChromaDB, extract context, and formulate a strategy.
    target_market_query = "What are the latest consumer complaints and trends regarding sunscreen in India?"
    
    final_strategy = orchestrator.run(query=target_market_query)
    
    print("\n--- FINAL STRATEGY OUTPUT ---\n")
    print(final_strategy)