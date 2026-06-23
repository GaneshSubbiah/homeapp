"""
Week 4 - Generator Q&A Demo
============================
Simple Streamlit app
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

# Demo Questions
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
1. Add OPENAI_API_KEY to Streamlit Secrets
2. Deploy full RAG system
3. Share with friends!

Made with ❤️ by Ganesh
""")
