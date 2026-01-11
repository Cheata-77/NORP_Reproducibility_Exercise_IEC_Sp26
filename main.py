import os
from ingest import load_documents
from rag_pipeline import RAGPipeline
import requests
import json
from Crime_API import run_query
import re

# API Information
API_URL = "https://openrouter.ai/api/v1/chat/completions"
API_KEY = "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"
MODEL = "mistralai/devstral-2512:free"

def test_llm_api():
    question = "What is the capital of France?"
    context = "France is a country in Europe. Its capital is Paris."
    response = query_llm_api(question, context)
    print("LLM API Test Response:\n", response)

def query_llm_api(question, context):
    # API_KEY = os.getenv("OPENROUTER_API_KEY")
    
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    data = {
        "model": MODEL,
        "messages": [
            {   
                "role": "system", 
                "content": 
                    "You are a SoQL query generator for a Socrata dataset. \
                    You must generate SoQL parameters for the question ONLY using the provided context examples. \
                    Do NOT invent fields, filters, or functions. \
                    If the context does not contain enough information to answer the question, \
                    output exactly: NOT_ENOUGH_CONTEXT. \
                    Your output must be a single valid JSON object containing ONLY SoQL parameters \
                    (e.g., $select, $where, $group, $order, $limit). \
                    Do not include explanations, comments, or extra text."
            },
            {"role": "user", "content": f"Context: {context}\n\nQuestion: {question}"}
        ],
    }
    
    response = requests.post(API_URL, headers=headers, data=json.dumps(data))
    if response.status_code == 200:
        return response.json()['choices'][0]['message']['content']
    else:
        return f"Error: {response.status_code}, {response.text}"
    

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
    
    # Append Question to the answer for context
    llm_answer = query_llm_api(question, "\n\n".join(answer))
    print("\nLLM Response:\n", llm_answer)
    
    # Extract json in {} and run the query
    
    output_df = None
    
    json_str = re.search(r"\{.*\}", llm_answer, re.DOTALL)
    if json_str:
        soql_params = json.loads(json_str.group())
        output_df = run_query(soql_params)
        
        # Print top 5 rows of the dataframe
        if output_df is not None:
            print("\nQuery Result (top 5 rows):\n", output_df.head())
        else:
            print("No data returned from the query.")
            
    else:
        print("No valid JSON found in LLM response.")
    
if __name__ == "__main__":
    # test_llm_api()
    main()