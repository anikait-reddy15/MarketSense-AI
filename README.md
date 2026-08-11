# MarketSense AI
An autonomous, multi-agent intelligence pipeline. It continuously ingests global social signals, ingredient trends, and consumer data (e.g., TikTok trends, Reddit reviews). It synthesizes this to proactively deliver localized, actionable product insights for Think9’s brands, converting static research into predictive strategy.

# MarketSense AI

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue)](https://www.python.org/)
[![LangChain](https://img.shields.io/badge/LangChain-LCEL-green)](https://www.langchain.com/)
[![ChromaDB](https://img.shields.io/badge/Vector%20DB-ChromaDB-orange)](https://www.trychroma.com/)
[![Ollama](https://img.shields.io/badge/LLM-Ollama-black)](https://ollama.com/)
[![Streamlit](https://img.shields.io/badge/UI-Streamlit-red)](https://streamlit.io/)

## Overview

### Definition

**MarketSense AI** is a centralized, AI-native consumer intelligence engine designed for Think9's venture studio and brand portfolio.

### Explanation

MarketSense AI ingests unstructured global consumer signals and transforms them into actionable, localized product strategies for the Indian market.

Instead of depending on static market research and manually collected insights, MarketSense AI creates an automated research layer that collects consumer discussions, search trends, product complaints, and emerging market signals. These signals are embedded into a local vector database and retrieved through a Retrieval-Augmented Generation (RAG) pipeline.

Specialized AI agents then analyze the retrieved information and generate insights that can support product development, positioning, marketing, and go-to-market decisions.

### Examples

**1. Consumer Pain Point Discovery**

The system can collect discussions and complaints about skincare products, such as consumers reporting sticky textures or white casts from sunscreens in humid climates.

These complaints can then be analyzed to identify formulation opportunities for products designed specifically for Indian consumers.

**2. Ingredient Trend Detection**

MarketSense AI can search for emerging ingredient trends such as Ashwagandha, Matcha, or other rapidly growing consumer interests and identify where these trends may represent potential product opportunities.

**3. Go-To-Market Strategy**

The system can combine consumer trends and pain points to generate potential influencer strategies, product positioning, retail hooks, and localized marketing concepts.

---

## Core Architecture

MarketSense AI is designed as a modular pipeline that separates data collection, knowledge storage, intelligence, and user interaction.

```text
                    ┌──────────────────────────┐
                    │     Consumer Signals     │
                    │ Web Search / Discussions │
                    └────────────┬─────────────┘
                                 │
                                 ▼
                    ┌──────────────────────────┐
                    │     Ingestion Layer       │
                    │     DDGS / Scraping      │
                    └────────────┬─────────────┘
                                 │
                                 ▼
                    ┌──────────────────────────┐
                    │     Vector Memory        │
                    │  ChromaDB + Embeddings   │
                    └────────────┬─────────────┘
                                 │
                                 ▼
                    ┌──────────────────────────┐
                    │   Intelligence Layer     │
                    │ LangChain + RAG + Agents │
                    │      + Local LLM         │
                    └────────────┬─────────────┘
                                 │
                                 ▼
                    ┌──────────────────────────┐
                    │      User Interface      │
                    │        Streamlit          │
                    └──────────────────────────┘
```

### Ingestion Layer

The ingestion layer collects live consumer signals from the web.

The active ingestion engine uses the `ddgs` library to perform API-free DuckDuckGo searches and collect relevant search results and consumer discussions.

The system can be configured around specific categories, products, ingredients, and consumer pain points.

```text
Search Query
     │
     ▼
DuckDuckGo Search
     │
     ▼
Consumer Signals
     │
     ▼
Structured JSON
```

This approach reduces dependence on paid APIs and external platform-specific access limitations.


### Vector Memory

MarketSense AI uses **ChromaDB** as its local vector database.

Collected consumer signals are transformed into embeddings using HuggingFace's `all-MiniLM-L6-v2` model.

```text
Raw Consumer Data
       │
       ▼
Text Processing
       │
       ▼
Embedding Model
       │
       ▼
Vector Representation
       │
       ▼
ChromaDB
```

The vector database allows the intelligence layer to retrieve relevant historical information when answering a new market research query.

Embeddings can run on the CPU, reducing GPU memory usage and allowing the system to operate on resource-constrained development machines.

### Intelligence Layer

The intelligence layer is built around LangChain Expression Language (LCEL) and Retrieval-Augmented Generation (RAG).

A modular agent architecture allows different agents to specialize in different types of market intelligence.

Example agents include:

* **Trend Analyzer**
* **Consumer Pain Point Analyzer**
* **Brand Strategist**
* **Product Opportunity Analyst**
* **Go-To-Market Strategist**

The system uses a local **Llama 3** model through **Ollama** for inference.

```text
User Query
     │
     ▼
Orchestrator
     │
     ▼
Retriever
     │
     ▼
Relevant Consumer Signals
     │
     ▼
Specialized Agent
     │
     ▼
Local Llama 3
     │
     ▼
Actionable Market Insight
```

### User Interface

The Streamlit dashboard provides an interactive interface for brand managers and market researchers.

Users can query the collected market intelligence without directly interacting with the underlying ingestion layer, vector database, or agent pipeline.

Example queries include:

* **What are the biggest complaints about Indian sunscreens?**
* **Which skincare ingredients are currently gaining consumer interest?**
* **What product opportunities exist around Ashwagandha?**
* **What positioning could differentiate a new sunscreen in India?**

### Project Structure

```text
marketsense_ai/
│
├── data/
│   ├── raw/
│   │   └── # Temporarily stores scraped JSON datasets
│   │
│   ├── processed/
│   │   └── # Processed analytical outputs
│   │
│   └── vector_store/
│       └── # Local ChromaDB storage
│
├── ingestion/
│   │
│   ├── trend_scraper.py
│   │   └── # API-free DuckDuckGo ingestion engine
│   │
│   └── data_pipeline.py
│       └── # Embeds collected data into ChromaDB
│
├── agents/
│   ├── orchestrator.py
│   │   └── # Main LCEL pipeline and retrieval logic
│   │
│   └── strategist.py
│       └── # Brand Strategist agent
│
├── ui/
│   └── dashboard.py
│       └── # Streamlit interface
│
├── utils/
│   ├── config.py
│   │   └── # Centralized configuration
│   │
│   └── logger.py
│       └── # System logging
│
├── main.py
│   └── # End-to-end execution entry point
│
├── requirements.txt
└── README.md
```

## Installation & Setup

### Prerequisites

Make sure the following are installed:

* Python 3.10 or higher
* Ollama
* Git

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/marketsense_ai.git
cd marketsense_ai
```

### 2. Create a Virtual Environment

```bash
python -m venv .venv
```

#### Windows

```powershell
.venv\Scripts\activate
```

#### macOS / Linux

```bash
source .venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

The `all-MiniLM-L6-v2` embedding model will be downloaded automatically during its first execution.

### 4. Install and Start Ollama

Install Ollama and download the required local LLM:

```bash
ollama run llama3
```

Verify that the model is available:

```bash
ollama list
```

## Usage

### Option A: End-to-End Pipeline

Run the complete pipeline:

```bash
python main.py
```

The pipeline performs the following operations:

```text
1. Collect consumer signals
        ↓
2. Process scraped data
        ↓
3. Generate embeddings
        ↓
4. Store vectors in ChromaDB
        ↓
5. Retrieve relevant market information
        ↓
6. Run the AI strategy pipeline
        ↓
7. Generate actionable insights
```

### Option B: Streamlit Dashboard

Launch the interactive dashboard:

```bash
streamlit run ui/dashboard.py
```

The application will be available locally at:

```text
http://localhost:8501
```

---

## Example Workflow

A typical MarketSense AI workflow looks like this:

```text
                     MarketSense AI
                           │
                           ▼
                 Define Research Query
                           │
                           ▼
              Search Consumer Discussions
                           │
                           ▼
                Collect Market Signals
                           │
                           ▼
                 Generate Embeddings
                           │
                           ▼
                    Store in ChromaDB
                           │
                           ▼
                    Retrieve Context
                           │
                           ▼
                  Analyze with LLM
                           │
                           ▼
                Generate Product Insight
```

For example:

```text
Input:
"What are consumers complaining about
when using sunscreen in India?"

                    ↓

Retrieved Signals:
- White cast
- Sticky texture
- Excessive sweating
- Eye irritation
- High humidity performance

                    ↓

AI Analysis:
Identify recurring pain points and
potential product opportunities.

                    ↓

Output:
Potential positioning around
lightweight, sweat-resistant,
zero-white-cast sunscreen.
```
## Implementation Roadmap

MarketSense AI currently represents a functional MVP. The following 30-day roadmap focuses on transforming the prototype into a scalable internal consumer intelligence platform.

### Week 1 — Scale Data Ingestion

* Expand the DDGS ingestion engine.
* Add asynchronous ingestion jobs.
* Support 50+ localized product categories.
* Introduce scheduled data collection.
* Improve query generation and deduplication.

### Week 2 — Improve RAG and Intelligence

* Implement Maximal Marginal Relevance (MMR) retrieval.
* Improve chunking and metadata filtering.
* Add specialized consumer insight agents.
* Introduce an FSSAI/AYUSH compliance analysis agent.
* Improve agent orchestration and response consistency.

### Week 3 — Internal Deployment

* Deploy the Streamlit application internally.
* Add multi-brand selection.
* Implement brand-specific knowledge bases.
* Add Human-in-the-Loop feedback.
* Store analyst feedback for improving future insights.

### Week 4 — Production Infrastructure

* Containerize the application with Docker.
* Separate ingestion, retrieval, and inference services.
* Move LLM inference to scalable GPU infrastructure.
* Implement scheduled production pipelines.
* Add monitoring, logging, and system health checks.

## Technology Stack

| Layer               | Technology                     |
| ------------------- | ------------------------------ |
| Language            | Python                         |
| Web Research        | DDGS / DuckDuckGo              |
| Embeddings          | HuggingFace `all-MiniLM-L6-v2` |
| Vector Database     | ChromaDB                       |
| RAG / Orchestration | LangChain / LCEL               |
| Local LLM           | Llama 3                        |
| LLM Runtime         | Ollama                         |
| Frontend            | Streamlit                      |
| Data Format         | JSON                           |
| Deployment          | Docker                         |
| Target Market       | India                          |

## Design Goals

MarketSense AI is designed around four core principles:

### 1. Automated Research

Reduce the amount of manual research required to identify emerging consumer trends and recurring product problems.

### 2. Localized Intelligence

Transform global consumer signals into insights specifically relevant to Indian consumers, categories, and market conditions.

### 3. Modular AI Architecture

Keep ingestion, retrieval, agents, and the user interface modular so that individual components can be upgraded independently.

### 4. Cost-Efficient AI

Use local embeddings, local vector storage, and local LLM inference to minimize dependence on expensive external AI APIs during development and internal deployment.

## Future Opportunities

Potential extensions include:

* Real-time trend monitoring
* Automated competitor intelligence
* Brand-specific RAG pipelines
* Consumer sentiment tracking
* Product concept generation
* Market opportunity scoring
* Automated influencer discovery
* Retail trend analysis
* Regulatory compliance analysis
* Multi-agent product research
* Automated executive reports
* Scheduled market intelligence alerts
