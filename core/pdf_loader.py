"""
PDF Loader - Week 4
===================
Load and extract text from PDF files.

WHAT: Loads all PDFs from a folder
HOW: Uses PyPDF2 to read PDFs
WHY: Convert binary PDF → readable text + metadata
WHERE: Called by setup.py during setup
"""

from pathlib import Path
from PyPDF2 import PdfReader
from langchain_core.documents import Document
import os


def load_pdfs_from_folder(pdf_folder_path="./data/pdfs/"):
    """
    Load all PDFs from a folder and extract text.
    
    Args:
        pdf_folder_path: Path to folder containing PDFs
        
    Returns:
        List of Document objects (one per page)
        
    Example:
        pdfs = load_pdfs_from_folder("./data/pdfs/")
        print(f"Loaded {len(pdfs)} pages")
    """
    
    documents = []
    pdf_path = Path(pdf_folder_path)
    
    # Create folder if doesn't exist
    pdf_path.mkdir(parents=True, exist_ok=True)
    print(f"📂 Folder: {pdf_folder_path}")
    
    # Find all PDF files
    pdf_files = list(pdf_path.glob("*.txt")) + list(pdf_path.glob("*.pdf"))
    
    # Check if PDFs found
    if not pdf_files:
        print(f"⚠️  No PDFs found in {pdf_folder_path}")
        print(f"   Add PDF files and try again")
        return documents
    
    print(f"📄 Found {len(pdf_files)} PDF files\n")
    
    # Process each PDF
    for pdf_file in pdf_files:
        print(f"  📖 Processing: {pdf_file.name}...")
        
        try:
            # Open PDF
            pdf_reader = PdfReader(pdf_file)
            total_pages = len(pdf_reader.pages)
            
            print(f"     Pages: {total_pages}")
            
            # Read each page
            for page_num, page in enumerate(pdf_reader.pages):
                # Extract text from page
                text = page.extract_text()
                
                # Only add if page has text
                # (ignore empty pages, images-only pages)
                if text.strip():
                    # Create Document with metadata
                    doc = Document(
                        page_content=text,
                        metadata={
                            "source": "pdf",
                            "pdf_name": pdf_file.name,
                            "page_number": page_num + 1,
                            "total_pages": total_pages
                        }
                    )
                    documents.append(doc)
        
        except Exception as e:
            print(f"     ❌ Error: {e}")
    
    print(f"\n✅ Loaded {len(documents)} total pages\n")
    return documents


if __name__ == "__main__":
    print("Testing pdf_loader.py...")
    print("="*60)
    
    pdfs = load_pdfs_from_folder("./data/pdfs/")
    
    if pdfs:
        print(f"✅ Successfully loaded {len(pdfs)} pages!\n")
        
        # Show first page
        print("First page preview:")
        print("-"*60)
        print(f"Source: {pdfs[0].metadata['pdf_name']}")
        print(f"Page: {pdfs[0].metadata['page_number']}")
        print(f"Content: {pdfs[0].page_content[:200]}...")
    else:
        print("⚠️  No PDFs loaded")
        print("   Add PDF files to ./data/pdfs/")
