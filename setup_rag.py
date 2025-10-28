"""Setup script for Digital Forge RAG system

Initializes Qdrant collection and indexes knowledge base documents.
"""

import os
import sys
from pathlib import Path
from typing import List
import logging

from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
import uuid

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Configuration
QDRANT_HOST = os.getenv("QDRANT_HOST", "localhost")
QDRANT_PORT = int(os.getenv("QDRANT_PORT", "6333"))
COLLECTION_NAME = "digital_forge_knowledge"
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "text-embedding-3-small")
KNOWLEDGE_BASE_DIR = Path("knowledge_base/documents")

def load_documents(directory: Path) -> List[tuple[str, dict]]:
    """Load all markdown documents from directory"""
    documents = []
    
    if not directory.exists():
        logger.warning(f"Directory {directory} does not exist")
        return documents
    
    for file_path in directory.rglob("*.md"):
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                metadata = {
                    "source": str(file_path),
                    "filename": file_path.name,
                    "type": "markdown"
                }
                documents.append((content, metadata))
                logger.info(f"✓ Loaded {file_path.name}")
        except Exception as e:
            logger.error(f"✗ Failed to load {file_path}: {e}")
    
    return documents

def chunk_documents(documents: List[tuple[str, dict]]) -> List[tuple[str, dict]]:
    """Chunk documents into smaller pieces"""
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len,
        separators=["\n\n", "\n", " ", ""]
    )
    
    chunks = []
    for content, metadata in documents:
        text_chunks = text_splitter.split_text(content)
        for i, chunk in enumerate(text_chunks):
            chunk_metadata = {
                **metadata,
                "chunk_index": i,
                "total_chunks": len(text_chunks)
            }
            chunks.append((chunk, chunk_metadata))
    
    logger.info(f"✓ Created {len(chunks)} chunks from {len(documents)} documents")
    return chunks

def setup_qdrant_collection(client: QdrantClient, vector_size: int = 1536):
    """Create or recreate Qdrant collection"""
    try:
        # Check if collection exists
        collections = client.get_collections().collections
        collection_names = [c.name for c in collections]
        
        if COLLECTION_NAME in collection_names:
            logger.info(f"Collection {COLLECTION_NAME} already exists, recreating...")
            client.delete_collection(COLLECTION_NAME)
        
        # Create collection
        client.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=VectorParams(size=vector_size, distance=Distance.COSINE)
        )
        logger.info(f"✓ Created collection {COLLECTION_NAME}")
        
    except Exception as e:
        logger.error(f"✗ Failed to setup collection: {e}")
        raise

def index_documents(client: QdrantClient, embeddings: OpenAIEmbeddings, chunks: List[tuple[str, dict]]):
    """Generate embeddings and index documents"""
    try:
        logger.info(f"Generating embeddings for {len(chunks)} chunks...")
        
        # Extract texts and metadata
        texts = [chunk[0] for chunk in chunks]
        metadatas = [chunk[1] for chunk in chunks]
        
        # Generate embeddings in batches
        batch_size = 100
        total_indexed = 0
        
        for i in range(0, len(texts), batch_size):
            batch_texts = texts[i:i+batch_size]
            batch_metadata = metadatas[i:i+batch_size]
            
            # Generate embeddings
            batch_embeddings = embeddings.embed_documents(batch_texts)
            
            # Create points
            points = [
                PointStruct(
                    id=str(uuid.uuid4()),
                    vector=embedding,
                    payload={
                        "text": text,
                        **metadata
                    }
                )
                for text, embedding, metadata in zip(batch_texts, batch_embeddings, batch_metadata)
            ]
            
            # Upload to Qdrant
            client.upsert(
                collection_name=COLLECTION_NAME,
                points=points
            )
            
            total_indexed += len(points)
            progress = (total_indexed / len(texts)) * 100
            logger.info(f"Progress: {total_indexed}/{len(texts)} ({progress:.1f}%)")
        
        logger.info(f"✓ Indexed {total_indexed} chunks successfully")
        
    except Exception as e:
        logger.error(f"✗ Failed to index documents: {e}")
        raise

def main():
    """Main setup function"""
    try:
        logger.info("=" * 60)
        logger.info("Digital Forge RAG Setup")
        logger.info("=" * 60)
        
        # Check OpenAI API key
        if not os.getenv("OPENAI_API_KEY"):
            logger.error("✗ OPENAI_API_KEY environment variable not set")
            sys.exit(1)
        
        # Connect to Qdrant
        logger.info(f"Connecting to Qdrant at {QDRANT_HOST}:{QDRANT_PORT}...")
        client = QdrantClient(host=QDRANT_HOST, port=QDRANT_PORT)
        logger.info("✓ Connected to Qdrant")
        
        # Initialize embeddings
        logger.info(f"Initializing OpenAI embeddings ({EMBEDDING_MODEL})...")
        embeddings = OpenAIEmbeddings(model=EMBEDDING_MODEL)
        logger.info("✓ Embeddings initialized")
        
        # Load documents
        logger.info(f"Loading documents from {KNOWLEDGE_BASE_DIR}...")
        documents = load_documents(KNOWLEDGE_BASE_DIR)
        
        if not documents:
            logger.warning("No documents found. Creating sample document...")
            KNOWLEDGE_BASE_DIR.mkdir(parents=True, exist_ok=True)
            sample_doc = KNOWLEDGE_BASE_DIR / "sample.md"
            sample_doc.write_text(
                "# Digital Forge Knowledge Base\n\n"
                "This is a sample document for the Digital Forge RAG system.\n\n"
                "## Features\n\n"
                "- Semantic search\n"
                "- RAG integration\n"
                "- GitHub Copilot support\n"
            )
            documents = load_documents(KNOWLEDGE_BASE_DIR)
        
        # Chunk documents
        logger.info("Chunking documents...")
        chunks = chunk_documents(documents)
        
        # Setup collection
        logger.info("Setting up Qdrant collection...")
        setup_qdrant_collection(client)
        
        # Index documents
        logger.info("Indexing documents...")
        index_documents(client, embeddings, chunks)
        
        # Verify
        collection_info = client.get_collection(COLLECTION_NAME)
        logger.info("=" * 60)
        logger.info("Setup Complete!")
        logger.info(f"Collection: {COLLECTION_NAME}")
        logger.info(f"Vectors: {collection_info.vectors_count}")
        logger.info(f"Points: {collection_info.points_count}")
        logger.info("=" * 60)
        
    except Exception as e:
        logger.error(f"Setup failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
