# RAG Pipeline Project

A Retrieval-Augmented Generation (RAG) pipeline implementation for CS 6365 Real-Time Systems coursework.

## Overview

This project implements a RAG system that combines document retrieval with language generation to provide contextually relevant responses. The pipeline uses vector databases for efficient document storage and retrieval, paired with language models for generating accurate responses.

## Features (TBD)

- Document ingestion and preprocessing with `unstructured`
- Vector embeddings and similarity search using `chromadb` and `faiss-cpu`
- Modular pipeline architecture with `langchain`
- Token management and optimization with `tiktoken`

## Installation

1. Clone the repository:
```bash
git clone https://github.gatech.edu/vmanivannan35/RAG-Pipeline.git
cd RAG-Project
```

2. Create and activate the virtual environment:
```bash
python -m venv rag-env
# On Windows:
rag-env\Scripts\activate
# On macOS/Linux:
source rag-env/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Dependencies

The project uses the following key packages (see [requirements.txt](requirements.txt)):

- **openai**: OpenAI API integration for language models
- **langchain**: Framework for building LLM applications
- **chromadb**: Vector database for document storage and retrieval
- **tiktoken**: Token counting and management
- **unstructured**: Document parsing and preprocessing
- **faiss-cpu**: Efficient similarity search and clustering

## Usage

1. Ensure your virtual environment is activated
2. Set up your OpenAI API key as an environment variable:
```bash
export OPENAI_API_KEY="your-api-key-here"
```

3. Run the RAG pipeline:
```bash
python main.py  # (when implemented)
```

## Project Structure

```
RAG-Project/
├── README.md           # This file
├── requirements.txt    # Python dependencies
├── .gitignore         # Git ignore rules
└── rag-env/           # Virtual environment (excluded from git)
```

## Contributing

This is a coursework project for CS 6365 Real-Time Systems. Please follow academic integrity guidelines when contributing.

## License

Educational use only - CS 6365 coursework project.