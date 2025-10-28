"""Test MCP compliance for Digital Forge RAG Server"""

import pytest
import httpx
from typing import Dict, Any

BASE_URL = "http://localhost:8000"

@pytest.fixture
def client():
    return httpx.Client(base_url=BASE_URL)

def test_health_check(client):
    """Test health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert "services" in data
    assert data["mcp_compliance"] == "A0-A6"

def test_search_knowledge_mcp_compliance(client):
    """Test search_knowledge MCP tool compliance"""
    response = client.post(
        "/api/search_knowledge",
        json={"query": "test query", "k": 5}
    )
    assert response.status_code == 200
    data = response.json()
    
    # Check MCP validation
    assert "mcp_validation" in data
    assert data["mcp_validation"]["accepted"] == True
    assert "gates" in data["mcp_validation"]
    
    # Check response structure
    assert "status" in data
    assert "results" in data
    assert "count" in data

def test_add_knowledge_mcp_compliance(client):
    """Test add_knowledge MCP tool compliance"""
    response = client.post(
        "/api/add_knowledge",
        json={
            "content": "Test content for MCP compliance",
            "metadata": {"test": True}
        }
    )
    assert response.status_code == 200
    data = response.json()
    
    # Check MCP validation
    assert "mcp_validation" in data
    assert data["mcp_validation"]["accepted"] == True
    
    # Check response structure
    assert "status" in data
    assert "chunks_added" in data

def test_query_with_context_mcp_compliance(client):
    """Test query_with_context MCP tool compliance"""
    response = client.post(
        "/api/query_with_context",
        json={"query": "test query", "context_k": 3}
    )
    assert response.status_code == 200
    data = response.json()
    
    # Check MCP validation
    assert "mcp_validation" in data
    assert data["mcp_validation"]["accepted"] == True
    
    # Check response structure
    assert "context" in data
    assert "prompt" in data

def test_list_collections_mcp_compliance(client):
    """Test list_knowledge_collections MCP tool compliance"""
    response = client.get("/api/list_knowledge_collections")
    assert response.status_code == 200
    data = response.json()
    
    # Check MCP validation
    assert "mcp_validation" in data
    assert data["mcp_validation"]["accepted"] == True
    
    # Check response structure
    assert "collections" in data
    assert "count" in data

def test_knowledge_collections_resource(client):
    """Test knowledge://collections MCP resource"""
    response = client.get("/resources/knowledge/collections")
    assert response.status_code == 200
    data = response.json()
    
    # Check MCP validation
    assert "mcp_validation" in data
    assert data["mcp_validation"]["accepted"] == True

def test_collection_stats_resource(client):
    """Test knowledge://{collection}/stats MCP resource"""
    response = client.get("/resources/knowledge/digital_forge_knowledge/stats")
    assert response.status_code == 200
    data = response.json()
    
    # Check MCP validation
    assert "mcp_validation" in data
    assert data["mcp_validation"]["accepted"] == True
    
    # Check stats structure
    assert "stats" in data
    assert "vectors_count" in data["stats"]

def test_rag_research_prompt(client):
    """Test rag_research_prompt MCP prompt"""
    response = client.get("/prompts/rag_research_prompt")
    assert response.status_code == 200
    data = response.json()
    
    # Check MCP validation
    assert "mcp_validation" in data
    assert data["mcp_validation"]["accepted"] == True
    
    # Check prompt structure
    assert "template" in data
    assert "variables" in data
    assert "query" in data["variables"]
    assert "context" in data["variables"]

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
