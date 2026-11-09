#!/usr/bin/env python3
"""Regenerate expected.json from the Python reference (sf_smartseal.core).
seal/verify take file paths, so content is written to temp files. Each signer
name gets a fixed TEST key derived from SHA-256(name), so runs are repeatable;
never use these keys for real. The signature covers the `created` timestamp, so
the signature value itself is dropped from the contract: ports must instead
produce receipts that verify (and fail to verify) exactly as listed here."""
import json, os, sys, tempfile
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.abspath(os.path.join(HERE, "..", "..", "src")))
import hashlib  # noqa: E402
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey  # noqa: E402
from sf_smartseal.core import public_key_hex, seal, verify  # noqa: E402


def test_key(name):
    """Deterministic TEST key for a signer name. Never use outside conformance."""
    return Ed25519PrivateKey.from_private_bytes(hashlib.sha256(name.encode()).digest())

def _tmp(content):
    fd, p = tempfile.mkstemp()
    with os.fdopen(fd, "w", encoding="utf-8", newline="") as f:
        f.write(content)
    return p

def do_seal(content, signer):
    p = _tmp(content); r = seal(p, test_key(signer), signer); os.unlink(p)
    return {"sha256": r.manifest.sha256, "public_key": r.public_key, "chain": r.chain,
            "signature_len": len(r.signature)}

def do_verify(seal_content, content, signer, vsigner):
    ps = _tmp(seal_content); r = seal(ps, test_key(signer), signer); os.unlink(ps)
    pc = _tmp(content); vr = verify(pc, r, public_key_hex(test_key(vsigner))); os.unlink(pc)
    return {"valid": vr.valid, "tampered": vr.tampered, "chain_len": vr.chain_len,
            "signature_ok": vr.signature_ok}

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
