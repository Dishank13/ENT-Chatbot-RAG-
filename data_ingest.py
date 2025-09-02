"""
Beginner-friendly script to:
- Extract and chunk text from PDFs/CSVs
- Generate embeddings locally (FastEmbed - no torch)
- Store chunks and embeddings in ChromaDB
"""
import os
import glob

import pandas as pd
from PyPDF2 import PdfReader
from langchain_community.vectorstores import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import FastEmbedEmbeddings
import shutil

# --- CONFIG ---
DATA_DIR = "data"  # Place your PDFs/CSVs here
CHROMA_DIR = "chroma_db"  # Where vector DB will be stored
# If True, delete existing Chroma directory before ingest to avoid embedding-size mismatches
RESET_CHROMA = True

# --- HELPERS ---
def extract_text_from_pdf(pdf_path):
    reader = PdfReader(pdf_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text() + "\n"
    return text

def extract_text_from_csv(csv_path):
    df = pd.read_csv(csv_path)
    return "\n".join(df.astype(str).apply(lambda row: " ".join(row), axis=1))

def chunk_text(text, chunk_size=500, chunk_overlap=50):
    splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    return splitter.split_text(text)

# --- MAIN INGESTION ---
def ingest():
    docs = []
    metadatas = []
    for pdf in glob.glob(os.path.join(DATA_DIR, "*.pdf")):
        text = extract_text_from_pdf(pdf)
        chunks = chunk_text(text)
        for i, chunk in enumerate(chunks):
            docs.append(chunk)
            metadatas.append({"source": os.path.basename(pdf), "chunk": i})
    for csv in glob.glob(os.path.join(DATA_DIR, "*.csv")):
        text = extract_text_from_csv(csv)
        chunks = chunk_text(text)
        for i, chunk in enumerate(chunks):
            docs.append(chunk)
            metadatas.append({"source": os.path.basename(csv), "chunk": i})
    print(f"Loaded {len(docs)} chunks.")
    # Optionally reset the persisted DB to avoid dimension mismatches when changing models
    if RESET_CHROMA and os.path.exists(CHROMA_DIR):
        shutil.rmtree(CHROMA_DIR)
        print(f"Reset existing Chroma directory: {CHROMA_DIR}")

    # Embedding and storing using FastEmbed (CPU/ONNX; no torch dependency)
    embeddings = FastEmbedEmbeddings(model_name="BAAI/bge-small-en-v1.5")
    vectordb = Chroma(
        persist_directory=CHROMA_DIR,
        embedding_function=embeddings
    )
    vectordb.add_texts(texts=docs, metadatas=metadatas)
    vectordb.persist()
    print(f"Ingestion complete. ChromaDB at {CHROMA_DIR}")

if __name__ == "__main__":
    ingest()
    
