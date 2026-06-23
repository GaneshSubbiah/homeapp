"""
Week 4 - Generator Q&A System
==============================
Streamlit Cloud compatible version
"""

import streamlit as st
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

st.set_page_config(page_title="Generator Q&A", page_icon="🤖", layout="wide")

st.title("🤖 Generator Troubleshooting Q&A")
st.write("Week 4 RAG System - Live on Streamlit Cloud!")

openai_key = os.getenv("OPENAI_API_KEY")

st.divider()

col1, col2 = st.columns(2)

with col1:
    st.subheader("📋 System Status")
    if openai_key:
        st.success("✅ OpenAI API Key loaded!")
    else:
        st.error("❌ Missing OPENAI_API_KEY")
        st.info("Add it in Streamlit Cloud Secrets")

with col2:
    st.subheader("📚 About")
    st.write("""
    **Built with:**
    - LangChain
    - OpenAI GPT-4o-mini
    - Streamlit
    """)

st.divider()

st.subheader("❓ Ask a Question")
st.write("Type your question about generator troubleshooting:")

question = st.text_input(
    "Your question:",
    placeholder="e.g., How to fix a generator that won't start?",
    label_visibility="collapsed"
)

if question:
    st.info(f"🤔 Question: {question}")
    st.write("---")
    
    if not openai_key:
        st.error("⚠️ Cannot process - API key missing!")
        st.info("Please add OPENAI_API_KEY to Streamlit Cloud Secrets")
    else:
        try:
            with st.spinner("🔍 Generating answer..."):
                llm = ChatOpenAI(
                    model="gpt-4o-mini",
                    api_key=openai_key,
                    temperature=0.7
                )
                
                prompt = ChatPromptTemplate.from_template("""
You are an expert in generator maintenance and troubleshooting.

Answer this question about generators with practical, actionable advice:

Question: {question}

Provide clear, helpful guidance.
Answer:""")
                
                chain = prompt | llm | StrOutputParser()
                answer = chain.invoke({"question": question})
            
            st.success("✅ Answer generated!")
            st.write("---")
            st.subheader("💬 Answer:")
            st.write(answer)
        
        except Exception as e:
            st.error(f"Error: {str(e)}")

st.divider()

st.subheader("❓ Sample Questions")
st.markdown("""
- How to fix a generator that won't start?
- What causes generator overheating?
- How to fix low power output?
- What maintenance is needed for generators?
""")

st.divider()

st.markdown("""
---
**Status:** ✅ Live on Streamlit Cloud

**Features:**
- AI-powered Q&A
- Real-time answers
- Generator expertise

Made with ❤️ by Ganesh Subbiah
""")
