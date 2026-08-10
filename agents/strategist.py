from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

class StrategistAgent:
    def __init__(self, llm):
        """Initializes the Brand Strategist Agent with an injected LLM instance."""
        self.llm = llm
        self.output_parser = StrOutputParser()
        self.prompt = self._build_prompt()
        self.chain = self.prompt | self.llm | self.output_parser

    def _build_prompt(self) -> ChatPromptTemplate:
        """Constructs the system prompt and instructions for the Brand Strategist persona."""
        return ChatPromptTemplate.from_messages([
            ("system", 
             "You are the Chief Strategy Officer for Think9's consumer brand portfolio in India.\n"
             "Your responsibility is to take analyzed market trends and translate them into high-velocity, "
             "actionable product development and go-to-market strategies.\n\n"
             "Strategic Requirements:\n"
             "1. Recommendations must be tailored strictly to the Indian consumer demographic.\n"
             "2. Identify clear hero ingredients, formulation adjustments, or packaging solutions.\n"
             "3. Define concrete marketing hooks and distribution channel ideas."),
            ("user", "Analyzed Trend Insights:\n{trends}\n\nGenerate the actionable strategic plan:")
        ])

    def execute(self, trends_summary: str) -> str:
        """Executes the agent strategy generation chain."""
        return self.chain.invoke({"trends": trends_summary})