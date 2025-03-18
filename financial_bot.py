import os
from dotenv import load_dotenv
import streamlit as st
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

# Page config for dark mode
st.set_page_config(
    page_title="Financial AI Assistant",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Apply custom CSS for dark mode
st.markdown("""
    <style>
    /* Dark mode styles */
    .stApp {
        background-color: #0E1117;
        color: #FAFAFA;
    }
    
    /* Chat message styling */
    .chat-message {
        padding: 1.5rem;
        border-radius: 0.8rem;
        margin-bottom: 1rem;
        display: flex;
        flex-direction: column;
        border: 1px solid #2D3748;
    }
    .user-message {
        background-color: #1E2530;
        margin-left: 2rem;
    }
    .bot-message {
        background-color: #2D3748;
        margin-right: 2rem;
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background-color: #1E2530;
    }
    
    /* Input field styling */
    .stTextInput > div > div > input {
        background-color: #1E2530;
        color: #FAFAFA;
    }
    
    /* Button styling */
    .stButton > button {
        background-color: #2D3748;
        color: #FAFAFA;
        border: 1px solid #4A5568;
    }
    .stButton > button:hover {
        background-color: #4A5568;
        color: #FAFAFA;
        border: 1px solid #718096;
    }
    </style>
""", unsafe_allow_html=True)

def create_financial_agent():
    return Agent(
        name='Financial AI Agent',
        role='Expert Financial Analyst and Advisor',
        model=Groq(
            id='llama3-70b-8192',
            api_key=GROQ_API_KEY,
            temperature=0.7,
            max_tokens=2048
        ),
        tools=[
            YFinanceTools(
                stock_price=True,
                analyst_recommendations=True,
                stock_fundamentals=True,
                company_news=True
            )
        ],
        instructions=[
            "You are an expert financial analyst and advisor.",
            "When analyzing stocks or financial data:",
            "1. Always provide current stock prices and key metrics first",
            "2. Include relevant financial ratios and their interpretation",
            "3. Analyze recent trends and market sentiment",
            "4. Provide clear, actionable insights",
            "5. Use markdown tables for data presentation",
            "6. Include relevant news that might impact the stock",
            "7. Always cite your data sources",
            "Format responses in a clear, structured manner with sections for:",
            "- Current Data",
            "- Analysis",
            "- Recommendations",
            "- Additional Context"
        ],
        show_tool_calls=False,
        markdown=True,
        async_mode=False
    )

def create_web_search_agent():
    return Agent(
        name='Web Search Agent',
        role='Research and Information Specialist',
        model=Groq(
            id='llama3-70b-8192',
            api_key=GROQ_API_KEY,
            temperature=0.7,
            max_tokens=2048
        ),
        tools=[DuckDuckGo()],
        instructions=[
            "You are a research and information specialist.",
            "When searching for information:",
            "1. Prioritize recent and reliable sources",
            "2. Provide comprehensive but concise answers",
            "3. Include relevant citations",
            "4. Fact-check information across multiple sources",
            "5. Organize information in a clear, logical structure",
            "6. Highlight key points and important details",
            "Format responses with clear sections for:",
            "- Key Information",
            "- Details",
            "- Sources"
        ],
        show_tool_calls=False,
        markdown=True,
        async_mode=False
    )

# Initialize agents
financial_agent = create_financial_agent()
web_search_agent = create_web_search_agent()

# Initialize session state for chat history
if 'messages' not in st.session_state:
    st.session_state.messages = []

# Main title and description with dark mode friendly emojis
st.title("💰 Financial AI Assistant")
st.markdown("""
<div style='background-color: #1E2530; padding: 1rem; border-radius: 0.8rem; margin-bottom: 1rem;'>
Welcome to your AI Financial Assistant! I can help you with:
<ul>
<li>📈 Stock market analysis and prices</li>
<li>📊 Company fundamentals and news</li>
<li>🔍 General web searches</li>
<li>💡 Financial insights and recommendations</li>
</ul>
</div>
""", unsafe_allow_html=True)

# Sidebar with dark mode styling
with st.sidebar:
    st.title("About")
    st.markdown("""
    <div style='background-color: #1E2530; padding: 1rem; border-radius: 0.8rem;'>
    <h4>This AI assistant combines:</h4>
    <ul>
    <li>📊 Financial data analysis</li>
    <li>🌐 Web search capabilities</li>
    <li>📈 Real-time market insights</li>
    </ul>
    
    <h4>Use natural language to ask about:</h4>
    <ul>
    <li>💹 Stock prices and trends</li>
    <li>🏢 Company analysis</li>
    <li>📰 Market news</li>
    <li>ℹ️ General information</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)
    
    # Clear chat button with dark mode styling
    if st.button("🗑️ Clear Chat History"):
        st.session_state.messages = []
        st.rerun()

# Display chat messages with dark mode styling
for message in st.session_state.messages:
    with st.container():
        if message["role"] == "user":
            st.markdown(f"""<div class="chat-message user-message">
                        💬 <span style='color: #9FA6B2;'>You:</span> {message["content"]}</div>""", 
                        unsafe_allow_html=True)
        else:
            st.markdown(f"""<div class="chat-message bot-message">
                        🤖 <span style='color: #9FA6B2;'>AI:</span> {message["content"]}</div>""", 
                        unsafe_allow_html=True)

# Chat input with dark mode styling
user_input = st.chat_input("💭 Ask me anything about finance or general information...")

if user_input:
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    try:
        # Show a loading spinner while processing
        with st.spinner('Processing your request...'):
            # Determine which agent to use based on the query
            if any(keyword in user_input.lower() for keyword in [
                "stock", "price", "financial", "market", "investment",
                "company", "shares", "dividend", "trading", "nasdaq",
                "nyse", "dow", "sp500", "s&p", "earnings"
            ]):
                response = financial_agent.run(user_input)
            else:
                response = web_search_agent.run(user_input)
            
            # Extract the content from the response
            if hasattr(response, 'content'):
                response_content = response.content
            elif isinstance(response, str):
                response_content = response
            else:
                # Try to get the last message from response messages if available
                if hasattr(response, 'messages') and response.messages:
                    last_message = response.messages[-1]
                    response_content = last_message.content if hasattr(last_message, 'content') else str(response)
                else:
                    response_content = str(response)
            
            # Clean up the response content
            response_content = response_content.strip()
            if response_content.startswith('Running:'):
                # Remove the "Running:" prefix and any tool call information
                response_content = response_content.split('\n\n', 1)[-1]
            
            # Add assistant response to chat history
            st.session_state.messages.append({"role": "assistant", "content": response_content})
            
    except Exception as e:
        error_message = f"Sorry, I encountered an error: {str(e)}\nPlease try rephrasing your question."
        st.session_state.messages.append({"role": "assistant", "content": error_message})
    
    # Rerun to update the chat display
    st.rerun()

# Footer with dark mode styling
st.markdown("---")
st.markdown("<p style='text-align: center; color: #718096;'>Created by saikrishna Paila</p>", unsafe_allow_html=True)
