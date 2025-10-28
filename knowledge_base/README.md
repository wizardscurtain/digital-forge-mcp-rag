# Digital Forge Knowledge Base

This directory contains the knowledge base documents for the Digital Forge MCP RAG system.

## Structure

```
knowledge_base/
├── documents/          # Source documents (markdown)
│   ├── architecture/   # System architecture docs
│   ├── guides/         # How-to guides
│   └── reference/      # API and configuration reference
└── index/             # Qdrant vector storage (auto-generated)
```

## Adding Documents

1. **Create markdown files** in the appropriate subdirectory:
   ```bash
   # Example: Add a new guide
   echo "# My Guide\n\nContent here..." > documents/guides/my-guide.md
   ```

2. **Run the setup script** to index new documents:
   ```bash
   python setup_rag.py
   ```

3. **Verify indexing:**
   ```bash
   curl http://localhost:8000/api/list_knowledge_collections
   ```

## Document Format

### Best Practices

- Use **clear headings** (H1, H2, H3)
- Include **code examples** with language tags
- Add **metadata** in frontmatter (optional)
- Keep documents **focused** on single topics
- Use **consistent terminology**

### Example Document

```markdown
---
title: FastAPI Best Practices
author: Digital Forge Team
date: 2025-01-15
tags: [fastapi, python, api]
---

# FastAPI Best Practices

## Introduction

FastAPI is a modern web framework...

## Key Principles

1. **Type hints everywhere**
2. **Dependency injection**
3. **Async when possible**

## Code Example

```python
from fastapi import FastAPI, Depends

app = FastAPI()

@app.get("/items/{item_id}")
async def read_item(item_id: int):
    return {"item_id": item_id}
```

## References

- [FastAPI Documentation](https://fastapi.tiangolo.com)
```

## Document Categories

### Architecture

System design, architecture decisions, and technical specifications.

**Examples:**
- System architecture overview
- Database schema design
- API design patterns
- Security architecture

### Guides

Step-by-step tutorials and how-to guides.

**Examples:**
- Getting started guide
- Deployment guide
- Integration guide
- Troubleshooting guide

### Reference

API documentation, configuration reference, and technical specifications.

**Examples:**
- API endpoint reference
- Configuration options
- Environment variables
- Error codes

## Chunking Strategy

Documents are automatically chunked using:

- **Chunk size:** 1000 characters
- **Overlap:** 200 characters
- **Separators:** `\n\n`, `\n`, ` `, ``

This ensures:
- Semantic coherence within chunks
- Context preservation across chunks
- Optimal retrieval performance

## Metadata

Each chunk includes metadata:

```json
{
  "source": "path/to/document.md",
  "filename": "document.md",
  "type": "markdown",
  "chunk_index": 0,
  "total_chunks": 5,
  "added_at": "2025-01-15T10:30:00Z"
}
```

## Search Tips

### Effective Queries

✅ **Good:**
- "How to implement authentication in FastAPI?"
- "Best practices for error handling"
- "Qdrant vector database setup"

❌ **Poor:**
- "auth" (too vague)
- "how do I do the thing" (unclear)
- "error" (too broad)

### Query Optimization

1. **Be specific** - Include context and details
2. **Use keywords** - Include technical terms
3. **Ask questions** - Natural language works well
4. **Iterate** - Refine based on results

## Maintenance

### Regular Tasks

1. **Review and update** outdated documents
2. **Add new content** as features are added
3. **Remove obsolete** information
4. **Optimize index** periodically

### Index Optimization

```bash
# Rebuild index from scratch
python setup_rag.py

# Or use the API
curl -X POST http://localhost:8000/api/update_knowledge_index \
  -H "Content-Type: application/json" \
  -d '{"force_rebuild": true}'
```

## Monitoring

### Collection Statistics

```bash
# Get collection stats
curl http://localhost:8000/resources/knowledge/digital_forge_knowledge/stats
```

### Search Quality

Monitor:
- **Relevance scores** - Should be > 0.7 for good matches
- **Result count** - Adjust `k` parameter as needed
- **Query latency** - Should be < 100ms for most queries

## Troubleshooting

### No Results Found

1. Check if documents are indexed:
   ```bash
   curl http://localhost:8000/api/list_knowledge_collections
   ```

2. Verify document content:
   ```bash
   ls -la documents/
   ```

3. Re-run setup:
   ```bash
   python setup_rag.py
   ```

### Poor Search Results

1. **Refine query** - Be more specific
2. **Increase k** - Get more results
3. **Check metadata** - Ensure proper categorization
4. **Update documents** - Add missing information

## Support

For questions or issues:
- Open an issue on GitHub
- Check the troubleshooting guide
- Contact support@digitalforge.dev
