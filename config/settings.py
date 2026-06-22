"""
Week 4 Configuration
====================
Minimal settings for clean learning

WHY THIS FILE?
- Single source of truth
- Easy to change values
- API keys from .env (safe)
- Used by all modules
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# ============================================
# API KEYS (from .env file)
# ============================================
# These come from your .env file (secrets!)
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
ANTHROPIC_API_KEY = os.getenv('ANTHROPIC_API_KEY')
PINECONE_API_KEY = os.getenv('PINECONE_API_KEY')

# ============================================
# MODEL SETTINGS
# ============================================
# Which AI models to use
EMBEDDING_MODEL = "text-embedding-3-small"  # OpenAI embeddings
LLM_MODEL = "claude-sonnet-4-20250514"       # Claude LLM

# ============================================
# PINECONE SETTINGS
# ============================================
# Cloud vector database configuration
PINECONE_INDEX_NAME = os.getenv('PINECONE_INDEX_NAME', 'salesforce-cases-w4')
PINECONE_DIMENSION = 1536  # OpenAI embeddings create 1536-dimensional vectors

# ============================================
# CHUNKING SETTINGS
# ============================================
# How to split documents into chunks
CHUNK_SIZE = 1000           # 1000 characters per chunk
CHUNK_OVERLAP = 200         # 200 character overlap between chunks

# ============================================
# RAG SETTINGS
# ============================================
# Retrieval settings
TOP_K_RESULTS = 3           # Return top 3 most similar chunks
SIMILARITY_THRESHOLD = 0.7  # Minimum similarity score (0-1)

# ============================================
# PATHS
# ============================================
# Where files are stored
DATA_DIR = "./data"
PDF_DIR = "./data/pdfs"
CASES_FILE = "./data/cases.json"

# ============================================
# CONFIRMATION
# ============================================
print("✅ Settings loaded successfully!")
