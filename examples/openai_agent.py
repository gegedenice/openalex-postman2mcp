"""
OpenAlex Academic Agent demo using OpenAI API, MCPServerStreamableHttp, and Gradio UI.
- Loads API key from environment.
- Sets up an async agent for OpenAlex queries.
- Provides a Gradio interface for user questions.
"""

import os
import asyncio
from dotenv import load_dotenv
import openai
import gradio as gr
from agents.mcp import MCPServerStreamableHttp
from agents import Agent, Runner

# Constants
OPENALEX_MCP_URL = "http://localhost:3333/mcp"

# Global variables for server and agent
openalex_server = None
agent = None

def load_env_and_set_api_key():
    load_dotenv()
    openai.api_key = os.getenv("OPENAI_API_KEY")
    if not openai.api_key:
        raise ValueError("OPENAI_API_KEY is not set in the environment variables.")

async def setup_agent():
    global openalex_server, agent
    openalex_server = MCPServerStreamableHttp({"url": OPENALEX_MCP_URL})
    await openalex_server.connect()
    agent = Agent(
        model="gpt-4.1",
        name="OpenAlex Agent",
        instructions="You help the user search and analyze academic papers, authors, and institutions using the OpenAlex tool.",
        mcp_servers=[openalex_server]
    )
    # Warm up tools list
    await Runner.run(agent, "__prime__")

async def run_query(task: str):
    if agent is None:
        return "Agent not initialized."
    res = await Runner.run(agent, task)
    return res.final_output

def main():
    load_env_and_set_api_key()
    # Gradio UI
    with gr.Blocks() as demo:
        gr.Markdown("## 📚 OpenAlex Academic Agent")
        with gr.Row():
            input_box = gr.Textbox(label="Ask a research question", placeholder="e.g., Find the most cited papers by Geoffrey Hinton.")
        output_box = gr.Textbox(label="Agent's Response", lines=10)
        run_button = gr.Button("Run")
        demo.load(fn=setup_agent)
        run_button.click(run_query, input_box, output_box)
        demo.launch()

if __name__ == "__main__":
    main()
