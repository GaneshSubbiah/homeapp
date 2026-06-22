"""
Week 4 Main - Ask Questions
============================
User interface for RAG system.
Using OpenAI's gpt-4o-mini (cheaper!)

Usage:
  python main.py
  Type questions, system answers!
"""

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
    """Format retrieved documents for OpenAI"""
    return "\n\n---\n\n".join(
        f"Source: {doc.metadata.get('pdf_name', 'Unknown')}\n"
        f"Page: {doc.metadata.get('page_number', 'N/A')}\n"
        f"Content: {doc.page_content}"
        for doc in docs
    )


def ask_question(question):
    """Ask a question against PDFs"""
    
    # Load vectorstore
    vectorstore = load_vectorstore()
    retriever = vectorstore.as_retriever(search_kwargs={"k": 3})
    
    # Setup OpenAI (gpt-4o-mini - cheap!)
    llm = ChatOpenAI(
        model="gpt-4o-mini",
        api_key=OPENAI_API_KEY
    )
    
    # Create prompt
    prompt = ChatPromptTemplate.from_template("""
You are a helpful assistant. Answer the question based on the provided documents.

Documents:
{context}

Question: {question}

Answer:""")
    
    # Build chain
    chain = (
        {
            "context": retriever | format_docs,
            "question": RunnablePassthrough()
        }
        | prompt
        | llm
        | StrOutputParser()
    )
    
    # Get answer
    answer = chain.invoke(question)
    return answer


def main():
    """Main loop"""
    
    print("\n" + "="*60)
    print("WEEK 4 - PDF Q&A SYSTEM (OpenAI gpt-4o-mini)")
    print("="*60)
    print("\nAsk questions about your documents!")
    print("Type 'quit' to exit\n")
    
    while True:
        question = input("❓ Question: ").strip()
        
        if question.lower() == 'quit':
            print("\n👋 Goodbye!\n")
            break
        
        if not question:
            continue
        
        try:
            print("\n🤔 Thinking...\n")
            answer = ask_question(question)
            print(f"💬 Answer:\n{answer}\n")
        
        except Exception as e:
            print(f"❌ Error: {e}\n")


if __name__ == "__main__":
    main()