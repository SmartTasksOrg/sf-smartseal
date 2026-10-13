#!/usr/bin/env python3
"""SmartSeal MCP server — zero dependencies.

Speaks the Model Context Protocol over stdio (newline-delimited JSON-RPC 2.0),
so it plugs into any MCP client: Claude Desktop, Cursor, Cline, Windsurf, Zed,
Continue. Register:
  { "mcpServers": { "smartseal": { "command": "python3",
      "args": ["/abs/path/integrations/mcp/server.py"] } } }
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import adapter

PROTOCOL = "2024-11-05"
SERVER = {"name": "smartseal", "version": "3.0.0"}
TOOLS = [{"name": adapter.TOOL_NAME, "description": adapter.DESCRIPTION, "inputSchema": adapter.INPUT_SCHEMA}]


def _reply(rid, result=None, error=None):
    m = {"jsonrpc": "2.0", "id": rid}
    if error is not None:
        m["error"] = error
    else:
        m["result"] = result
    sys.stdout.write(json.dumps(m) + "\n")
    sys.stdout.flush()


def main():
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            msg = json.loads(line)
        except Exception:
            continue
        method, rid = msg.get("method"), msg.get("id")
        if method == "initialize":
            _reply(rid, {"protocolVersion": PROTOCOL, "capabilities": {"tools": {}}, "serverInfo": SERVER})
        elif method == "tools/list":
            _reply(rid, {"tools": TOOLS})
        elif method == "tools/call":
            params = msg.get("params", {})
            try:
                out = adapter.run(params.get("arguments", {}))
                _reply(rid, {"content": [{"type": "text", "text": json.dumps(out)}]})
            except Exception as e:
                _reply(rid, error={"code": -32000, "message": str(e)})
        elif method and method.startswith("notifications/"):
            continue
        elif rid is not None:
            _reply(rid, error={"code": -32601, "message": f"method not found: {method}"})


if __name__ == "__main__":
    main()
