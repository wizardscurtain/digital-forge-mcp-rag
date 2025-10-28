# FastAPI MCP Integration Guide

## Overview

This guide covers integrating FastAPI applications with the Model Context Protocol (MCP) for AI agent interactions.

## What is MCP?

The Model Context Protocol (MCP) is a standardized protocol for AI agents to interact with external tools, resources, and prompts. It enables:

- **Tools**: Callable functions that agents can execute
- **Resources**: Data sources that agents can query
- **Prompts**: Template prompts for common tasks

## FastAPI-MCP Integration

### Installation

```bash
pip install fastapi-mcp
```

### Basic Setup

```python
from fastapi import FastAPI
from fastapi_mcp import FastApiMCP

app = FastAPI()

# Define your API endpoints
@app.get("/api/search")
async def search(query: str):
    return {"results": [...]}

# Mount MCP server
mcp = FastApiMCP(app)
mcp.mount()
```

### MCP Tools

MCP tools are automatically generated from FastAPI endpoints:

```python
@app.post("/api/search_knowledge")
async def search_knowledge(request: SearchRequest):
    """Search the knowledge base
    
    This becomes an MCP tool that agents can call.
    """
    # Implementation
    return {"results": [...]}
```

### MCP Resources

Resources provide read-only access to data:

```python
@app.get("/resources/knowledge/collections")
async def get_collections():
    """MCP Resource: knowledge://collections"""
    return {"collections": [...]}
```

### MCP Prompts

Prompts are templates for common tasks:

```python
@app.get("/prompts/research_prompt")
async def get_research_prompt():
    """MCP Prompt: research_prompt"""
    return {
        "template": "Based on {context}, answer {query}",
        "variables": ["context", "query"]
    }
```

## Best Practices

### 1. Clear Documentation

```python
@app.post("/api/tool")
async def my_tool(param: str):
    """Clear description of what this tool does.
    
    Args:
        param: Description of parameter
        
    Returns:
        Description of return value
    """
    pass
```

### 2. Type Hints

```python
from pydantic import BaseModel, Field

class SearchRequest(BaseModel):
    query: str = Field(..., description="Search query")
    k: int = Field(5, description="Number of results")
```

### 3. Error Handling

```python
from fastapi import HTTPException

@app.post("/api/tool")
async def my_tool(request: Request):
    try:
        # Implementation
        return {"status": "success"}
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Tool failed: {str(e)}"
        )
```

### 4. MCP Compliance

Include MCP validation in responses:

```python
return {
    "status": "success",
    "data": {...},
    "mcp_validation": {
        "accepted": True,
        "gates": "A0-A6"
    }
}
```

## GitHub Copilot Integration

### Configuration

1. Create `.vscode/mcp.json`:

```json
{
  "servers": {
    "my-mcp-server": {
      "type": "http",
      "url": "http://localhost:8000",
      "tools": ["search_knowledge", "add_knowledge"],
      "resources": ["knowledge://collections"],
      "prompts": ["research_prompt"]
    }
  }
}
```

2. Start MCP server
3. Open Copilot Chat
4. Switch to Agent mode
5. Access tools via tools icon

### Usage in Copilot

```
@agent search the knowledge base for "FastAPI patterns"
```

```
@agent add this content to the knowledge base: [content]
```

## Testing

### Unit Tests

```python
from fastapi.testclient import TestClient

client = TestClient(app)

def test_search_knowledge():
    response = client.post(
        "/api/search_knowledge",
        json={"query": "test", "k": 5}
    )
    assert response.status_code == 200
    assert "results" in response.json()
```

### MCP Compliance Tests

```python
def test_mcp_validation():
    response = client.post("/api/tool", json={...})
    data = response.json()
    assert "mcp_validation" in data
    assert data["mcp_validation"]["accepted"] == True
```

## Deployment

### Local Development

```bash
uvicorn app:app --reload --port 8000
```

### Production

```bash
uvicorn app:app --host 0.0.0.0 --port 8000 --workers 4
```

### Docker

```dockerfile
FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
```

## Troubleshooting

### Tools Not Appearing

1. Verify MCP server is running
2. Check `.vscode/mcp.json` configuration
3. Restart VS Code
4. Enable Agent mode in Copilot

### Authentication Issues

```python
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer

security = HTTPBearer()

@app.post("/api/tool")
async def my_tool(token: str = Depends(security)):
    if not validate_token(token):
        raise HTTPException(status_code=401)
    # Implementation
```

## Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com)
- [FastAPI-MCP GitHub](https://github.com/tadata-org/fastapi_mcp)
- [MCP Specification](https://modelcontextprotocol.io)
- [GitHub Copilot MCP Guide](https://docs.github.com/copilot)
