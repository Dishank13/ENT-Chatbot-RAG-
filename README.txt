# Instructions for running the beginner-friendly RAG ENT chatbot

1. Install dependencies:
   Open a terminal in this folder and run:
   pip install -r requirements.txt

2. Prepare your data:
   - Place your ENT-related PDFs and CSVs in a folder named 'data' in this directory.

3. Set your OpenAI API key:
   - In your terminal, set the environment variable before running scripts:
     $env:OPENAI_API_KEY = "sk-..."   # (for PowerShell)

4. Ingest your data:
   python data_ingest.py
   - This will extract, chunk, embed, and store your data in ChromaDB.

5. Run the chatbot:
   streamlit run rag_chatbot.py
   - Open the provided local URL in your browser.

6. Ask questions!  
   - The chatbot will answer using your data and show the source chunks.

---

If you want to add more data, repeat steps 2 and 4.

For any errors, ensure all dependencies are installed and your API key is set.
