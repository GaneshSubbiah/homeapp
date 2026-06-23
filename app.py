"""
Week 4 - Streamlit Web App
===========================
Web interface for RAG system
"""

import streamlit as st
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

from core.vector_store import load_vectorstore
from config import OPENAI_API_KEY
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv

load_dotenv()


def format_docs(docs):
    """Format retrieved documents"""
    return "\n\n---\n\n".join(
        f"Source: {doc.metadata.get('pdf_name', 'Unknown')}\n"
        f"Page: {doc.metadata.get('page_number', 'N/A')}\n"
        f"Content: {doc.page_content}"
        for doc in docs
    )


def ask_question(question):
    """Ask a question against PDFs"""
    
    vectorstore = load_vectorstore()
    retriever = vectorstore.as_retriever(search_kwargs={"k": 3})
    
    llm = ChatOpenAI(
        model="gpt-4o-mini",
        api_key=OPENAI_API_KEY
    )
    
    prompt = ChatPromptTemplate.from_template("""
You are a helpful assistant. Answer the question based on the provided documents.

Documents:
{context}

Question: {question}

Answer:""")
    
    chain = (
        {
            "context": retriever | format_docs,
            "question": RunnablePassthrough()
        }
        | prompt
        | llm
        | StrOutputParser()
    )
    
    return chain.invoke(question)


# Streamlit UI
st.set_page_config(page_title="Generator Q&A", layout="wide")

st.title("🤖 Generator Troubleshooting Q&A")
st.write("Ask questions about generator maintenance and troubleshooting")

# Input
question = st.text_input("❓ Ask a question:", placeholder="e.g., How to fix a generator that won't start?")

# Answer
if question:
    with st.spinner("🤔 Thinking..."):
        try:
            answer = ask_question(question)
            st.success("✅ Answer:")
            st.write(answer)
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")

st.divider()
st.markdown("**Built with:** LangChain | OpenAI | ChromaDB | Streamlit")
