"""LangChain tool for SmartSeal.

    from tool import make_tools
    tools = make_tools()          # add to any agent / llm.bind_tools(tools)
"""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import json
from langchain_core.tools import StructuredTool
import adapter


def _run(**kwargs):
    return json.dumps(adapter.run(kwargs))


def make_tools():
    return [StructuredTool.from_function(
        func=_run, name=adapter.TOOL_NAME, description=adapter.DESCRIPTION,
    )]
