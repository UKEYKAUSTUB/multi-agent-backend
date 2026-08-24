from langchain.agents import create_agent
from langchain_mistralai import ChatMistralAI
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from tools import web_search,scrape_url 

load_dotenv()
# Model setup
Model=ChatMistralAI(model="mistral-small-2603")

#1st Agent
def build_search_agent():
    return create_agent(
        model=Model,
        tools=[web_search]
    )
    
#2nd Agent
def build_reader_agent():
    return create_agent(
        model=Model,
        tools=[scrape_url]
    )
    
#Writer Chain
writer_prompt=ChatPromptTemplate.from_messages([
    ('system',"You are an expert research write.Write concise, factual and structured reports. Avoid unnecessary explanations and long paragraphs"),
    ('human',"""Write a concise research report on the topic below.
    Topic:{topic}
    Research Gathered:
    {research}
    Use EXACTLY this structure:

Introduction:
Write 2-3 sentences.

Key Findings:
- Finding 1: 2-3 sentences.
- Finding 2: 2-3 sentences.
- Finding 3: 2-3 sentences.

Conclusion:
Write 2-3 sentences.

Sources:
- URL
- URL

IMPORTANT RULES:
- Include exactly 3 key findings.
- Each key finding must be maximum 2-3 sentences.
- Do not write large paragraphs.
- Use simple and direct language.
- Do not add sections other than those requested.
- List all URLs found in the research.
    """),
])

writer_chain = writer_prompt | Model | StrOutputParser()

#critic_chain
critic_prompt = ChatPromptTemplate.from_messages([
     ("system", "You are a sharp and constructive research critic. Be honest and specific.Never write long paragraphs"),
    ("human", """Review the research report below and evaluate it strictly.

Report:
{report}

espond in EXACTLY this format:

Score: X/10

Strengths:
- One short sentence.
- One short sentence.
- One short sentence.

Areas to Improve:
- One short sentence.
- One short sentence.
- One short sentence.

One line verdict:
One concise sentence.

IMPORTANT RULES:
- Maximum 3 strengths.
- Maximum 3 areas to improve.
- Each bullet must contain ONLY one sentence.
- Each bullet should be maximum 20 words.
- One line verdict must be maximum 20 words.
- Do not use paragraphs.
- Do not repeat the report.

..."""),
])

critic_chain = critic_prompt | Model | StrOutputParser()
