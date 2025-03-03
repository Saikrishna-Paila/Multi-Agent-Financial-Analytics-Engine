import os
from dotenv import load_dotenv

import streamlit as st

# Import phi modules first
from phi.agent import Agent
from phi.model.groq import Groq
from phi.model.openai import OpenAIChat
from phi.tools.yfinance import YFinanceTools
from phi.tools.duckduckgo import DuckDuckGo

from pathlib import Path
from phi.agent.python import PythonAgent





import phi
from phi.playground import Playground, serve_playground_app

# Load environment variables from .env file
load_dotenv()

PHI_API_KEY = os.getenv("PHI_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

## Financial Agent
financial_agent = Agent(
    name='Financial AI Agent',
    role='Retrieve financial data', 
    model=Groq(id='llama3-70b-8192', api_key=GROQ_API_KEY), 
    tools=[YFinanceTools(stock_price=True, analyst_recommendations=True, stock_fundamentals=True, company_news=True)],
    instructions=["Provide well-structured, concise, and insightful financial analysis with clear justifications.", 
                  "Ensure all financial data is accurate and sourced from reliable sources.", 
                  "Use markdown tables to neatly present stock prices, analyst recommendations, and company fundamentals.", 
                  "Explain financial metrics in an intuitive manner for better user understanding.", 
                  "Answer basic queries like what tools you use, more about yourself, and how you can assist the user."],
    show_tool_calls=True,
    markdown=True,
)

## Web Search Agent
web_search_agent = Agent(
    name='Web Search Agent',
    role='Search the web for information', 
    model=Groq(id='llama3-70b-8192', api_key=GROQ_API_KEY), 
    tools=[DuckDuckGo()],
    instructions=["Provide accurate web search results with citations.", 
                  "Ensure information is current and relevant.", 
                  "Answer general knowledge queries effectively."],
    show_tool_calls=True,
    markdown=True,
)

## Streamlit Interface
st.title("Financial and Web Search AI Bot")
st.write("Interact with the Financial AI Agent and Web Search Agent for financial insights and web-based queries.")

user_input = st.text_input("Enter your query:")
if user_input:
    if any(keyword in user_input.lower() for keyword in ["stock", "price", "financial", "market", "investment"]):
        response = financial_agent.run(user_input)
    else:
        response = web_search_agent.run(user_input)

    st.write(response)

## Playground Application
app = Playground(agents=[financial_agent, web_search_agent]).get_app()

# Remove `serve_playground_app` since it's not needed for Streamlit
