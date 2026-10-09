"""SmartSeal core — content-addressed manifest + verify."""
import hashlib, os, time
from .models import Manifest, Receipt, VerifyResult

def _sha256(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()

def seal(path: str, signer: str = "SmartSeal-demo") -> Receipt:
    digest = _sha256(path)
    man = Manifest(os.path.basename(path), digest, time.strftime("%Y-%m-%dT%H:%M:%SZ"))
    sig = hashlib.sha256((digest + signer).encode()).hexdigest()[:32]
    return Receipt(man, sig, [signer])

def verify(path: str, receipt: Receipt, signer: str = "SmartSeal-demo") -> VerifyResult:
    now = _sha256(path)
    tampered = now != receipt.manifest.sha256
    expected_sig = hashlib.sha256((receipt.manifest.sha256 + signer).encode()).hexdigest()[:32]
    return VerifyResult(valid=(not tampered and expected_sig == receipt.signature),
                        tampered=tampered, chain_len=len(receipt.chain))
