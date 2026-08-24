from langchain.tools import tool
import requests
from bs4 import BeautifulSoup
from tavily import TavilyClient
import os
from rich import print
from dotenv import load_dotenv
load_dotenv()

#1 TOOL
tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

@tool
def web_search(query:str) ->str:
    """Search the web for recent & reliable information on a topic.Returns titles, URLs, & snippets"""
    results=tavily.search(query=query,max_results=5)
    
    out=[]
    for r in results["results"]:
        out.append(
            f"Title: {r['title']}\nURL: {r['url']}\nSnippet: {r['content'][:300]}\n"
        ) 
    return "\n-----\n".join(out)

# print(web_search.invoke("What is recent news on Indias contribution in AI, Maths, Medical science?"))


scrape_count = 0
@tool
def scrape_url(url: str) -> str:
    """Scrape and return clean text from a maximum of 3 URLs."""
    global scrape_count

    if scrape_count >= 3:
        return "Scraping limit reached. Only 3 websites can be scraped."

    try:
        scrape_count += 1

        resp = requests.get(
            url,
            timeout=8,
            headers={"User-Agent": "Mozilla/5.0"}
        )

        soup = BeautifulSoup(resp.text, "html.parser")

        for tag in soup(["script", "style", "nav", "footer"]):
            tag.decompose()

        return soup.get_text(separator=" ", strip=True)[:300]

    except Exception as e:
        return f"Could not scrape URL: {str(e)}"
    
        
    

