# Render Deployment Guide

## Automatic Deployment via Render Dashboard

### Step 1: Connect GitHub Repository

1. Go to [Render Dashboard](https://dashboard.render.com)
2. Click "New +" → "Web Service"
3. Connect your GitHub account if not already connected
4. Select repository: `wizardscurtain/digital-forge-mcp-rag`
5. Click "Connect"

### Step 2: Configure Service

**Basic Settings:**
- **Name:** `digital-forge-mcp-rag`
- **Region:** Oregon (US West)
- **Branch:** `main`
- **Runtime:** Python 3

**Build Settings:**
- **Build Command:** `pip install -r requirements.txt`
- **Start Command:** `uvicorn rag_mcp_server:app --host 0.0.0.0 --port $PORT`

**Plan:**
- Select **Starter** or higher (Free tier not supported for Python services)

### Step 3: Environment Variables

Add the following environment variables:

| Key | Value | Notes |
|-----|-------|-------|
| `PYTHON_VERSION` | `3.12.0` | Python version |
| `QDRANT_HOST` | `localhost` | Qdrant host (will need external service) |
| `QDRANT_PORT` | `6333` | Qdrant port |
| `EMBEDDING_MODEL` | `text-embedding-3-small` | OpenAI embedding model |
| `OPENAI_API_KEY` | `<your-key>` | **Secret** - Add your OpenAI API key |

### Step 4: Health Check

- **Health Check Path:** `/health`
- **Health Check Interval:** 30 seconds

### Step 5: Deploy

1. Click "Create Web Service"
2. Wait for deployment (5-10 minutes)
3. Monitor build logs
4. Verify health check passes

## Deployment URL

Once deployed, your service will be available at:
```
https://digital-forge-mcp-rag.onrender.com
```

## Verify Deployment

### Test Health Endpoint

```bash
curl https://digital-forge-mcp-rag.onrender.com/health
```

Expected response:
```json
{
  "status": "healthy",
  "timestamp": "2025-01-15T10:30:00Z",
  "services": {
    "qdrant": "healthy",
    "embeddings": "healthy",
    "vectorstore": "healthy"
  },
  "mcp_compliance": "A0-A6"
}
```

### Test API Documentation

Access Swagger UI:
```
https://digital-forge-mcp-rag.onrender.com/docs
```

## Important Notes

### Qdrant Service

⚠️ **Note:** The current configuration uses `localhost` for Qdrant, which won't work in production.

**Options:**

1. **Qdrant Cloud (Recommended):**
   - Sign up at [cloud.qdrant.io](https://cloud.qdrant.io)
   - Create a cluster
   - Update `QDRANT_HOST` and `QDRANT_PORT` environment variables
   - Add `QDRANT_API_KEY` if using authentication

2. **Separate Render Service:**
   - Deploy Qdrant as a separate Docker service on Render
   - Use internal Render networking
   - Update `QDRANT_HOST` to the internal service URL

3. **Docker Compose (Not supported on Render free/starter):**
   - Requires higher tier plan
   - Use `render.yaml` with multiple services

### Cold Starts

Render free/starter plans have cold starts:
- Service spins down after 15 minutes of inactivity
- First request after spin-down takes 30-60 seconds
- Consider upgrading to paid plan for always-on service

### Logs

View logs in Render Dashboard:
1. Go to your service
2. Click "Logs" tab
3. Monitor for errors or warnings

## Troubleshooting

### Build Fails

**Check:**
- Python version compatibility
- Requirements.txt syntax
- Build logs for specific errors

**Solution:**
```bash
# Test locally first
pip install -r requirements.txt
python -c "import fastapi, qdrant_client, langchain"
```

### Health Check Fails

**Check:**
- Service is actually running
- Port binding is correct ($PORT)
- Health endpoint returns 200

**Solution:**
```bash
# Test locally
uvicorn rag_mcp_server:app --host 0.0.0.0 --port 8000
curl http://localhost:8000/health
```

### Qdrant Connection Fails

**Check:**
- QDRANT_HOST and QDRANT_PORT are correct
- Qdrant service is running
- Network connectivity

**Solution:**
- Use Qdrant Cloud for production
- Update environment variables
- Restart service

## Manual Deployment via Render API

For automated deployments, use the Render API:

```bash
curl -X POST https://api.render.com/v1/services \
  -H "Authorization: Bearer YOUR_RENDER_API_KEY" \
  -H "Content-Type: application/json" \
  -d @render-service-config.json
```

See `render-service-config.json` for the full configuration.

## Continuous Deployment

Render automatically deploys on push to `main` branch:

1. Make changes locally
2. Commit and push to GitHub
3. Render detects changes
4. Automatic build and deploy
5. Health check verification
6. Service goes live

## Monitoring

### Metrics

Render provides:
- CPU usage
- Memory usage
- Request count
- Response times
- Error rates

### Alerts

Set up alerts for:
- Health check failures
- High error rates
- Resource exhaustion
- Deployment failures

## Scaling

### Vertical Scaling

Upgrade plan for more resources:
- Starter: 512 MB RAM
- Standard: 2 GB RAM
- Pro: 4 GB RAM

### Horizontal Scaling

Add multiple instances:
- Load balancing automatic
- Session affinity if needed
- Shared Qdrant backend required

## Cost Optimization

1. **Use Qdrant Cloud free tier** (1 GB storage)
2. **Optimize embeddings** (cache frequently used)
3. **Implement rate limiting** (prevent abuse)
4. **Monitor usage** (track API calls)
5. **Scale down** when not needed

## Production Checklist

- [ ] Qdrant Cloud configured
- [ ] OpenAI API key set
- [ ] Health checks passing
- [ ] API documentation accessible
- [ ] Logs monitored
- [ ] Alerts configured
- [ ] Backup strategy in place
- [ ] Rate limiting enabled
- [ ] HTTPS enforced
- [ ] CORS configured

## Support

For deployment issues:
- Check Render status: [status.render.com](https://status.render.com)
- Render docs: [render.com/docs](https://render.com/docs)
- GitHub issues: [github.com/wizardscurtain/digital-forge-mcp-rag/issues](https://github.com/wizardscurtain/digital-forge-mcp-rag/issues)
