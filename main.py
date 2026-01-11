import os
from ingest import load_documents
from rag_pipeline import RAGPipeline

def main():
    print("Entering Main")
    docs_dir = "data"
    texts = load_documents(docs_dir)
    if not texts:
        print("No documents found. Please add files to data/")
        return

    rag = RAGPipeline(texts)
    question = input("Enter your question: ")
    answer = rag.query(question)
    print("\nAnswer:\n", answer)

if __name__ == "__main__":
    main()