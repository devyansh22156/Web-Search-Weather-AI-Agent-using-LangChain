import os
import certifi
from dotenv import load_dotenv

import streamlit as st

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.tools.tavily_search import TavilySearchResults

from langchain import hub
from langchain.tools import tool
from langchain.agents import create_react_agent, AgentExecutor # reasoning and acting agent

import requests
# load environment variables from .env file

os.environ["SSL_CERT_FILE"] = certifi.where() # set the SSL certificate file path for secure connections
# why do we need to set the SSL certificate file path?
# Setting the SSL certificate file path is necessary to ensure that the application can establish secure connections when making API calls or accessing resources over HTTPS. The SSL certificate file contains trusted certificates that allow the application to verify the identity of the server it is connecting to, ensuring that the communication is secure
load_dotenv() # load environment variables from .env file

# Streamlit page configuration

st.set_page_config(
    page_title="LangChain Agent Demo",
    page_icon="🤖",
    layout="centered"
)

st.title("Agentic AI Assistant")
st.markdown("Search + Weather AI agent using LangChain")


GEMINI_API_KEY = os.getenv("GEMINI_API_KEY") 
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
WEATHER_STACK_API_KEY = os.getenv("WEATHER_STACK_API_KEY")
search_tool = TavilySearchResults(max_results=3, api_key=TAVILY_API_KEY)
# result = search_tool.invoke("What is the latest news about AI?")
# result
# Intializing our large language model (LLM) with the Gemini API key

@tool
def get_weather_data(location: str) -> str:


    '''
    Fetches the current weather data for a given location using the WeatherStack API.
    '''

    url = (
        f"https://api.weatherstack.com/current?"
        f"access_key={WEATHER_STACK_API_KEY}&query={location}"
    )

    response = requests.get(url)

    data = response.json()

    if "current" not in data:
        return f"Could not retrieve weather data for {location}. Please check the location and try again."

    return (
        f"City: {location}\n"
        f"Temperature: {data['current']['temperature']}°C\n"
        f"Weather: {data['current']['weather_descriptions'][0]}\n"
        f"Humidity: {data['current']['humidity']}%"
    )


llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash", 
    google_api_key=GEMINI_API_KEY, 
    temperature=0.2
)
# result = llm.invoke("What year is it?")
# result
from langsmith import Client

# prompt for the agent to use, we can pull it from the LangSmith Hub

client = Client()

prompt = client.pull_prompt("hwchase17/react")

# prompt
# tools

tools = [search_tool, get_weather_data]
# Create the agent using the LLM, tools, and prompt

agent = create_react_agent(
    llm=llm,
    tools=tools,
    prompt=prompt 
)

# Executer 

agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True,
    return_intermediate_steps=True,
    handle_parsing_errors=True
)

# UI Input

user_query = st.text_input(
    "Enter your query:",
    placeholder="Example: Find the Capital of France and the latest news about AI."
)


# Run Agent

if st.button("Run Agent"):

    if user_query:
        with st.spinner("Agent is thinking..."):

            try:
                response = agent_executor.invoke({
                    "input": user_query
                })

                st.success("Response Generated!")
                st.write(response["output"])
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")

    else:
        st.warning("Please enter a query before running the agent.")
