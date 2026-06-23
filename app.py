"""
Week 4 - Full RAG System
========================
PDF Q&A with real answering
"""

import streamlit as st
import os
from dotenv import load_dotenv

# RAG imports
from core.vector_store import load_vectorstore
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

# ============================================
# PAGE CONFIG
# ============================================

st.set_page_config(
    page_title="Generator Q&A",
    page_icon="🤖",
    layout="wide"
)

# ============================================
# HEADER
# ============================================

st.title("🤖 Generator Troubleshooting Q&A")
st.write("Your Week 4 RAG System - Live on Streamlit Cloud!")

# ============================================
# CHECK API KEY
# ============================================

openai_key = os.getenv("OPENAI_API_KEY")

st.divider()

col1, col2 = st.columns(2)

with col1:
    st.subheader("📋 System Status")
    if openai_key:
        st.success("✅ OpenAI API Key loaded!")
    else:
        st.error("❌ Missing OPENAI_API_KEY")
        st.info("Add it in Streamlit Cloud settings")

with col2:
    st.subheader("📚 About")
    st.write("""
    **Built with:**
    - LangChain
    - OpenAI GPT-4o-mini
    - ChromaDB
    - Streamlit
    """)

st.divider()

# ============================================
# QUESTION INPUT & PROCESSING (NEW!)
# ============================================

st.subheader("❓ Ask a Question")
st.write("Type your question about generator troubleshooting below:")

# Input box
question = st.text_input(
    "Your question:",
    placeholder="e.g., How to fix a generator that won't start?",
    label_visibility="collapsed"
)

# ============================================
# RAG FUNCTION (NEW!)
# ============================================

def format_docs(docs):
    """Format retrieved documents for LLM"""
    return "\n\n---\n\n".join(
        f"Source: {doc.metadata.get('pdf_name', 'Unknown')}\n"
        f"Page: {doc.metadata.get('page_number', 'N/A')}\n"
        f"Content: {doc.page_content}"
        for doc in docs
    )

def get_rag_answer(user_question):
    """
    Get answer using RAG pipeline
    
    Steps:
    1. Load ChromaDB
    2. Search for similar documents
    3. Send to OpenAI with context
    4. Get answer
    """
    
    try:
        # Step 1: Load vector store
        vectorstore = load_vectorstore()
        retriever = vectorstore.as_retriever(search_kwargs={"k": 3})
        
        # Step 2: Setup LLM
        llm = ChatOpenAI(
            model="gpt-4o-mini",
            api_key=openai_key
        )
        
        # Step 3: Create prompt
        prompt = ChatPromptTemplate.from_template("""
You are a helpful assistant for generator troubleshooting. 
Answer the question based ONLY on the provided documents.
If the answer is not in the documents, say "I don't have this information in the documents."

Documents:
{context}

Question: {question}

Answer:""")
        
        # Step 4: Build RAG chain
        chain = (
            {
                "context": retriever | format_docs,
                "question": RunnablePassthrough()
            }
            | prompt
            | llm
            | StrOutputParser()
        )
        
        # Step 5: Get answer
        answer = chain.invoke(user_question)
        return answer
        
    except Exception as e:
        return f"Error: {str(e)}"

# ============================================
# PROCESS QUESTION (UPDATED!)
# ============================================

if question:
    st.info(f"🤔 Question: {question}")
    st.write("---")
    
    if not openai_key:
        st.error("⚠️ Cannot process - API key missing!")
        st.info("Please add OPENAI_API_KEY to Streamlit Cloud Secrets")
    else:
        # Show spinner while processing
        with st.spinner("🔍 Searching documents and generating answer..."):
            answer = get_rag_answer(question)
        
        # Display answer
        st.success("✅ Answer generated!")
        st.write("---")
        st.subheader("💬 Answer:")
        st.write(answer)

st.divider()

# ============================================
# SAMPLE QUESTIONS
# ============================================

st.subheader("❓ Sample Questions")
st.write("Try asking these questions:")
st.markdown("""
- How to fix a generator that won't start?
- What causes overheating?
- How to fix low power output?
""")

st.divider()

# ============================================
# FOOTER
# ============================================

st.markdown("""
---
**Status:** ✅ Live on Streamlit Cloud with Full RAG!

**How it works:**
1. You type a question
2. System searches ChromaDB for relevant documents
3. OpenAI reads the documents
4. You get an answer based on your PDFs!

**Architecture:**
Question → ChromaDB Search → OpenAI → Answer

Made with ❤️ by Ganesh
""")
