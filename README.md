```markdown
# ⚡ Autonomous Multi-Agent Research System (Backend)

An autonomous multi-agent backend built with **FastAPI**, **LangChain**, **Mistral AI**, and **Tavily AI**. The service coordinates special-purpose LLM agents to conduct domain web searches, web scraping, factual synthesis, and evaluation scoring.

## 🚀 Multi-Agent Workflow

1. **Search Agent**: Powered by **Tavily API** to perform web searches and gather domain intelligence.
2. **Reader Agent**: Built using **BeautifulSoup4** to parse and extract main-body text from target URLs.
3. **Writer Agent**: Processes unstructured raw data via **Mistral AI** (`mistral-small-latest`) to synthesize structured reports.
4. **Critic Agent**: Evaluates generated reports for factual consistency, logical depth, and structure.

## 🛠️ Tech Stack

- **Framework**: FastAPI (Uvicorn)
- **Agent Orchestration**: LangChain
- **LLM Provider**: Mistral AI (`langchain-mistralai`)
- **Search & Scraping**: Tavily API, BeautifulSoup4, Requests
- **Hosting**: Render

## ⚙️ Local Setup & Running

### 1. Clone & Setup Virtual Environment
```bash
git clone [https://github.com/UKEYKAUSTUB/multi-agent-backend.git](https://github.com/UKEYKAUSTUB/multi-agent-backend.git)
cd multi-agent-backend

python -m venv .venv
# On Windows:
.venv\Scripts\activate
# On macOS/Linux:
source .venv/bin/activate

pip install -r requirements.txt

2. Environment Variables
Create a .env file in the root directory:
MISTRAL_API_KEY=your_mistral_api_key_here
TAVILY_API_KEY=your_tavily_api_key_here


3. Start Local API Server
python -m uvicorn api:app --reload --port 8000


🌐 Deployment (Render)
Environment: Python 3.11

Build Command: pip install -r requirements.txt

Start Command: python -m uvicorn api:app --host 0.0.0.0 --port $PORT

Environment Variables: Add MISTRAL_API_KEY and TAVILY_API_KEY under Render Settings.
