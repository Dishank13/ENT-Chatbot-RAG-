# ENT Disorder Chatbot using RAG

Offline RAG chatbot for ENT using FastEmbed (BGE-small), ChromaDB, and a local LLM via Ollama. Streamlit UI with cited sources.

## Stack
- Embeddings: FastEmbed `BAAI/bge-small-en-v1.5`
- Vector store: ChromaDB (`chroma_db/`)
- LLM: Ollama (default `llama2`)
- UI: Streamlit
- Orchestration: LangChain RetrievalQA (stuff)

## Setup
1. Install Python 3.11 and [Ollama](https://ollama.com/).
2. Install Python deps:
   - `pip install -r requirements.txt`
3. Pull an LLM:
   - `ollama pull llama2`

## Ingest data
Place PDFs/CSVs into `data/`.
Then run:
```
python data_ingest.py
```
This creates/updates `chroma_db/`.

## Run the app
```
streamlit run rag_chatbot.py
```
Open http://localhost:8501

## Config (defaults)
- chunk_size=500, chunk_overlap=50
- retriever top-k=4
- temperature=0.1, max_new_tokens≈512

## Notes
- `.gitignore` excludes `data/` and `chroma_db/`.
- To version data, commit small synthetic samples only.

## Paper
LaTeX draft at `paper/ent_rag_ieee.tex`.

---

Repo: ENT-Chatbot-RAG-
