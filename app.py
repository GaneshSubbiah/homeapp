"""
Week 4 - Generator Q&A Streamlit App
=====================================
Ask questions about generator troubleshooting
"""

import streamlit as st
import os
from dotenv import load_dotenv

load_dotenv()

# Page config
st.set_page_config(
    page_title="Generator Q&A",
    page_icon="🤖",
    layout="wide"
)

# Header
st.title("🤖 Generator Troubleshooting Q&A")
st.write("Your Week 4 RAG System - Live on Streamlit Cloud!")

# Check API Key
openai_key = os.getenv("OPENAI_API_KEY")

st.divider()

# Two columns
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

# QUESTION INPUT SECTION (NEW!)
st.subheader("❓ Ask a Question")
st.write("Type your question about generator troubleshooting below:")

# Input box
question = st.text_input(
    "Your question:",
    placeholder="e.g., How to fix a generator that won't start?",
    label_visibility="collapsed"
)

# Process question
if question:
    st.info(f"🤔 Question: {question}")
    st.write("---")
    
    if not openai_key:
        st.error("⚠️ Cannot process - API key missing!")
        st.info("Please add OPENAI_API_KEY to Streamlit Cloud Secrets")
    else:
        st.success("✅ System has OpenAI API key loaded!")
        st.write("""
        **Next Steps:**
        1. Click "Next" to implement full RAG system
        2. Connect ChromaDB for PDF search
        3. Get real answers from your documents!
        """)

st.divider()

# Sample Questions
st.subheader("❓ Sample Questions")
st.write("Try asking these questions:")
st.markdown("""
- How to fix a generator that won't start?
- What causes overheating?
- How to fix low power output?
""")

st.divider()

# Footer
st.markdown("""
---
**Status:** ✅ Live on Streamlit Cloud

**Next Steps:**
1. ✅ Basic app is working
2. ⏳ Add full RAG system (Week 5)
3. ⏳ Connect to your PDFs
4. ⏳ Get answers from documents!

Made with ❤️ by Ganesh
""")
