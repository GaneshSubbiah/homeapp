"""
Week 4 Setup
============
Load PDFs → Chunk → Embed → Upload to ChromaDB

Run once to setup entire system!
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from core.pdf_loader import load_pdfs_from_folder
from core.chunking import chunk_documents
from core.vector_store import load_vectorstore, upload_chunks


def setup_week4():
    """Complete setup in one function"""
    
    print("\n" + "="*60)
    print("WEEK 4 SETUP - MULTI-SOURCE RAG")
    print("="*60 + "\n")
    
    # STEP 1: Load PDFs
    print("STEP 1: Load PDF Documents")
    print("-"*60)
    pdfs = load_pdfs_from_folder("./data/pdfs/")
    
    if not pdfs:
        print("⚠️  No PDFs found. Add PDFs to ./data/pdfs/\n")
        return
    
    # STEP 2: Chunk documents
    print("STEP 2: Chunk Documents")
    print("-"*60)
    chunks = chunk_documents(pdfs)
    
    # STEP 3: Load vectorstore
    print("STEP 3: Load ChromaDB Vector Store")
    print("-"*60)
    vectorstore = load_vectorstore()
    
    # STEP 4: Upload to ChromaDB
    print("STEP 4: Upload to ChromaDB")
    print("-"*60)
    upload_chunks(chunks, vectorstore)
    
    # STEP 5: Summary
    print("STEP 5: Summary")
    print("-"*60)
    print(f"✅ Setup complete!")
    print(f"   • PDF pages loaded: {len(pdfs)}")
    print(f"   • Chunks created: {len(chunks)}")
    print(f"   • All uploaded to ChromaDB!")
    print(f"\n✨ Ready to use! Run: python main.py\n")


if __name__ == "__main__":
    setup_week4()