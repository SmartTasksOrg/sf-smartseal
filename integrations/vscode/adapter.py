#!/usr/bin/env python3
"""SmartSeal integration adapter — the single source of truth for every
framework wrapper in this folder. Exposes TOOL_NAME, DESCRIPTION, INPUT_SCHEMA
and run(payload)->dict, plus a CLI:  python adapter.py --file <input>
"""
import argparse
import json
import os
import sys

from smartseal.core import seal

TOOL_NAME = "smartseal_seal"
DESCRIPTION = "Produce a content-addressed SHA-256 receipt (manifest + signature) for a file."
INPUT_SCHEMA = {
    "type": "object",
    "properties": {
        "path": {
                "type": "string",
                "description": "Path to the file to seal"
        }
    },
    "required": ["path"],
}


def _read(p):
    with open(p, encoding="utf-8", errors="ignore") as f:
        return f.read()


def run(payload):
    """Run SmartSeal on a payload dict and return a compact, JSON-safe result."""
    r = seal(payload['path'])
    result = {'artifact': r.manifest.artifact, 'sha256': r.manifest.sha256,
              'signature': r.signature, 'chain': r.chain}
    return result


def main(argv=None):
    ap = argparse.ArgumentParser(description=DESCRIPTION)
    ap.add_argument("--text")
    ap.add_argument("--file")
    ap.add_argument("--root")
    ap.add_argument("--sources")
    args = ap.parse_args(argv)
    payload = {'path': args.file or args.text}
    print(json.dumps(run(payload)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
