"""UML data objects for SmartSeal — the diagram in the README is these classes."""
from __future__ import annotations
from dataclasses import dataclass, field

@dataclass
class Manifest:
    artifact: str
    sha256: str
    created: str

@dataclass
class Receipt:
    manifest: Manifest
    signature: str          # Ed25519 signature, hex (128 characters)
    chain: list[str]        # signer name(s)
    public_key: str = ""    # signer's Ed25519 public key, hex (informational: verify against a key you trust)

@dataclass
class VerifyResult:
    valid: bool
    tampered: bool
    chain_len: int
    signature_ok: bool = False
