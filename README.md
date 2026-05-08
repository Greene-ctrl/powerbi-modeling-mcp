---
title: Clickup Mcp
emoji: 🐨
colorFrom: red
colorTo: gray
sdk: docker
pinned: false
app_port: 7860
---

# ClickUp MCP Server

This is an MCP server for ClickUp, deployed to Hugging Face Spaces.

## API Endpoints

- `GET /health`: Health check endpoint.
- `GET /sse`: MCP SSE connection endpoint (requires Bearer token).
- `POST /messages`: MCP messages endpoint.

## Configuration

The following environment variables are required:

- `CLICKUP_API_KEY`: Your ClickUp Personal API Key.
- `TOKEN`: The secret token for authenticating SSE connections.
