"""
Multi-agent OpenAlex analysis and charting demo using smolagents, Gradio, and OpenAI API.
- Analyst agent delegates OpenAlex API queries to a tool-calling agent.
- Analyst agent handles data analysis, charting, and user-facing answers.
- Gradio UI for interactive exploration.
"""

import os
from dotenv import load_dotenv

import gradio as gr
from smolagents import MCPClient, ToolCallingAgent, CodeAgent, OpenAIServerModel, GradioUI

# Third-party libraries used by agents (not directly in this script, but required)
# import altair as alt
# import pandas as pd


def main():
    load_dotenv()

    if not os.getenv("OPENAI_API_KEY"):
        raise ValueError("OPENAI_API_KEY is not set in the environment variables.")

    model = OpenAIServerModel(
        model_id="gpt-4.1",
        api_base="https://api.openai.com/v1",
        api_key=os.environ["OPENAI_API_KEY"],
    )

    MCP_SERVER_URL = "http://localhost:3333/mcp"
    tools = MCPClient({"url": MCP_SERVER_URL, "transport": "streamable-http"}).get_tools()

    # Agent for querying OpenAlex API
    openalex_agent = ToolCallingAgent(
        tools=tools,  # Use the tools directly from MCPClient
        model=model,
        max_steps=10,
        name="openalex_agent",
        description="Runs requests on OpenAlex API endpoints defined in the OpenAPI schema.",
        instructions=(
            "Use only parameters and endpoints defined in the OpenAPI schema and described in the tools documentation. "
            "Refer to the provided examples in the endpoint descriptions for correct parameter usage. "
            "Do not invent parameters. "
            "If you need to perform calculations (like summing APCs), fetch the data using valid parameters and process it in Python."
            "If the OpenAPI schema provides enums or explicit value ranges for parameters, validate that user-supplied/analyst-supplied parameters conform to these before making a request."),
    )

    # Agent for analysis, charting, and user-facing answers
    analyst_agent = CodeAgent(
        tools=[],  # No direct API tools, but can call openalex_agent
        model=model,
        name="analyst_agent",
        managed_agents=[openalex_agent],
        additional_authorized_imports=["time", "numpy", "pandas", "json", "re"],
        description="You are an analyst agent: Analyzes OpenAlex data, generates charts and reports.",
        add_base_tools=False,
        instructions=(
            "Interpret user questions. "
            "Always break down the problem into clear steps before answering. "
            "If a query requires an entity ID (such as institution, publisher, or topic), "
            "first use the appropriate endpoint (e.g., List_institutions, List_publishers, List_topics) to retrieve the ID by searching with the entity's name. "
            "Then, use this ID in subsequent queries as a filter or group_by parameter. For example, to filter on an institution, use the `authorships.institutions.lineage:ixxxxxxx` parameter."
            "Never use entity names directly in filters or group_by—always resolve and use the correct ID. "
            "Never simulate or invent IDs or data. Always use the appropriate tool to retrieve real IDs and values, even if you think you know them. "
            "Do not use hardcoded or example IDs. Always call List_institutions (or the relevant tool) to get the actual ID before proceeding. "
            "Delegate all data queries to openalex_agent, analyze and process the results, and generate human-readable answers with charts and text. "
            "Always validate API response data and handle missing, empty, or error responses gracefully. "
            "For each user question, first write a plan as a numbered list of steps, then execute each step in order, showing your reasoning. "
            "Use pandas for data analysis. "
            "Do not query the OpenAlex API directly; always use openalex_agent for data."
            "\n\nExample:\n"
            "Question: How many open access publications at EPFL in 2022?\n"
            "Plan:\n"
            "1. Use List_institutions with search='Ecole Polytechnique Fédérale de Lausanne' to get the institution ID.\n"
            "2. Use List_works with filter='authorships.institutions.lineage:I<ID> and publication_year:2022' to get the publication count.\n"
            "3. Present the result in a human-readable format.\n"
        ),
    )

    # Initialize GradioUI once
    ui = GradioUI(analyst_agent)
    ui.launch()


if __name__ == "__main__":
    main()