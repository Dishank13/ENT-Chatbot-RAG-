import streamlit as st
from langchain_community.embeddings import FastEmbedEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_community.llms import Ollama
from langchain.chains import RetrievalQA

# --- CONFIG ---
CHROMA_DIR = "chroma_db"  # Must match your ingestion script
EMBED_MODEL = "BAAI/bge-small-en-v1.5"
OLLAMA_MODEL = "llama2"  # You can change to 'mistral', 'phi', etc. if you prefer

# --- LOAD VECTOR DB & EMBEDDINGS ---
@st.cache_resource
def load_vectordb():
    embeddings = FastEmbedEmbeddings(model_name=EMBED_MODEL)
    vectordb = Chroma(persist_directory=CHROMA_DIR, embedding_function=embeddings)
    return vectordb

vectordb = load_vectordb()

# --- LLM (Ollama local) ---
llm = Ollama(model=OLLAMA_MODEL, temperature=0.1)

# --- RAG CHAIN ---
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=vectordb.as_retriever(),
    return_source_documents=True,
)

# --- STREAMLIT UI ---
st.title("ENT_RAG Chatbot")
query = st.text_area("Ask a question about ENT:")

if st.button("Get Answer") and query.strip():
    with st.spinner("Thinking..."):
        result = qa_chain({"query": query})
        st.markdown("### Answer:")
        st.write(result["result"])
        st.markdown("---")
        st.markdown("**Top Sources:**")
        for doc in result["source_documents"]:
            st.write(f"- {doc.metadata['source']} (chunk {doc.metadata['chunk']})")


