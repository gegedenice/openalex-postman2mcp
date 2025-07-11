"""
Simple example: Query OpenAlex API using a CodeAgent and LiteLLMModel via MCPClient.
- Loads API key from environment.
- Runs a single query and prints the result.
"""

import os
from dotenv import load_dotenv
from smolagents import MCPClient, CodeAgent, LiteLLMModel


def main():
    load_dotenv()

    if not os.getenv("OPENAI_API_KEY"):
        raise ValueError("OPENAI_API_KEY is not set in the environment variables.")

    MCP_SERVER_URL = "http://localhost:3333/mcp"
    # Initialize the LiteLLMModel with the OpenAI API key
    model = LiteLLMModel(model_id="openai/o3-mini", api_key=os.getenv("OPENAI_API_KEY"))
    # Initialize server parameters and tools
    with MCPClient({"url": MCP_SERVER_URL, "transport": "streamable-http"}) as tools:
        agent = CodeAgent(
            tools=tools,
            model=model,
            add_base_tools=False,
            instructions=(
                "Use only parameters and endpoints defined in the OpenAPI schema and described in the tool documentation. "
                "Refer to the provided examples in the endpoint descriptions for correct parameter usage. "
                "Do not invent parameters. "
                "If you need to perform calculations (like summing APCs), fetch the data using valid parameters and process it in Python."
            )
        )
        result = agent.run(
            "What is the amount of paid APC by the EPFL institution in 2024? (EPFL is Ecole polytechnique Fédérale de Lausanne)"
        )
        # Process the result as needed
        print(f"Agent response: {result}")


if __name__ == "__main__":
    main()
    
