from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
import streamlit as st
import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Groq API key
os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")

# LangSmith tracking (optional)
os.environ["LANGCHAIN_TRACING_V2"] = os.getenv("LANGSMITH_TRACING", "true")
os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGSMITH_API_KEY", "")
os.environ["LANGCHAIN_ENDPOINT"] = os.getenv("LANGSMITH_ENDPOINT", "https://api.smith.langchain.com")
os.environ["LANGCHAIN_PROJECT"] = os.getenv("LANGSMITH_PROJECT", "default")

# Prompt Template
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a helpful assistant. Please respond to the user queries"),
        ("user", "Question:{question}")
    ]
)

# Streamlit framework
st.title('Langchain Demo With Groq LLM')
input_text = st.text_input("Search the topic you want")

# Groq LLM
llm = ChatGroq(model="llama-3.1-8b-instant", temperature=0)
output_parser = StrOutputParser()

# Create chain
chain = prompt | llm | output_parser

if input_text:
    # Use the chain to get response
    response = chain.invoke({"question": input_text})
    st.write(response)