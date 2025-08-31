import httpx
from fastmcp import FastMCP
import os
import subprocess

# Create an HTTP client for your API
client = httpx.AsyncClient(base_url="http://localhost:8000")

# Load your OpenAPI spec 
openapi_spec = httpx.get("http://localhost:8000/openapi.json").json()

# Create the MCP server
mcp = FastMCP.from_openapi(
    openapi_spec=openapi_spec,
    client=client,
    stateless_http=True, #!important for OpenAI Response API to accept the MCP streamable http transport mode
    name="MCP Server"
)
if __name__ == "__main__":
    print("Starting FastMCP server...")
    try:
        mcp.run(transport="streamable-http", host="0.0.0.0", port=3333, path="/mcp")
    except Exception as e:
        print(f"FastMCP server crashed: {{e}}", exc_info=True)
