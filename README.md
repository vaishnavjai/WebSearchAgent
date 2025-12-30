# AI Assistant with Dynamic Web Search

An advanced AI assistant that dynamically fetches live data from search engines to provide accurate, context-aware responses. Built with Python, Ollama, and web search APIs.

## 🚀 Features

### Core Functionality
- **Smart Search Decision**: Automatically determines if a user query requires external data (e.g., real-time updates, missing context).
- **Real-Time Streaming**: Responses stream dynamically for a natural conversation flow.
- **Context-Aware Responses**: Uses conversation history to maintain coherence.

### Technical Highlights
- **Modular Architecture**:
  - `sys_msgs.py`: System prompts for the AI and search decision module.
  - `searchOrNot.py`: Main logic for search decisions, streaming responses, and user interaction.
- **Ollama Integration**: Leverages local or cloud-based LLMs (e.g., Llama 3.1) for efficient inference.
- **Web Search API**: Integrates with Google Custom Search (or other APIs) to fetch live data.

# AI Assistant with Dynamic Web Search

An AI assistant that decides when to consult live web data and streams up-to-date, context-aware responses.

Built with Python, Ollama (Llama 3.1), and pluggable web search APIs so you get accurate answers when external data is required.

**Highlights**
- Smart search decision: checks if a query needs live data before calling web APIs
- Streaming responses for natural, low-latency conversations
- Modular code: clear separation between prompts, decision logic, search, and streaming

**Repository (key files)**
- `sys_msgs.py` — system & assistant prompts used by the models
- `searchOrNot.py` — main orchestration (search-decision, web fetch, streaming)
- `modelSelection.py` — model configuration (e.g., `llama3.1:8b`)
- `searchAgent.py` — the web search agent and fetch utilities
- `requirements.txt` — Python dependencies

**Quick Start**
1. Create and activate a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate
```
2. Install dependencies:
```bash
pip install -r requirements.txt
```
3. Configure environment variables (create a `.env`):
- `SEARCH_API_KEY` — API key for your chosen web search provider
- `OLLAMA_HOST` / `OLLAMA_MODEL` — if using Ollama or custom model endpoints

4. Run the agent (example):
```bash
python searchAgent.py
```

**How it works (brief)**
1. The user asks a question.
2. The search-decision logic (in `searchOrNot.py`) inspects the prompt and conversation history to decide if live web data is needed.
3. If needed, the agent performs targeted searches (Google Custom Search, Bing, or other API) and gathers citations.
4. The LLM (configured in `modelSelection.py`) composes a streamed, context-aware answer that includes up-to-date information.

**Example Use Case**
- Q: "What’s the latest on AI regulation in the EU?"
- System: decides a web lookup is required → fetches recent sources → returns a summarized, cited response.

**Configuration & Models**
- Edit `modelSelection.py` to change which LLM the project uses (default: `llama3.1:8b`).

**Development notes**
- Prompts and system messages are stored in `sys_msgs.py` for easy iteration.
- The web search integration is intentionally pluggable — swap providers by changing the client in `searchAgent.py`.

**Contribution & Next steps**
- Add tests for the search decision heuristics.
- Add more search integrations and caching for rate limits.

