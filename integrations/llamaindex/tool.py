"""LlamaIndex tool for SmartSeal.

    from tool import make_tool
    agent = FunctionAgent(tools=[make_tool()], llm=llm)
"""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import json
from llama_index.core.tools import FunctionTool
import adapter


def _run(**kwargs):
    return json.dumps(adapter.run(kwargs))


def make_tool():
    return FunctionTool.from_defaults(fn=_run, name=adapter.TOOL_NAME, description=adapter.DESCRIPTION)
