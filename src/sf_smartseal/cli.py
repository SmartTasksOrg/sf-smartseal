"""SmartSeal CLI.

    sf-smartseal --demo                                  # bundled demo, saves nothing
    sf-smartseal keygen --out release                    # writes release.key (secret) and release.pub
    sf-smartseal seal FILE --key release.key [--signer NAME] [--out FILE.receipt.json]
    sf-smartseal verify FILE RECEIPT --pub release.pub   # exit 0 valid, 1 invalid or tampered
"""
import argparse
import os
import sys
import tempfile

from . import core
from ._version import __version__

BANNER = f"\n🦔 SmartSeal {__version__}  ·  IAIso §3 · Provenance"
FOOTER = "\nBacked by IAIso §3 · Provenance · part of the Smart* family · https://smarttasks.cloud\n"


def _demo_dir():
    return os.path.join(os.path.dirname(__file__), "..", "..", "demo")


def _read_pub(value: str) -> str:
    return open(value).read().strip() if os.path.exists(value) else value.strip()


def main(argv=None):
    argv = argv if argv is not None else sys.argv[1:]
    if "--version" in argv:
        print(f"SmartSeal {__version__}"); return 0
    if not argv or argv == ["--demo"] or "--demo" in argv:
        print(BANNER); print(core_demo()); print(FOOTER); return 0

    ap = argparse.ArgumentParser(prog="sf-smartseal")
    sub = ap.add_subparsers(dest="cmd", required=True)
    k = sub.add_parser("keygen", help="create an Ed25519 key pair")
    k.add_argument("--out", required=True, help="path prefix; writes PREFIX.key and PREFIX.pub")
    s = sub.add_parser("seal", help="sign a file")
    s.add_argument("file"); s.add_argument("--key", required=True, help="private key PEM file")
    s.add_argument("--signer", default=""); s.add_argument("--out", default=None)
    v = sub.add_parser("verify", help="verify a file against a receipt and a trusted public key")
    v.add_argument("file"); v.add_argument("receipt")
    v.add_argument("--pub", required=True, help="trusted public key: a .pub file or 64 hex characters")
    a = ap.parse_args(argv)

    if a.cmd == "keygen":
        pem, pub = core.generate_keypair()
        key_path, pub_path = a.out + ".key", a.out + ".pub"
        fd = os.open(key_path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
        with os.fdopen(fd, "wb") as fh:
            fh.write(pem)
        with open(pub_path, "w") as fh:
            fh.write(pub + "\n")
        print(f"private key: {key_path} (keep it secret)\npublic key:  {pub_path}  {pub}")
        return 0
    if a.cmd == "seal":
        receipt = core.seal(a.file, a.key, signer=a.signer)
        out = a.out or a.file + ".receipt.json"
        with open(out, "w") as fh:
            fh.write(core.receipt_to_json(receipt) + "\n")
        print(f"sealed {receipt.manifest.artifact}  sha256:{receipt.manifest.sha256[:16]}…  → {out}")
        return 0
    receipt = core.receipt_from_json(open(a.receipt).read())
    result = core.verify(a.file, receipt, _read_pub(a.pub))
    print(f"valid={result.valid} tampered={result.tampered} signature_ok={result.signature_ok}")
    return 0 if result.valid else 1


def core_demo() -> str:
    return _DEMO()


def _DEMO():
    with tempfile.TemporaryDirectory() as d:
        p = os.path.join(d, "smartseal_demo.txt")
        with open(p, "w") as fh:
            fh.write("shipped artifact v1")
        pem, pub = core.generate_keypair()
        rc = core.seal(p, pem, signer="demo")
        ok = core.verify(p, rc, pub)
        _, other_pub = core.generate_keypair()
        wrong = core.verify(p, rc, other_pub)
        with open(p, "a") as fh:
            fh.write(" TAMPERED")
        bad = core.verify(p, rc, pub)
    return (f"sealed {rc.manifest.artifact}  sha256:{rc.manifest.sha256[:16]}…  key:{pub[:16]}…\n"
            f"  verify (unchanged):     valid={ok.valid} tampered={ok.tampered}\n"
            f"  verify (someone else's key): valid={wrong.valid} signature_ok={wrong.signature_ok}\n"
            f"  verify (after edit):    valid={bad.valid} tampered={bad.tampered}")


if __name__ == "__main__":
    sys.exit(main())
