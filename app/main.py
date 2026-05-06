import os
import logging
from typing import Any, Dict, List, Optional
from fastapi import FastAPI, Request, HTTPException, Depends
from mcp.server.fastmcp import FastMCP
from app.clickup_client import ClickUpClient

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Token for SSE authentication
TOKEN = os.getenv("TOKEN", "default-token")

# Initialize FastMCP
mcp = FastMCP("ClickUp MCP Server", sse_path="/sse", message_path="/messages")

def get_clickup_client():
    return ClickUpClient()

@mcp.tool()
async def list_tasks(list_id: str, archived: bool = False) -> List[Dict[str, Any]]:
    """List tasks in a ClickUp list."""
    client = get_clickup_client()
    return await client.get_tasks(list_id, archived)

@mcp.tool()
async def get_task(task_id: str) -> Dict[str, Any]:
    """Get details of a specific ClickUp task."""
    client = get_clickup_client()
    return await client.get_task(task_id)

@mcp.tool()
async def create_task(list_id: str, name: str, description: str = "", priority: Optional[int] = None) -> Dict[str, Any]:
    """Create a new task in a ClickUp list."""
    client = get_clickup_client()
    data = {
        "name": name,
        "description": description,
    }
    if priority:
        data["priority"] = priority
    return await client.create_task(list_id, data)

@mcp.tool()
async def update_task(task_id: str, name: Optional[str] = None, description: Optional[str] = None, status: Optional[str] = None) -> Dict[str, Any]:
    """Update an existing ClickUp task."""
    client = get_clickup_client()
    data = {}
    if name: data["name"] = name
    if description: data["description"] = description
    if status: data["status"] = status
    return await client.update_task(task_id, data)

# Initialize FastAPI app
app = FastAPI()

@app.get("/health")
async def health():
    return {"status": "ok", "message": "ClickUp MCP Server is running"}

async def verify_token(request: Request):
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing or invalid Authorization header")

    token = auth_header.split(" ")[1]
    if token != TOKEN:
        raise HTTPException(status_code=401, detail="Unauthorized")

# FastMCP Starlette app
mcp_app = mcp.sse_app()

@app.get("/sse")
async def sse(request: Request, _ = Depends(verify_token)):
    # Find the sse route in mcp_app
    for route in mcp_app.routes:
        if route.path == "/sse":
            # Override host header for FastMCP transport security
            request.scope["headers"] = [(k, v) for k, v in request.scope["headers"] if k.lower() != b"host"]
            request.scope["headers"].append((b"host", b"localhost:7860"))
            return await route.endpoint(request)
    raise HTTPException(status_code=404)

@app.post("/messages")
async def messages(request: Request):
    # Find the messages route/mount in mcp_app
    for route in mcp_app.routes:
        if route.path == "/messages":
            # Override host header
            request.scope["headers"] = [(k, v) for k, v in request.scope["headers"] if k.lower() != b"host"]
            request.scope["headers"].append((b"host", b"localhost:7860"))
            return await route.app(request.scope, request.receive, request._send)
    raise HTTPException(status_code=404)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=7860)
