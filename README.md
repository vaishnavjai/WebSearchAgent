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

### Example Workflow
1. User asks: *"What’s the latest news about AI regulations in the EU?"*
2. System checks if the conversation lacks context → Triggers a web search.
3. Assistant responds with up-to-date information, e.g.:
   > *"As of June 2024, the EU’s AI Act has entered enforcement phase, targeting high-risk applications like biometrics and autonomous systems..."*

---

## 📁 Repository Structure
├── sys_msgs.py          # System prompts for AI and search logic
├── searchOrNot.py        # Main script (search decision + streaming)
├── requirements.txt      # Dependencies (Ollama, web search API client)
├── .env                 # Environment variables (API keys, etc.)
└── README.md            # You're reading this!


---

## 🛠️ Setup & Installation

### Prerequisites
- Refer to requirements.txt

### Quick Start
1. Clone the repo:
   ```bash
   git clone https://github.com/vaishnavjai/WebSearchAgent
   cd WebSearchAgent
    ```