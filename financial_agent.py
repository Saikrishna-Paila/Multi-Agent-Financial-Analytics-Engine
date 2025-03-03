import os
from dotenv import load_dotenv
import openai
from phi.agent import Agent
from phi.model.groq import Groq
from phi.tools.yfinance import YFinanceTools
from phi.tools.duckduckgo import DuckDuckGo

# Load environment variables from .env
load_dotenv()

# Retrieve API keys from environment variables
PHI_API_KEY = os.getenv("PHI_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

## Websearch Agent #1
web_search_agent = Agent(
    name='Web Search Agent',
    role='Search the web for information', 
    model=Groq(id="llama3-70b-8192", api_key=GROQ_API_KEY), 
    tools=[DuckDuckGo()],
    instructions=["Always include the source where you are getting the data from"],
    show_tool_calls=True,
    markdown=True,
)

## Financial Agent #2
financial_agent = Agent(
    name='Financial AI Agent',
    role='Retrieve financial data', 
    model=Groq(id="llama3-70b-8192", api_key=GROQ_API_KEY), 
    tools=[
        YFinanceTools(stock_price=True, analyst_recommendations=True, stock_fundamentals=True, company_news=True),
    ],
    instructions=["Use tables to display the data"],
    show_tool_calls=True,
    markdown=True,
)

## Workflow
multi_ai_agent = Agent(
    team=[web_search_agent, financial_agent],
    name='Financial Bot',
    role='Retrieve financial data',
    instructions=["Always include sources", "Use tables to display the data"],
    show_tool_calls=True,
    markdown=True,
)

# Execute the request
multi_ai_agent.print_response("Summarize analyst recommendations and share the latest news for google", stream=False)
