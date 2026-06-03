from dotenv import load_dotenv
load_dotenv()

import os
import pdfplumber

from langchain_core.documents import Document

from langchain_text_splitters import RecursiveCharacterTextSplitter

from langchain_openai import OpenAIEmbeddings

from langchain_community.vectorstores import FAISS


def extract_pdf_text(pdf_path):

    all_text = ""

    with pdfplumber.open(pdf_path) as pdf:

        for page in pdf.pages:

            text = page.extract_text()

            if text:
                all_text += text + "\n"

    return all_text


def create_vectorstore(pdf_folder):

    documents = []

    pdf_files = [
        f for f in os.listdir(pdf_folder)
        if f.endswith(".pdf")
    ]

    for pdf in pdf_files:

        pdf_path = os.path.join(pdf_folder, pdf)

        print(f"Reading: {pdf}")

        text = extract_pdf_text(pdf_path)

        doc = Document(
            page_content=text,
            metadata={"source": pdf}
        )

        documents.append(doc)

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1500,
        chunk_overlap=300
    )

    docs = splitter.split_documents(documents)

    print(f"Total chunks: {len(docs)}")

    embeddings = OpenAIEmbeddings(
        model="text-embedding-3-small"
    )

    vectorstore = FAISS.from_documents(
        docs,
        embeddings
    )

    vectorstore.save_local("vectorstore")

    print("Vector DB Created Successfully")