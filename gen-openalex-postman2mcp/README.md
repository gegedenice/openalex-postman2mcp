# FastAPI MCP Project
This project contains a FastAPI-based MCP server that proxies requests to an OpenAPI-compliant API.

It has been generated with the [`postman2mcp`](https://github.com/gegedenice/postman2mcp) tool, which converts a Postman collection into an OpenAPI specification and sets up a FastAPI server to handle requests.

## Prerequisites

- Python 3.7 or later
- **Optional (for FastMCP Inspector):**  
   - [Node.js](https://nodejs.org/) (version 14 or later recommended)
   - [npm](https://www.npmjs.com/) (comes with Node.js)
   - To use the FastMCP Inspector, you will need to install the npm package `@modelcontextprotocol/inspector@0.16.0`:
      ```
      npm install -g @modelcontextprotocol/inspector@0.16.0
      ```
- **Optional:** an [Ngrok](https://ngrok.com/) account (for public tunneling)

## Setup (in several steps and separate terminals)

1. Install dependencies:
   ```   
    pip install -r requirements.txt
    ```
    
2. Set up your environment variables in `.env`:

   Normally the `.env` file is already generated in the project directory and should contain your Postman API key and ngrok authtoken:
   ```
   POSTMAN_API_KEY=your_postman_api_key
   NGROK_AUTHTOKEN=your_ngrok_authtoken
   ```
   Check if you have a `.env` file in the project directory, if not create one (the POSTMAN_API_KEY is optional at this stage).
   
3. Run the FastAPI server:
   ```
    uvicorn fastapi_proxy.main:app --host 0.0.0.0 --port 8000
    ```
4. Run the FastMCP server:
   ```
    python server.py
    ```
5. Optional but useful: run the FastMCP inspecteur:
   ```
   fastmcp dev server.py
    ```
5. Start the ngrok tunnel:
   ```
    python ngrok_tunnel.py
    ```
## Available URLs and Endpoints

### Postman Collection
You can find the Postman collection in `fastapi_proxy/postman_collection.json`.

### OpenAPI Specification
The OpenAPI specification is available at `fastapi_proxy/openapi.json`.    

### FastAPI Server
- The FastAPI server will be running at `http://localhost:8000`.
- Acces the plugin manifest at `http://localhost:8000/.well-known/ai-plugin.json`.
- Access the OpenAPI specification at `http://localhost:8000/openapi.json`.
- Access the Swagger API documentation at `http://localhost:8000/docs`.

### FastMCP server

The MCP server url is `http://localhost:3333/mcp`

### FastMCP Inspector
- Access the FastMCP Inspector at `http://localhost:6274` (get the token in the console output of the FastMCP server).

### Ngrok Tunnel
- Get the ngrok public url in the console output of the `ngrok_tunnel.py` script.
- You can access the MCP server at `http://<ngrok_url>/mcp`.
- Monitore your ngrok requests at `https://dashboard.ngrok.com` (login with your ngrok account).

## Integrations examples

### Claude Desktop

Currently, Claude Desktop does not support HTTP streamable transport for MCP. To connect your MCP server, you need to add it to your `claude_desktop_config.json` using mcp-remote with the http-only transport option:
```
{
  "mcpServers": {
    "my-mcp-server": {
      "command": "npx",
      "args": [
	    "-y",
        "mcp-remote",
        "http://localhost:3333/mcp",
        "--transport",
        "http-only"
      ]
    }
  }	
}
```
This configuration ensures Claude Desktop communicates with your MCP server over HTTP.
