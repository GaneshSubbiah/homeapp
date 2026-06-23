#!/bin/bash

echo "╔════════════════════════════════════════════════════════════╗"
echo "║     WEEK 4 RAG SYSTEM - COMPLETE VERIFICATION             ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

PASS=0
FAIL=0

# Function to check file
check_file() {
    if [ -f "$1" ]; then
        echo -e "${GREEN}✅${NC} $1"
        ((PASS++))
    else
        echo -e "${RED}❌${NC} $1"
        ((FAIL++))
    fi
}

# Function to check directory
check_dir() {
    if [ -d "$1" ]; then
        echo -e "${GREEN}✅${NC} $1/"
        ((PASS++))
    else
        echo -e "${RED}❌${NC} $1/"
        ((FAIL++))
    fi
}

echo "1️⃣ CHECKING DIRECTORY STRUCTURE"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
check_dir "config"
check_dir "core"
check_dir "data"
check_dir "data/pdfs"
check_dir "data/chroma_db"
echo ""

echo "2️⃣ CHECKING CONFIG FILES"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
check_file "config/__init__.py"
check_file "config/settings.py"
echo ""

echo "3️⃣ CHECKING CORE MODULES"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
check_file "core/__init__.py"
check_file "core/pdf_loader.py"
check_file "core/chunking.py"
check_file "core/vector_store.py"
echo ""

echo "4️⃣ CHECKING MAIN APPLICATION FILES"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
check_file "app.py"
check_file "main.py"
check_file "setup.py"
echo ""

echo "5️⃣ CHECKING DEPLOYMENT FILES"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
check_file "requirements.txt"
check_file "Procfile"
check_file ".env"
check_file ".gitignore"
echo ""

echo "6️⃣ CHECKING DATA FILES"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
PDF_COUNT=$(find data/pdfs -name "*.pdf" 2>/dev/null | wc -l)
echo "📄 PDFs found: $PDF_COUNT"
if [ $PDF_COUNT -gt 0 ]; then
    echo -e "${GREEN}✅${NC} PDFs present"
    ((PASS++))
else
    echo -e "${RED}❌${NC} No PDFs found"
    ((FAIL++))
fi
echo ""

echo "7️⃣ CHECKING FILE COUNTS"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
PY_FILES=$(find . -name "*.py" -type f | wc -l)
echo "Python files: $PY_FILES"
echo ""

echo "8️⃣ CHECKING IMPORTS & SYNTAX"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Test imports
python3 << 'PYTHON_CHECK'
try:
    from config import OPENAI_API_KEY
    print("✅ config imports work")
except Exception as e:
    print(f"❌ config import error: {e}")

try:
    from core.pdf_loader import load_pdfs_from_folder
    print("✅ pdf_loader imports work")
except Exception as e:
    print(f"❌ pdf_loader import error: {e}")

try:
    from core.chunking import chunk_documents
    print("✅ chunking imports work")
except Exception as e:
    print(f"❌ chunking import error: {e}")

try:
    from core.vector_store import load_vectorstore, upload_chunks
    print("✅ vector_store imports work")
except Exception as e:
    print(f"❌ vector_store import error: {e}")

print("✅ All imports successful!")
PYTHON_CHECK
echo ""

echo "9️⃣ CHECKING .env FILE"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
if grep -q "OPENAI_API_KEY" .env 2>/dev/null; then
    echo -e "${GREEN}✅${NC} OPENAI_API_KEY found in .env"
    ((PASS++))
else
    echo -e "${RED}❌${NC} OPENAI_API_KEY missing in .env"
    ((FAIL++))
fi
echo ""

echo "🔟 CHECKING REQUIREMENTS.TXT"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
REQ_COUNT=$(wc -l < requirements.txt)
echo "Dependencies: $REQ_COUNT packages"
for pkg in streamlit langchain chromadb openai; do
    if grep -q "$pkg" requirements.txt; then
        echo -e "${GREEN}✅${NC} $pkg found"
        ((PASS++))
    else
        echo -e "${RED}❌${NC} $pkg missing"
        ((FAIL++))
    fi
done
echo ""

echo "1️⃣1️⃣ CHECKING GIT STATUS"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
if git status > /dev/null 2>&1; then
    echo -e "${GREEN}✅${NC} Git repository initialized"
    ((PASS++))
    
    COMMITS=$(git log --oneline 2>/dev/null | wc -l)
    echo "📊 Commits: $COMMITS"
    
    if git remote get-url origin > /dev/null 2>&1; then
        REMOTE=$(git remote get-url origin)
        echo -e "${GREEN}✅${NC} Remote: $(echo $REMOTE | rev | cut -d'/' -f1 | rev)"
        ((PASS++))
    fi
else
    echo -e "${RED}❌${NC} Git not initialized"
    ((FAIL++))
fi
echo ""

echo "1️⃣2️⃣ CHECKING CHROMADB DATA"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
if [ -d "data/chroma_db" ] && [ "$(ls -A data/chroma_db)" ]; then
    echo -e "${GREEN}✅${NC} ChromaDB database exists"
    CHROMA_SIZE=$(du -sh data/chroma_db | cut -f1)
    echo "📊 Size: $CHROMA_SIZE"
    ((PASS++))
else
    echo -e "${YELLOW}⚠️${NC} ChromaDB database empty or missing (run setup.py first)"
fi
echo ""

echo "╔════════════════════════════════════════════════════════════╗"
echo "║                    VERIFICATION SUMMARY                   ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""
echo -e "${GREEN}✅ PASSED: $PASS${NC}"
echo -e "${RED}❌ FAILED: $FAIL${NC}"
echo ""

if [ $FAIL -eq 0 ]; then
    echo -e "${GREEN}╔════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${GREEN}║        ✅ ALL CHECKS PASSED - READY TO DEPLOY!          ║${NC}"
    echo -e "${GREEN}╚════════════════════════════════════════════════════════════╝${NC}"
    exit 0
else
    echo -e "${RED}╔════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${RED}║    ❌ SOME CHECKS FAILED - FIX ISSUES BEFORE DEPLOY       ║${NC}"
    echo -e "${RED}╚════════════════════════════════════════════════════════════╝${NC}"
    exit 1
fi
