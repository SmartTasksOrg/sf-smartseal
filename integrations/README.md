# SmartSeal — integrations

Drop-in ways to run **SmartSeal** inside the tools and frameworks you already use.
Every wrapper here calls one source of truth, [`adapter.py`](adapter.py), which wires
straight to the Python core (`seal`).

| Target | Path | What it gives you |
|---|---|---|
| LangChain | [`langchain/tool.py`](langchain/tool.py) | a `StructuredTool` for any LangChain agent |
| LlamaIndex | [`llamaindex/tool.py`](llamaindex/tool.py) | a `FunctionTool` for LlamaIndex agents |
| OpenAI / Anthropic / Gemini | [`function-calling/schema.py`](function-calling/schema.py) | tool schemas + `dispatch()` |
| MCP (Claude Desktop, Cursor, Cline, Windsurf, Zed) | [`mcp/server.py`](mcp/server.py) | a zero-dep stdio MCP server |
| Flowise | [`flowise/`](flowise/) | a custom node for the visual builder |
| VS Code | [`vscode/`](vscode/) | a command that runs it on the active file/workspace |
| GitHub Actions | [`github-action/action.yml`](github-action/action.yml) | a composite action for CI |
| pre-commit / git hook | [`precommit/`](precommit/) | gate commits locally |

## Quick check
```bash
python integrations/adapter.py --file <file>
```
Returns a compact JSON result — the same shape every wrapper emits.
