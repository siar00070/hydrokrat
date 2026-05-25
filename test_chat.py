from utils.rag_chain import load_qa_chain

qa_chain = load_qa_chain()

while True:

    question = input("\nAsk Question: ")

    if question.lower() == "exit":
        break

    response = qa_chain.invoke({
        "query": question
    })

    print("\nANSWER:\n")

    print(response["result"])

    print("\nSOURCE DOCUMENTS:\n")

    for doc in response["source_documents"]:

        print(doc.page_content[:500])

        print("\n-----------------\n")