#!/usr/bin/env python3
"""Regenerate expected.json from the Python reference (smartseal.core).
seal/verify take file paths, so content is written to temp files; the
non-deterministic `created` timestamp is dropped from the contract."""
import json, os, sys, tempfile
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.abspath(os.path.join(HERE, "..", "..", "src")))
from smartseal.core import seal, verify  # noqa: E402

def _tmp(content):
    fd, p = tempfile.mkstemp()
    with os.fdopen(fd, "w", encoding="utf-8", newline="") as f:
        f.write(content)
    return p

def do_seal(content, signer):
    p = _tmp(content); r = seal(p, signer); os.unlink(p)
    return {"sha256": r.manifest.sha256, "signature": r.signature, "chain": r.chain}

def do_verify(seal_content, content, signer, vsigner):
    ps = _tmp(seal_content); r = seal(ps, signer); os.unlink(ps)
    pc = _tmp(content); vr = verify(pc, r, vsigner); os.unlink(pc)
    return {"valid": vr.valid, "tampered": vr.tampered, "chain_len": vr.chain_len}

v = json.load(open(os.path.join(HERE, "vectors.json"), encoding="utf-8"))
res = []
for c in v["cases"]:
    signer = c.get("signer", "SmartSeal-demo")
    if c.get("op", "seal") == "seal":
        res.append({"name": c["name"], **do_seal(c.get("content", ""), signer)})
    else:
        res.append({"name": c["name"], **do_verify(c.get("seal_content", ""), c.get("content", ""),
                                                    signer, c.get("verify_signer", signer))})
out = {"results": res}
with open(os.path.join(HERE, "expected.json"), "w", encoding="utf-8") as f:
    json.dump(out, f, indent=2); f.write("\n")
print(f"wrote expected.json ({len(res)} cases)")
