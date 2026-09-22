from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os

# ---------- Load Environment ----------
load_dotenv()

groq_api_key = os.getenv("GROQ_API_KEY")
if not groq_api_key:
    raise ValueError("GROQ_API_KEY not found in .env file!")

# ---------- Model ----------
model = ChatGroq(
    model="openai/gpt-oss-20b",
    groq_api_key=groq_api_key,
    temperature=0.7,
)

# ---------- Prompt Template ----------
system_template = "Translate the following into {language}:"
prompt_template = ChatPromptTemplate.from_messages([
    ('system', system_template),
    ('user', '{text}')
])

# ---------- Parser & Chain ----------
parser = StrOutputParser()
chain = prompt_template | model | parser

# ---------- FastAPI App ----------
app = FastAPI(
    title="LangChain Server",
    version="1.0",
    description="A simple API server using FastAPI + LangChain",
)

# ---------- Request / Response Models (Pydantic v2) ----------
class ChainInput(BaseModel):
    language: str
    text: str

class InvokeRequest(BaseModel):
    input: ChainInput
    config: dict = {}
    kwargs: dict = {}

class InvokeResponse(BaseModel):
    output: str

# ---------- Routes ----------
@app.get("/")
def root():
    return {"status": "ok", "message": "Backend is running"}

@app.post("/chain/invoke", response_model=InvokeResponse)
async def invoke(request: InvokeRequest):
    try:
        result = chain.invoke({
            "language": request.input.language,
            "text": request.input.text,
        })
        return InvokeResponse(output=result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ---------- Run ----------
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)