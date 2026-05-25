from fastapi import FastAPI

from fastapi.middleware.cors import CORSMiddleware

from pydantic import BaseModel

from utils.rag_chain import load_qa_chain


app = FastAPI()

# ENABLE CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

qa_chain = load_qa_chain()


class QuestionRequest(BaseModel):

    question: str


@app.post("/chat")

def chat(request: QuestionRequest):

    response = qa_chain.invoke({
        "query": request.question
    })

    return {
        "answer": response["result"]
    }