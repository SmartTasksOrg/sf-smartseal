#!/usr/bin/env python3
"""Generic conformance comparator: deep-compare a port's {"results":[...]} on
stdin against expected.json (float-normalised, order-sensitive)."""
import json, sys
def norm(x):
    if isinstance(x, bool): return x
    if isinstance(x, float): return round(x, 6)
    if isinstance(x, list): return [norm(i) for i in x]
    if isinstance(x, dict): return {k: norm(v) for k, v in x.items()}
    return x
exp = norm(json.load(open(sys.argv[1], encoding="utf-8"))["results"])
got = norm(json.load(sys.stdin)["results"])
if exp == got:
    print(f"PASS ({len(exp)} cases)"); sys.exit(0)
if len(exp) != len(got):
    print(f"FAIL: {len(got)} results != expected {len(exp)}"); sys.exit(1)
for a, b in zip(exp, got):
    if a != b:
        print(f"FAIL at '{a.get('name')}':")
        print("  exp:", json.dumps(a, sort_keys=True, ensure_ascii=False))
        print("  got:", json.dumps(b, sort_keys=True, ensure_ascii=False)); sys.exit(1)
sys.exit(1)
