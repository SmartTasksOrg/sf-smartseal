"""Behaviour of core.seal and core.verify: Ed25519-signed receipts."""
import hashlib
import json

import pytest

from sf_smartseal import cli, core
from sf_smartseal.models import Manifest, Receipt


def make(tmp_path, text="artifact v1"):
    p = tmp_path / "artifact.txt"
    p.write_text(text)
    return str(p)


@pytest.fixture
def keys():
    return core.generate_keypair()


def test_seal_records_the_digest_signer_and_key(tmp_path, keys):
    pem, pub = keys
    r = core.seal(make(tmp_path), pem, signer="alice")
    assert r.manifest.artifact == "artifact.txt"
    assert r.manifest.sha256 == hashlib.sha256(b"artifact v1").hexdigest()
    assert r.chain == ["alice"] and r.public_key == pub
    assert len(r.signature) == 128          # 64-byte Ed25519 signature, hex


def test_an_unchanged_file_verifies(tmp_path, keys):
    pem, pub = keys
    p = make(tmp_path)
    v = core.verify(p, core.seal(p, pem), pub)
    assert v.valid and v.signature_ok and not v.tampered


def test_a_changed_file_is_reported_as_tampered(tmp_path, keys):
    pem, pub = keys
    p = make(tmp_path)
    r = core.seal(p, pem)
    with open(p, "a") as f:
        f.write(" TAMPERED")
    v = core.verify(p, r, pub)
    assert v.tampered and not v.valid and v.signature_ok


def test_verifying_with_another_key_fails(tmp_path, keys):
    pem, _ = keys
    _, other = core.generate_keypair()
    p = make(tmp_path)
    v = core.verify(p, core.seal(p, pem), other)
    assert not v.valid and not v.signature_ok and not v.tampered


def test_the_old_keyless_forgery_no_longer_verifies(tmp_path, keys):
    """Version 3.0 receipts were SHA-256(digest + signer): anyone could make one."""
    _, pub = keys
    p = make(tmp_path, "attacker's file")
    d = hashlib.sha256(b"attacker's file").hexdigest()
    forged = Receipt(Manifest("artifact.txt", d, "2026-01-01T00:00:00Z"),
                     hashlib.sha256((d + "alice").encode()).hexdigest()[:32], ["alice"], public_key=pub)
    assert not core.verify(p, forged, pub).valid


def test_an_attacker_key_inside_the_receipt_is_not_trusted(tmp_path, keys):
    _, trusted_pub = keys
    attacker_pem, _ = core.generate_keypair()
    p = make(tmp_path)
    r = core.seal(p, attacker_pem, signer="alice")      # valid signature, wrong key
    assert not core.verify(p, r, trusted_pub).valid


@pytest.mark.parametrize("field", ["artifact", "created"])
def test_editing_any_signed_field_breaks_the_signature(tmp_path, keys, field):
    pem, pub = keys
    p = make(tmp_path)
    r = core.seal(p, pem, signer="alice")
    setattr(r.manifest, field, "edited")
    assert not core.verify(p, r, pub).signature_ok


def test_editing_the_signer_breaks_the_signature(tmp_path, keys):
    pem, pub = keys
    p = make(tmp_path)
    r = core.seal(p, pem, signer="alice")
    r.chain = ["mallory"]
    assert not core.verify(p, r, pub).valid


def test_seal_requires_a_key(tmp_path):
    with pytest.raises(ValueError, match="needs a private key"):
        core.seal(make(tmp_path))


def test_bad_public_keys_are_rejected():
    with pytest.raises(ValueError):
        core.load_public_key("not hex")
    with pytest.raises(ValueError):
        core.load_public_key("ab" * 16)


def test_receipts_round_trip_through_json(tmp_path, keys):
    pem, pub = keys
    p = make(tmp_path)
    r = core.seal(p, pem, signer="ci")
    again = core.receipt_from_json(core.receipt_to_json(r))
    assert again == r and core.verify(p, again, pub).valid


def test_version_3_receipts_are_refused_with_a_reason():
    old = json.dumps({"manifest": {"artifact": "a", "sha256": "0", "created": "t"},
                      "signature": "00", "chain": []})
    with pytest.raises(ValueError, match="reseal"):
        core.receipt_from_json(old)


def test_large_files_are_hashed_in_chunks(tmp_path, keys):
    pem, _ = keys
    p = tmp_path / "big.bin"
    data = b"x" * (8192 * 3 + 5)
    p.write_bytes(data)
    assert core.seal(str(p), pem).manifest.sha256 == hashlib.sha256(data).hexdigest()


def test_cli_keygen_seal_verify(tmp_path, capsys):
    p = make(tmp_path)
    prefix = str(tmp_path / "release")
    assert cli.main(["keygen", "--out", prefix]) == 0
    assert (tmp_path / "release.key").stat().st_mode & 0o077 == 0     # private key not world-readable
    assert cli.main(["seal", p, "--key", prefix + ".key", "--signer", "ci"]) == 0
    receipt = p + ".receipt.json"
    assert cli.main(["verify", p, receipt, "--pub", prefix + ".pub"]) == 0
    with open(p, "a") as f:
        f.write("x")
    assert cli.main(["verify", p, receipt, "--pub", prefix + ".pub"]) == 1
