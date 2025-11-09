from fastapi import FastAPI
from langserve import add_routes
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv
import os

 
load_dotenv()

 
os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")
os.environ["LANGSMITH_API_KEY"] = os.getenv("LANGSMITH_API_KEY")
os.environ["LANGSMITH_TRACING"] = os.getenv("LANGSMITH_TRACING")
os.environ["LANGSMITH_ENDPOINT"] = os.getenv("LANGSMITH_ENDPOINT")
os.environ["LANGSMITH_PROJECT"] = os.getenv("LANGSMITH_PROJECT")
 
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant. Please respond to user queries."),
    ("user", "Question: {question}")
])
llm = ChatGroq(model="llama-3.1-8b-instant", temperature=0)
output_parser = StrOutputParser()
chain = prompt | llm | output_parser

 
app = FastAPI(title="LangChain LLM API with LangServe + LangSmith")

 
add_routes(
    app,
    chain,
    path="/llm",
    token_feedback_config={
        "enabled": True,
        "project": os.getenv("LANGSMITH_PROJECT"),
        "key_configs": [
            {
                "key": os.getenv("LANGSMITH_API_KEY")
            }
        ]
    }
)

 
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.app:app", host="0.0.0.0", port=8000, reload=True)
