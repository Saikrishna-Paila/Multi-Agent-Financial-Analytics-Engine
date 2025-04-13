# Multi-Agent-Financial-Analytics-Engine

## Overview
This project is a **Financial Agent Bot** that provides financial insights using AI. The bot leverages external APIs such as OpenAI and Groq, along with financial data sources like **Yahoo Finance**. It is built using **FastAPI** for backend processing and includes a **playground** interface for user interaction.

## Features
- Fetch real-time financial data.
- AI-powered financial insights.
- Integration with OpenAI and Groq.
- Web-based interface for interaction.

## Prerequisites
Before running the project, ensure you have the following installed:
- **Python 3.8+**
- **Google Chrome Browser** (for playground access)
- **Required Python packages** (see `requirements.txt`)

## Installation
```sh
# Clone the repository
git clone https://github.com/Saikrishna-Paila/Multi-Agent-Financial-Analytics-Engine.git
cd <repository-folder>

# Install dependencies
pip install -r requirements.txt
```

## API Keys Configuration
This project requires API keys for **OpenAI**, **Groq**, **Yahoo Finance**, and **PhiData**.
This project requires API keys for **OpenAI**, **Groq**, and **Yahoo Finance**.

### Where to find API keys?
- **PhiData API Key**: Required for API endpoint connection. Get it from [PhiData](https://phidata.com/).
- All API keys are free (with limited access).
- **OpenAI API Key**: [Get it here](https://platform.openai.com/signup)
- **Groq API Key**: [Get it here](https://groq.com/)
- **Yahoo Finance**: No API key required

### How to add API keys?
- Create a `.env` file in the project root directory.
- Add the following environment variables:

```sh
PHI_API_KEY="your API key"
OPENAI_API_KEY="your API key"
GROQ_API_KEY="your API key"
```
- Ensure that `.env` is loaded in the project code to access API keys securely.
- Open `financial_bot.py` and `playground.py`
- Locate the `API_KEY` variables inside these files.
- Replace placeholder values with your actual API keys.

## Running the Project
```sh
# Run the financial bot
python financial_bot.py  # Output will be displayed in the terminal

# Run the playground
python playground.py  # Allows interaction with the bot
```

## Connecting to API Endpoint via PhiData
1. Go to the **PhiData** website and connect to the API endpoint.
2. Ensure your local server is running.

## Chatting with the Bot (Chrome Only)
- Open **PhiData**, log in to your account that has an API key.
- Ensure the **PhiData API key** is added in the `.env` file.
- Connect to the **API endpoint** via PhiData.
- Open Chrome and visit the following URL:

```sh
http://localhost:7777
```
- Start chatting with the bot.
- See the output in the screenshot below.


## Usage Instructions
- Enter financial queries in the **playground UI** or **terminal**.
- The bot fetches and returns financial insights using AI.
- Responses are displayed in the terminal or browser interface.

## Screenshot of Output
![Output Screenshot](https://github.com/Saikrishna-Paila/Multi-Agent-Financial-Analytics-Engine/blob/main/output.png)
[ Click me to see the APP](https://multi-agent-financial-analytics-engine-e5juedtfgzhurwxmpjbcpv.streamlit.app)

