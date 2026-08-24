from Agents import build_reader_agent, build_search_agent, writer_chain, critic_chain
from rich import print

def run_research_pipeline(topic:str)->dict:
    state={}
    
    # Search Agent Working
    print("\n"+" ="*50)
    print("step 1 --search agent is working...")
    print("="*50)
    search_agent = build_search_agent()
    search_result= search_agent.invoke({
        "messages":[("user",f"Find reliable,recent & detailed info about :{topic}")]
    })
    raw_content=search_result['messages'][-1].content
    
    # Check if content is returned as a list of dictionaries/blocks
    if isinstance(raw_content, list):
        clean_text = "\n".join(
            item.get("text", "") for item in raw_content 
            if isinstance(item, dict) and item.get("type") == "text"
        )
        state["search_results"] = clean_text
    else:
        state["search_results"] = str(raw_content)

    print("\n search result:\n", state["search_results"])
    
    
    #Step 2 Reader agent
    print("\n"+" ="*50)
    print("step 2 --Reader agent is working...")
    print("="*50)
    
    reader_agent= build_reader_agent()
    reader_result=reader_agent.invoke({
        "messages": [("user",
            f"Based on the following search results about '{topic}', "
            f"pick the most relevant URL and scrape it for deeper content.\n\n"
            f"Search Results:\n{state['search_results'][:800]}"
        )]
    })
    state['scraped_content']= reader_result['messages'][-1].content
    print("\nScraped Content\n",state['scraped_content'])
    
    # step 3 Writer Chain
    print("\n"+" ="*50)
    print("step 3 --Writer agent is drafting the report...")
    print("="*50)
    
    research_combined= (
        f"SEARCH RESULTS: \n{state['search_results']}"
        f"DETAILED SCRAPED CONTENT:\n{state['scraped_content']}"
    )
    state["report"]=writer_chain.invoke(
        {
            "topic":topic,
            "research":research_combined
        }
    )
    print("\n Final report \n",state["report"])
    
    #critic report
    
    print("\n"+" ="*50)
    print("step 4 --Critic agent is reviewing the report...")
    print("="*50)
    state["feedback"]=critic_chain.invoke({
        "report":state["report"]
    })
    print("\n Critic Report \n" ,state["feedback"])
    
    return state

if __name__ =="__main__":
    topic = input("\n Enter a research topic \n")
    run_research_pipeline(topic)