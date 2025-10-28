# Setup Verification Script

import sys
import os
from typing import List, Tuple

def check_environment_variables() -> Tuple[bool, List[str]]:
    """Check required environment variables"""
    required_vars = [
        "OPENAI_API_KEY",
    ]
    
    optional_vars = [
        "QDRANT_HOST",
        "QDRANT_PORT",
        "EMBEDDING_MODEL",
    ]
    
    issues = []
    
    for var in required_vars:
        if not os.getenv(var):
            issues.append(f"❌ Required: {var} not set")
    
    for var in optional_vars:
        if not os.getenv(var):
            issues.append(f"⚠️  Optional: {var} not set (using default)")
    
    return len([i for i in issues if i.startswith("❌")]) == 0, issues

def check_dependencies() -> Tuple[bool, List[str]]:
    """Check if required packages are installed"""
    required_packages = [
        "fastapi",
        "fastapi_mcp",
        "uvicorn",
        "langchain",
        "langchain_openai",
        "qdrant_client",
        "pydantic",
    ]
    
    issues = []
    
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            issues.append(f"❌ Package not installed: {package}")
    
    return len(issues) == 0, issues

def check_qdrant_connection() -> Tuple[bool, List[str]]:
    """Check Qdrant connection"""
    issues = []
    
    try:
        from qdrant_client import QdrantClient
        
        host = os.getenv("QDRANT_HOST", "localhost")
        port = int(os.getenv("QDRANT_PORT", "6333"))
        
        client = QdrantClient(host=host, port=port, timeout=5)
        collections = client.get_collections()
        issues.append(f"✅ Qdrant connected: {len(collections.collections)} collections")
        return True, issues
        
    except Exception as e:
        issues.append(f"❌ Qdrant connection failed: {str(e)}")
        return False, issues

def check_openai_api() -> Tuple[bool, List[str]]:
    """Check OpenAI API key"""
    issues = []
    
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        issues.append("❌ OPENAI_API_KEY not set")
        return False, issues
    
    try:
        from langchain_openai import OpenAIEmbeddings
        
        embeddings = OpenAIEmbeddings(
            model="text-embedding-3-small",
            openai_api_key=api_key
        )
        
        # Test with a simple embedding
        test_embedding = embeddings.embed_query("test")
        
        if len(test_embedding) == 1536:
            issues.append("✅ OpenAI API key valid")
            return True, issues
        else:
            issues.append(f"❌ Unexpected embedding size: {len(test_embedding)}")
            return False, issues
            
    except Exception as e:
        issues.append(f"❌ OpenAI API test failed: {str(e)}")
        return False, issues

def check_knowledge_base() -> Tuple[bool, List[str]]:
    """Check knowledge base structure"""
    issues = []
    
    kb_dir = "knowledge_base/documents"
    
    if not os.path.exists(kb_dir):
        issues.append(f"⚠️  Knowledge base directory not found: {kb_dir}")
        return False, issues
    
    # Count markdown files
    md_files = []
    for root, dirs, files in os.walk(kb_dir):
        for file in files:
            if file.endswith(".md"):
                md_files.append(os.path.join(root, file))
    
    if len(md_files) == 0:
        issues.append("⚠️  No markdown files found in knowledge base")
        return False, issues
    
    issues.append(f"✅ Knowledge base: {len(md_files)} documents found")
    return True, issues

def main():
    """Run all verification checks"""
    print("="*60)
    print("Digital Forge MCP RAG - Setup Verification")
    print("="*60)
    print()
    
    all_passed = True
    
    # Check environment variables
    print("[1/5] Checking environment variables...")
    passed, issues = check_environment_variables()
    for issue in issues:
        print(f"  {issue}")
    all_passed = all_passed and passed
    print()
    
    # Check dependencies
    print("[2/5] Checking dependencies...")
    passed, issues = check_dependencies()
    if passed:
        print("  ✅ All dependencies installed")
    else:
        for issue in issues:
            print(f"  {issue}")
    all_passed = all_passed and passed
    print()
    
    # Check Qdrant
    print("[3/5] Checking Qdrant connection...")
    passed, issues = check_qdrant_connection()
    for issue in issues:
        print(f"  {issue}")
    all_passed = all_passed and passed
    print()
    
    # Check OpenAI API
    print("[4/5] Checking OpenAI API...")
    passed, issues = check_openai_api()
    for issue in issues:
        print(f"  {issue}")
    all_passed = all_passed and passed
    print()
    
    # Check knowledge base
    print("[5/5] Checking knowledge base...")
    passed, issues = check_knowledge_base()
    for issue in issues:
        print(f"  {issue}")
    all_passed = all_passed and passed
    print()
    
    # Summary
    print("="*60)
    if all_passed:
        print("✅ All checks passed! System is ready.")
        print()
        print("Next steps:")
        print("  1. Run: python setup_rag.py")
        print("  2. Start server: uvicorn rag_mcp_server:app --reload")
        print("  3. Access docs: http://localhost:8000/docs")
        sys.exit(0)
    else:
        print("❌ Some checks failed. Please fix the issues above.")
        print()
        print("Common fixes:")
        print("  - Set OPENAI_API_KEY: export OPENAI_API_KEY='your-key'")
        print("  - Start Qdrant: docker-compose up -d")
        print("  - Install deps: pip install -r requirements.txt")
        sys.exit(1)
    print("="*60)

if __name__ == "__main__":
    main()
