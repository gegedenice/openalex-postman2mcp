
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.openapi.docs import get_swagger_ui_html
import httpx
import os
import uvicorn

app = FastAPI(title="FastAPi server", openapi_url=None )

# CORS for LLM or local dev tools
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# OpenAPI and Swagger UI
# ================================
@app.get("/.well-known/ai-plugin.json")
async def plugin_manifest():
    return {'schema_version': 'v1', 'name_for_human': 'Generic FastAPI', 'name_for_model': 'generic_api', 'description_for_human': 'Interact with a generic API via MCP.', 'description_for_model': 'Plugin for querying a generic API using MCP.', 'auth': {'type': 'none'}, 'api': {'type': 'openapi', 'url': 'http://localhost:8000/openapi.json'}, 'logo_url': 'https://example.com/logo.png', 'contact_email': 'support@example.com', 'legal_info_url': 'https://example.com/terms'}
    
@app.get("/openapi.json", include_in_schema=False)
async def serve_openapi():
    return FileResponse("fastapi_proxy/openapi.json", media_type="application/json")


@app.get("/docs", include_in_schema=False)
async def custom_docs():
    return get_swagger_ui_html(openapi_url="/openapi.json", title="OpenAlex API Docs")

@app.get("/")
async def root():
    return {"message": "FastAPI MCP-compatible proxy server is running.", "docs": "/docs", "openapi": "/openapi.json"}

# Proxy endpoints
# ================================
@app.get("/{full_path:path}")
async def generic_proxy_get(full_path: str, request: Request):
    target_url = f"https://api.openalex.org/{full_path}"
    query_params = dict(request.query_params)

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(target_url, params=query_params)
        return JSONResponse(status_code=response.status_code, content=response.json())
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
