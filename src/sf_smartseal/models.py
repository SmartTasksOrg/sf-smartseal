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
    signature: str
    chain: list[str]

@dataclass
class VerifyResult:
    valid: bool
    tampered: bool
    chain_len: int
