"""SmartSeal core — content-addressed manifest, signed with Ed25519, and verify.

A receipt binds a file's SHA-256 digest, its name, a timestamp and the signer's
name to the signer's Ed25519 key. Anyone holding the signer's *public* key can
check that the file is unchanged and that the receipt was made by the holder of
the matching *private* key. Without that private key a receipt cannot be forged.

    priv_pem, pub_hex = generate_keypair()          # keep priv_pem secret; publish pub_hex
    receipt = seal("build.tar.gz", priv_pem, signer="release-bot")
    verify("build.tar.gz", receipt, pub_hex).valid  # True

Always verify against a public key you obtained from a trusted place (your
release notes, a key server, your own config), never only the key printed
inside the receipt: an attacker can make a valid receipt with their own key.
"""
from __future__ import annotations

import hashlib
import json
import os
import time
from typing import Union

from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.ed25519 import (
    Ed25519PrivateKey,
    Ed25519PublicKey,
)

from .models import Manifest, Receipt, VerifyResult

PrivateKeyLike = Union[Ed25519PrivateKey, bytes, str]
PublicKeyLike = Union[Ed25519PublicKey, bytes, str]

RECEIPT_FORMAT = "sf-smartseal/receipt/v2"


def _sha256(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


# ---------------------------------------------------------------- keys

def generate_keypair() -> tuple[bytes, str]:
    """Return (private key as PEM bytes, public key as 64 hex characters)."""
    key = Ed25519PrivateKey.generate()
    pem = key.private_bytes(
        serialization.Encoding.PEM,
        serialization.PrivateFormat.PKCS8,
        serialization.NoEncryption(),
    )
    return pem, public_key_hex(key)


def load_private_key(key: PrivateKeyLike) -> Ed25519PrivateKey:
    """Accept a key object, PEM bytes, PEM text, or a path to a PEM file."""
    if isinstance(key, Ed25519PrivateKey):
        return key
    if isinstance(key, str):
        data = open(key, "rb").read() if os.path.exists(key) else key.encode()
    elif isinstance(key, bytes):
        data = key
    else:
        raise TypeError("private key must be an Ed25519 key, PEM bytes/text or a PEM file path")
    loaded = serialization.load_pem_private_key(data, password=None)
    if not isinstance(loaded, Ed25519PrivateKey):
        raise ValueError("private key is not an Ed25519 key")
    return loaded


def load_public_key(key: PublicKeyLike) -> Ed25519PublicKey:
    """Accept a key object, 32 raw bytes, or 64 hex characters."""
    if isinstance(key, Ed25519PublicKey):
        return key
    if isinstance(key, str):
        try:
            key = bytes.fromhex(key.strip())
        except ValueError as exc:
            raise ValueError("public key must be 64 hex characters") from exc
    if not isinstance(key, bytes) or len(key) != 32:
        raise ValueError("public key must be 32 bytes (64 hex characters)")
    return Ed25519PublicKey.from_public_bytes(key)


def public_key_hex(key: Union[Ed25519PrivateKey, Ed25519PublicKey]) -> str:
    pub = key.public_key() if isinstance(key, Ed25519PrivateKey) else key
    return pub.public_bytes(serialization.Encoding.Raw, serialization.PublicFormat.Raw).hex()


# ---------------------------------------------------------------- seal / verify

def _signed_bytes(manifest: Manifest, signer: str, public_key: str) -> bytes:
    """Canonical bytes that the signature covers: every field of the receipt."""
    payload = {
        "format": RECEIPT_FORMAT,
        "artifact": manifest.artifact,
        "sha256": manifest.sha256,
        "created": manifest.created,
        "signer": signer,
        "public_key": public_key,
    }
    return json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()


def seal(path: str, private_key: PrivateKeyLike | None = None, signer: str = "") -> Receipt:
    """Hash `path` and sign the manifest with `private_key`."""
    if private_key is None:
        raise ValueError("seal() needs a private key; create one with generate_keypair() "
                         "or `sf-smartseal keygen`")
    key = load_private_key(private_key)
    pub = public_key_hex(key)
    man = Manifest(os.path.basename(path), _sha256(path),
                   time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()))
    signature = key.sign(_signed_bytes(man, signer, pub)).hex()
    return Receipt(man, signature, [signer] if signer else [], public_key=pub)


def verify(path: str, receipt: Receipt, public_key: PublicKeyLike) -> VerifyResult:
    """Check the file against the receipt, and the receipt against a trusted public key.

    `valid` is True only when the file is unchanged, the receipt names the same
    key you trust, and the signature over every receipt field checks out.
    """
    trusted = load_public_key(public_key)
    trusted_hex = public_key_hex(trusted)
    tampered = _sha256(path) != receipt.manifest.sha256
    signer = receipt.chain[0] if receipt.chain else ""
    try:
        if receipt.public_key and receipt.public_key != trusted_hex:
            raise InvalidSignature("receipt was made with a different key")
        trusted.verify(bytes.fromhex(receipt.signature),
                       _signed_bytes(receipt.manifest, signer, trusted_hex))
        signature_ok = True
    except (InvalidSignature, ValueError):
        signature_ok = False
    return VerifyResult(valid=signature_ok and not tampered, tampered=tampered,
                        chain_len=len(receipt.chain), signature_ok=signature_ok)


# ---------------------------------------------------------------- receipts on disk

def receipt_to_json(receipt: Receipt) -> str:
    return json.dumps({
        "format": RECEIPT_FORMAT,
        "manifest": {"artifact": receipt.manifest.artifact,
                     "sha256": receipt.manifest.sha256,
                     "created": receipt.manifest.created},
        "signature": receipt.signature,
        "chain": receipt.chain,
        "public_key": receipt.public_key,
    }, indent=2)


def receipt_from_json(text: str) -> Receipt:
    d = json.loads(text)
    if d.get("format") != RECEIPT_FORMAT:
        raise ValueError(f"not a {RECEIPT_FORMAT} receipt (version 3.0 receipts were "
                         "unsigned and cannot be verified; reseal the file)")
    m = d["manifest"]
    return Receipt(Manifest(m["artifact"], m["sha256"], m["created"]),
                   d["signature"], list(d.get("chain", [])), public_key=d.get("public_key", ""))
