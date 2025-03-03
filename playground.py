import openai
from phi.agent import Agent
import phi.api
from phi.model.groq import Groq
from phi.model.openai import OpenAIChat
from phi.tools.yfinance import YFinanceTools
from phi.tools.duckduckgo import DuckDuckGo
from dotenv import load_dotenv

import os
import phi
from phi.playground import Playground, serve_playground_app

# Load environment variables from .env file
load_dotenv()

PHI_API_KEY = os.getenv("PHI_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

## Websearch Agent #1
web_search_agent = Agent(
    name='Web Search Agent',
    role='Search the web for information', 
    model=Groq(id='llama3-70b-8192', api_key=GROQ_API_KEY), 
    tools=[DuckDuckGo(), YFinanceTools(stock_price=True, analyst_recommendations=True, stock_fundamentals=True, company_news=True)],
    instructions=["Provide well-structured, concise, and insightful financial analysis with clear justifications.", "Ensure all financial data is accurate and sourced from reliable sources.", "Use markdown tables to neatly present stock prices, analyst recommendations, and company fundamentals.", "Explain financial metrics in an intuitive manner for better user understanding.", "Answer basic queries like what tools you use, more about yourself, and how you can assist the user."],
    show_tool_calls=True,
    markdown=True,
)

## Financial Agent #2
financial_agent = Agent(
    name='Financial AI Agent',
    role='Retrieve financial data', 
    model=Groq(id='llama3-70b-8192', api_key=GROQ_API_KEY), 
    tools=[YFinanceTools(stock_price=True, analyst_recommendations=True, stock_fundamentals=True, company_news=True), DuckDuckGo()],
    instructions=["Provide well-structured, concise, and insightful financial analysis with clear justifications.", "Ensure all financial data is accurate and sourced from reliable sources.", "Use markdown tables to neatly present stock prices, analyst recommendations, and company fundamentals.", "Explain financial metrics in an intuitive manner for better user understanding.", "Answer basic queries like what tools you use, more about yourself, and how you can assist the user."],
    show_tool_calls=True,
    markdown=True,
)

## Playground Application
app = Playground(agents=[financial_agent, web_search_agent]).get_app()

if __name__ == '__main__':
    serve_playground_app('playground:app', reload=True)
