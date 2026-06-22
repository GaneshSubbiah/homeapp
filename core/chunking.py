"""
Chunking - Week 4
=================
Split documents into chunks with metadata.

WHAT: Splits large Documents into smaller chunks
HOW: Uses RecursiveCharacterTextSplitter (smart splitting)
WHY: Optimize for embedding and search
WHERE: Called by setup.py after pdf_loader.py
"""

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from typing import List
from config import CHUNK_SIZE, CHUNK_OVERLAP


def chunk_documents(documents: List[Document]) -> List[Document]:
    """
    Split documents into chunks with metadata.
    
    Uses RecursiveCharacterTextSplitter for smart splitting:
    - Tries to split by paragraphs first
    - Then sentences
    - Then words
    - Finally characters as last resort
    
    Args:
        documents: List of Document objects (from pdf_loader)
        
    Returns:
        List of chunked Document objects
        
    Example:
        pdf_docs = load_pdfs_from_folder()
        chunks = chunk_documents(pdf_docs)
        print(f"Created {len(chunks)} chunks")
    """
    
    print(f"✂️  Chunking {len(documents)} documents...")
    print(f"   Chunk size: {CHUNK_SIZE} characters")
    print(f"   Chunk overlap: {CHUNK_OVERLAP} characters\n")
    
    # Create splitter (smart splitting!)
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,              # 1000 characters per chunk
        chunk_overlap=CHUNK_OVERLAP,         # 200 character overlap
        separators=[
            "\n\n",     # Split by paragraph first
            "\n",       # Then by line break
            ". ",       # Then by sentence
            " ",        # Then by word
            ""          # Finally by character
        ],
        length_function=len,  # Use character count
    )
    
    all_chunks = []
    
    # Process each document
    for doc_idx, doc in enumerate(documents):
        # Get text to split
        text = doc.page_content
        
        # Split into chunks
        text_chunks = splitter.split_text(text)
        
        print(f"  📄 Document {doc_idx + 1}: {len(text_chunks)} chunks")
        
        # Create Document object for each chunk
        for chunk_idx, chunk_text in enumerate(text_chunks):
            # Copy original metadata
            chunk_metadata = doc.metadata.copy()
            
            # Add chunking metadata
            chunk_metadata["chunk_index"] = chunk_idx
            chunk_metadata["chunk_count"] = len(text_chunks)
            chunk_metadata["chunk_size"] = len(chunk_text)
            
            # Create chunk Document
            chunk_doc = Document(
                page_content=chunk_text,
                metadata=chunk_metadata
            )
            all_chunks.append(chunk_doc)
    
    print(f"\n✅ Created {len(all_chunks)} total chunks\n")
    return all_chunks


def chunk_pdf_documents(pdfs: List[Document]) -> List[Document]:
    """
    Chunk PDF documents specifically.
    
    Same as chunk_documents() but for PDFs.
    Useful if you have different settings for PDFs vs cases.
    """
    return chunk_documents(pdfs)


def chunk_salesforce_cases(cases: List[Document]) -> List[Document]:
    """
    Chunk Salesforce cases specifically.
    
    Same as chunk_documents() but for cases.
    Useful if you have different settings for cases vs PDFs.
    """
    return chunk_documents(cases)


if __name__ == "__main__":
    """Test chunking with sample document"""
    print("Testing chunking.py...")
    print("="*60)
    
    # Create sample document
    test_doc = Document(
        page_content="""Generator Troubleshooting Guide

Problem: Generator Won't Start
Description: Customer reported generator fails to restart after 
power outage. System won't turn on after electrical reset.

Cause: Electrical System Fault
Analysis: Control panel detected fault condition after power 
interruption. Requires manual reset.

Solution: Perform Control Panel Reset
Steps:
1. Turn off generator
2. Wait 30 seconds for capacitors to discharge
3. Turn on generator
4. Verify operation with test load

Result: Generator restarted successfully. Issue resolved.""",
        metadata={
            "source": "pdf",
            "pdf_name": "test_guide.pdf",
            "page_number": 1,
            "total_pages": 50
        }
    )
    
    # Chunk it
    chunks = chunk_documents([test_doc])
    
    # Show results
    print(f"✅ Test complete!")
    print(f"   Total chunks: {len(chunks)}\n")
    
    # Show each chunk
    for i, chunk in enumerate(chunks):
        print(f"CHUNK {i+1}:")
        print(f"  Metadata:")
        print(f"    - Source: {chunk.metadata['source']}")
        print(f"    - PDF: {chunk.metadata['pdf_name']}")
        print(f"    - Chunk {chunk.metadata['chunk_index']+1} of {chunk.metadata['chunk_count']}")
        print(f"    - Size: {chunk.metadata['chunk_size']} chars")
        print(f"  Content: {chunk.page_content[:80]}...")
        print()
