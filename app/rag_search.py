from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

DB_PATH = "vectorstore"

embeddings = OpenAIEmbeddings()

db = FAISS.load_local(
    DB_PATH,
    embeddings,
    allow_dangerous_deserialization=True
)

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)


def ask_hydrokrat_rag(user_question):

    docs = db.similarity_search(
        user_question,
        k=4
    )

    context = "\n\n".join(
        [doc.page_content for doc in docs]
    )

    system_prompt = f"""
You are Hydrokrat AI.

You are a professional KSB pump selection engineer.

Use ONLY the provided catalogue information.

Catalogue Context:
{context}

Provide:
- Pump recommendations
- Engineering explanations
- Hydraulic suggestions
- OEM accurate information
"""

    response = client.chat.completions.create(
        model="gpt-4.1-mini",

        messages=[
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": user_question
            }
        ],

        temperature=0.2
    )

    return response.choices[0].message.content