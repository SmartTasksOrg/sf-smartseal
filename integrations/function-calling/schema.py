"""Framework-agnostic function/tool schema for SmartSeal.

Drop into any tool-calling loop — OpenAI, Anthropic, Gemini, Mistral, Bedrock.
`TOOLS_OPENAI` / `TOOLS_ANTHROPIC` are the schemas to advertise; `dispatch(name, args)`
runs the call and returns a compact JSON string.
"""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import json
import adapter

TOOLS_OPENAI = [{"type": "function", "function": {
    "name": adapter.TOOL_NAME, "description": adapter.DESCRIPTION, "parameters": adapter.INPUT_SCHEMA}}]

TOOLS_ANTHROPIC = [{
    "name": adapter.TOOL_NAME, "description": adapter.DESCRIPTION, "input_schema": adapter.INPUT_SCHEMA}]


def dispatch(name, args):
    if name == adapter.TOOL_NAME:
        return json.dumps(adapter.run(args))
    raise ValueError(f"unknown tool: {name}")
