import streamlit as st
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

st.set_page_config(page_title="Generator Q&A", page_icon="🤖", layout="wide")
st.title("🤖 Generator Troubleshooting Q&A")
st.write("AI-Powered Expert Assistant for Generator Questions")

openai_key = os.getenv("OPENAI_API_KEY")

st.divider()
col1, col2 = st.columns(2)

with col1:
    st.subheader("📋 System Status")
    if openai_key:
        st.success("✅ API Key loaded!")
    else:
        st.error("❌ Missing OPENAI_API_KEY")

with col2:
    st.subheader("📚 About")
    st.write("AI Model: GPT-4o-mini\nFramework: LangChain\nHosting: Streamlit Cloud")

st.divider()
st.subheader("❓ Ask Your Question")
question = st.text_input("Your question:", placeholder="e.g., How to fix a generator?", label_visibility="collapsed")

if question:
    st.info(f"🤔 Question: {question}")
    st.write("---")
    
    if not openai_key:
        st.error("⚠️ Missing API key!")
    else:
        try:
            with st.spinner("🔍 Generating answer..."):
                llm = ChatOpenAI(model="gpt-4o-mini", api_key=openai_key, temperature=0.7, max_tokens=1000)
                prompt = ChatPromptTemplate.from_template("You are a generator expert. Answer: {question}")
                chain = prompt | llm | StrOutputParser()
                answer = chain.invoke({"question": question})
            
            st.success("✅ Answer generated!")
            st.write("---")
            st.subheader("💬 Answer:")
            st.markdown(answer)
        except Exception as e:
            st.error(f"Error: {str(e)}")

st.divider()
st.subheader("❓ Sample Questions")
st.markdown("- How to fix a generator that won't start?\n- What causes overheating?\n- How to fix low power?")
st.markdown("---\n✅ Live on Streamlit Cloud | Built by Ganesh Subbiah")
