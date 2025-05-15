import os
from langchain_community.llms import Ollama
from langchain.chains import RetrievalQA
from load_retriever import retrieve_documents

# Load Ollama Mistral Model
def load_mistral_model():
    llm = Ollama(
        model="mistral:instruct",  # Use the same model name as you pulled
        temperature=0.1
    )
    print("✅ Mistral LLM loaded from Ollama.")
    return llm

# Build the QA Chain
def build_qa_chain():
    llm = load_mistral_model()

    # ⚡ Instead of building retriever from vectorstore directly,
    # we will manually retrieve and re-rank in each query
    def custom_retriever(query):
        return retrieve_documents(query, k_retrieve=10, k_rerank=5)

    # Define a custom chain-like function
    class ManualRetrievalQA:
        def __init__(self, llm, retriever):
            self.llm = llm
            self.retriever = retriever
        
        def __call__(self, query):
            docs = self.retriever(query)
            context = "\n\n".join([doc.page_content for doc in docs])

            full_prompt = f"""Answer the question based only on the context below:

            Context:
            {context}

            Question: {query}
            Answer:"""

            answer = self.llm.invoke(full_prompt)

            return {
                "result": answer,
                "source_documents": docs
            }

    qa_chain = ManualRetrievalQA(llm=llm, retriever=custom_retriever)
    print("✅ QA Chain successfully built with reranker.")
    return qa_chain

# Example test
if __name__ == "__main__":
    qa_chain = build_qa_chain()

    query = "What are the requirements for MS Accounting admission?"
    result = qa_chain(query)

    print("\n🧠 Answer:")
    print(result["result"])

    print("\n📚 Sources:")
    for doc in result["source_documents"]:
        print(f"- {doc.metadata.get('source_url')}")
