# 🤖 AI-Powered Customer Support Copilot with Memory and Tool Calling

Support agents lose over 60% of their time switching between multiple enterprise tools to gather customer context before drafting a reply. This project resolves this friction by building a production-ready, **100% free-tier** AI Customer Support Copilot. 

The system automatically collects customer context using **Local RAG** for knowledge base searches, a custom **Persistent Memory Layer** for tracking customer preferences, and **LangChain Tool Calling** for live relational CRM/billing database lookups. It then orchestrates these components using an LLM to generate a ready-to-review response in one click via a human-in-the-loop dashboard.

---

## 🔄 System Architecture & User Flow

1. **Ticket Ingestion**: A customer submits an open-text inquiry targeting transaction history, delays, or standard corporate regulations.
2. **Context Assembly**: The FastAPI engine concurrently pulls live relational metrics from SQLite, matches semantic rules from local Markdown/text policies, and surfaces historical notes.
3. **Agentic Synthesis**: The application routes text to a free instance of `gpt-4o-mini` via GitHub Models, matching the customer's preferred communication tone and conditions.
4. **Human Evaluation Interface**: The compiled findings and draft emails are served directly to a Streamlit workspace for human review.

---

## 🛠️ Tech Stack & Free-Tier Configuration

We built this stack to be completely functional with **zero cost dependencies**:

* **Orchestration Engine**: LangChain (v0.3)
* **LLM Provider**: GitHub Models API Gateway (`gpt-4o-mini` / `gpt-4o` running over an OpenAI-compatible endpoint via `langchain-openai`)
* **Vector Infrastructure (RAG & Memory)**: ChromaDB (Local instances running embedded)
* **Embedding Model**: Hugging Face Hub (`all-MiniLM-L6-v2` running completely on local CPU)
* **Relational Data Store**: SQLite3 (Local file-based database)
* **Backend Application Layer**: FastAPI + Uvicorn
* **Frontend Dashboard UI**: Streamlit Framework
* **DevOps & Deployment**: Docker, Docker Compose (Optimized for CPU-only execution layers)

---

## 📁 Project Directory Structure

```text
ai-support-copilot/
├── backend/
│   ├── app/
│   │   ├── agent.py          # Central agentic loop & prompt orchestration
│   │   ├── database.py       # SQLite CRM database schema & seed data
│   │   ├── llm.py            # Free GitHub Models connection interface
│   │   ├── main.py           # FastAPI application & entrypoint
│   │   ├── memory.py         # Custom persistent preference vector store
│   │   ├── rag.py            # Corporate policy indexing engine
│   │   └── tools.py          # LangChain structured database tool calls
│   └── Dockerfile            # Optimized backend container setup
├── frontend/
│   ├── app.py                # Streamlit human-in-the-loop dashboard
│   └── Dockerfile            # Lightweight frontend container setup
├── data/                     # Local persistent storage volume mount
│   ├── chroma_db/            # RAG vector chunks
│   ├── crm.db                # SQLite binary file
│   └── customer_memories_db/ # User preferences vector space
├── .env                      # Universal environment configuration keys
├── docker-compose.yml        # Multi-container orchestration plan
└── requirements.txt          # Shared dependency blueprint

🚀 Installation & Local Development

GITHUB_TOKEN=your_github_personal_access_token_here

python -m venv ai-support-copilot
# Activate on Windows:
.\ai-support-copilot\Scripts\activate

pip install -r requirements.txt

cd backend/app
python main.py

cd frontend
streamlit run app.py

🐋 Option B: Production Container Deployment (Docker Compose)

docker compose builder prune -f

docker compose up --build