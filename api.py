import os
import sys
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
from typing import Optional

# Ensure environment variables (.env) are loaded
load_dotenv()

# Import the main pipeline runner from your local Pipeline.py
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from Pipeline import run_research_pipeline

# 1. Initialize FastAPI App
app = FastAPI(
    title="Multi-Agent AI Research API",
    description="FastAPI backend executing Search, Reader, Writer, and Critic agents."
)

# 2. Configure CORS Middleware
# Allows your React/Vite frontend (e.g., localhost:5173) to communicate with this backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Restrict to specific domains in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 3. Define Request Data Model (Matches input required by run_research_pipeline)
class ResearchRequest(BaseModel):
    topic: str
    url: Optional[str] = None

# 4. Root Health Check Endpoint
@app.get("/")
def read_root():
    return {"status": "online", "message": "Multi-Agent System API is operational"}

# 5. Pipeline Execution Endpoint
@app.post("/api/research")
async def execute_research(request: ResearchRequest):
    if not request.topic.strip():
        raise HTTPException(status_code=400, detail="Topic cannot be empty")
        
    try:
        # Executes Search -> Reader -> Writer -> Critic pipeline
        results = run_research_pipeline(topic=request.topic)
        
        # Returns structured state object to the frontend
        return {
            "status": "success",
            "data": {
                "search_results": results.get("search_results", ""),
                "scraped_content": results.get("scraped_content", ""),
                "report": results.get("report", ""),
                "feedback": results.get("feedback", "")
            }
        }
    except Exception as e:
        print("Pipeline Execution Error:", str(e))  # Prints backend traceback to terminal
        raise HTTPException(status_code=500, detail=str(e))