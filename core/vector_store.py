"""
Vector Store - Week 4
=====================
Using ChromaDB (local, no compilation issues!)

WHAT: Manages vector storage
HOW: Uses LangChain Chroma
WHY: Store and search embeddings locally
WHERE: Called by setup.py and main.py
"""

from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from typing import List
from langchain_core.documents import Document
import os
from dotenv import load_dotenv
from config import (
    OPENAI_API_KEY,
    EMBEDDING_MODEL,
)

load_dotenv()


def create_embeddings():
    """Create OpenAI embeddings object"""
    
    print(f"🔗 Creating embeddings object...")
    
    embeddings = OpenAIEmbeddings(
        model=EMBEDDING_MODEL,
        openai_api_key=OPENAI_API_KEY
    )
    
    print(f"   ✅ Embeddings ready ({EMBEDDING_MODEL})\n")
    return embeddings


def load_vectorstore():
    """Load ChromaDB vector store"""
    
    print(f"🔗 Loading ChromaDB vector store...")
    
    embeddings = create_embeddings()
    
    vectorstore = Chroma(
        collection_name="salesforce_cases",
        embedding_function=embeddings,
        persist_directory="./data/chroma_db"
    )
    
    print(f"   ✅ Connected to ChromaDB\n")
    return vectorstore


def upload_chunks(chunks: List[Document], vectorstore=None):
    """Upload chunks to ChromaDB"""
    
    if vectorstore is None:
        vectorstore = load_vectorstore()
    
    print(f"⬆️  Uploading {len(chunks)} chunks to ChromaDB...")
    
    try:
        vectorstore.add_documents(chunks)
        print(f"   ✅ Upload successful!\n")
    
    except Exception as e:
        print(f"   ❌ Error uploading: {e}\n")
        raise