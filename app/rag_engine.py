import os
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv

load_dotenv()

CATALOGUE_FOLDER = "catalogues"

DB_PATH = "vectorstore"

embeddings = OpenAIEmbeddings()


def load_catalogues():

    documents = []

    for file in os.listdir(CATALOGUE_FOLDER):

        if file.endswith(".pdf"):

            pdf_path = os.path.join(
                CATALOGUE_FOLDER,
                file
            )

            loader = PyPDFLoader(pdf_path)

            docs = loader.load()

            documents.extend(docs)

    return documents


def build_vector_database():

    docs = load_catalogues()

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1200,
        chunk_overlap=150
    )

    split_docs = splitter.split_documents(docs)

    db = FAISS.from_documents(
        split_docs,
        embeddings
    )

    db.save_local(DB_PATH)

    print("✅ Vector DB created")


if __name__ == "__main__":

    build_vector_database()