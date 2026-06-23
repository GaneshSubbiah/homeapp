import streamlit as st
import os
from dotenv import load_dotenv

load_dotenv()

st.title("🤖 Generator Q&A - Full RAG")

openai_key = os.getenv("OPENAI_API_KEY")

st.divider()

col1, col2 = st.columns(2)

with col1:
    st.subheader("📋 System Status")
    if openai_key:
        st.success("✅ OpenAI API Key loaded!")
    else:
        st.error("❌ Missing OPENAI_API_KEY")

with col2:
    st.subheader("📚 About")
    st.write("RAG System with ChromaDB + OpenAI")

st.divider()

st.subheader("❓ Ask a Question")
question = st.text_input(
    "Your question:",
    placeholder="Ask about the PDF content...",
    label_visibility="collapsed"
)

if question:
    st.info(f"🤔 Question: {question}")
    st.write("---")
    
    if not openai_key:
        st.error("⚠️ Missing API key!")
    else:
        try:
            with st.spinner("🔍 Searching PDF and generating answer..."):
                # FULL RAG PIPELINE
                from core.vector_store import load_vectorstore
                from langchain_openai import ChatOpenAI
                from langchain_core.prompts import ChatPromptTemplate
                from langchain_core.runnables import RunnablePassthrough
                from langchain_core.output_parsers import StrOutputParser
                
                # Load ChromaDB
                vectorstore = load_vectorstore()
                retriever = vectorstore.as_retriever(search_kwargs={"k": 3})
                
                # Format docs
                def format_docs(docs):
                    return "\n\n---\n\n".join(
                        f"Source: {doc.metadata.get('pdf_name')}\n"
                        f"Content: {doc.page_content}"
                        for doc in docs
                    )
                
                # Setup LLM
                llm = ChatOpenAI(
                    model="gpt-4o-mini",
                    api_key=openai_key
                )
                
                # RAG prompt (uses PDF content!)
                prompt = ChatPromptTemplate.from_template("""
You are a helpful assistant. Answer based ONLY on the provided documents.

Documents:
{context}

Question: {question}

If the answer is not in the documents, say: "This information is not in the provided documents."

Answer:""")
                
                # Build RAG chain
                chain = (
                    {
                        "context": retriever | format_docs,
                        "question": RunnablePassthrough()
                    }
                    | prompt
                    | llm
                    | StrOutputParser()
                )
                
                answer = chain.invoke(question)
            
            st.success("✅ Answer generated!")
            st.write("---")
            st.subheader("💬 Answer:")
            st.write(answer)
        
        except Exception as e:
            st.error(f"Error: {str(e)}")
            st.info("Make sure to run: python setup.py")

st.markdown("---\n**Source:** PDF content via vector matching")
