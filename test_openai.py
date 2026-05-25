from dotenv import load_dotenv
load_dotenv()

import os

from openai import OpenAI

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

response = client.embeddings.create(
    model="text-embedding-3-small",
    input="test"
)

print("OPENAI WORKING")