# LangChain Agent Demo

This folder contains a small LangChain agent project with two entry points:

- [app.py](app.py) runs a Streamlit UI for chatting with the agent.
- [main.py](main.py) runs a simple command-line demo.

The agent combines Google Gemini, Tavily search, and a WeatherStack tool.

## Setup

Create a Python 3.11 environment and install the dependencies:

```bash
conda create -n langagent python=3.11 -y
conda activate langagent
pip install -r requirements.txt
```

## Environment Variables

Create a `.env` file in this folder and add the API keys used by the app:

```env
GEMINI_API_KEY=your_gemini_api_key
TAVILY_API_KEY=your_tavily_api_key
WEATHER_STACK_API_KEY=your_weatherstack_api_key
```

If you use the Streamlit app, the prompt is pulled from LangSmith Hub, so you may also need LangSmith credentials depending on your account setup.

## Run the App

Start the Streamlit UI:

```bash
streamlit run app.py
```

## Run the Console Demo

Run the command-line example:

```bash
python main.py
```

## What The Agent Can Do

- Search the web with Tavily.
- Look up current weather for a location.
- Combine tool results into a single answer using a ReAct-style agent.

## Project Structure

- [app.py](app.py) - Streamlit interface and agent execution.
- [main.py](main.py) - Minimal script version of the agent.
- [requirements.txt](requirements.txt) - Python dependencies.
- [research/agent_demo.ipynb](research/agent_demo.ipynb) - Notebook used for experimentation.

## Notes

- The app sets the SSL certificate path with `certifi` for HTTPS requests.
- Weather lookups depend on the WeatherStack API returning data for the requested location.