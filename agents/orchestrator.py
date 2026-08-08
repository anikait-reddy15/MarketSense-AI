import os
from dotenv import load_dotenv
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

# Load environment variables
load_dotenv()

class MarketSenseOrchestrator:
    # Initializing with the local llama3 model
    def __init__(self, model_name="llama3", temperature=0.2):
        """Initializes the LLM and the agent prompts."""
        print(f"[INFO] Initializing local LLM: {model_name} via Ollama...")
        self.llm = ChatOllama(model=model_name, temperature=temperature)
        self.output_parser = StrOutputParser()
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

    def _build_pipeline(self):
        """Chains the agents together using LCEL."""
        # Step 1: Trend Analysis
        analyze_trends = (
            self._build_trend_analyzer_prompt() 
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

    def run(self, retrieved_context: str) -> str:
        """Executes the orchestrator pipeline."""
        print("[INFO] Starting MarketSense AI Orchestration Pipeline...")
        print("[INFO] Analyzing trends and generating strategies...")
        
        try:
            # The input dictionary must match the expected variable in the first prompt
            result = self.chain.invoke({"context": retrieved_context})
            print("[SUCCESS] Pipeline execution complete.")
            return result
        except Exception as e:
            print(f"[ERROR] Pipeline failed: {str(e)}")
            return ""

if __name__ == "__main__":
    # Mock context that would normally come from your vector store
    mock_scraped_data = (
        "TikTok trend: Users are mixing ashwagandha with matcha for focus. "
        "Reddit skincare routines heavily feature Centella Asiatica for barrier repair. "
        "High complaints about sticky sunscreens in humid climates."
    )
    
    orchestrator = MarketSenseOrchestrator()
    final_strategy = orchestrator.run(retrieved_context=mock_scraped_data)
    
    print("\n--- FINAL STRATEGY OUTPUT ---\n")
    print(final_strategy)