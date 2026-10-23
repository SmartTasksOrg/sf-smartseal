"""Behaviour of core.seal and core.verify. The receipt's signature is a keyless hash: it detects a
changed file, not who made the receipt (see README, Status)."""
import hashlib
from sf_smartseal import core


def make(tmp_path, text="artifact v1"):
    p = tmp_path / "artifact.txt"
    p.write_text(text)
    return str(p)


def test_seal_records_the_file_digest_and_the_signer(tmp_path):
    p = make(tmp_path)
    r = core.seal(p, signer="alice")
    assert r.manifest.artifact == "artifact.txt"
    assert r.manifest.sha256 == hashlib.sha256(b"artifact v1").hexdigest()
    assert r.chain == ["alice"] and len(r.signature) == 32


def test_an_unchanged_file_verifies(tmp_path):
    p = make(tmp_path)
    v = core.verify(p, core.seal(p))
    assert v.valid and not v.tampered and v.chain_len == 1


def test_a_changed_file_is_reported_as_tampered(tmp_path):
    p = make(tmp_path)
    r = core.seal(p)
    with open(p, "a") as f:
        f.write(" TAMPERED")
    v = core.verify(p, r)
    assert v.tampered and not v.valid


def test_verifying_with_another_signer_name_fails(tmp_path):
    p = make(tmp_path)
    v = core.verify(p, core.seal(p, signer="alice"), signer="mallory")
    assert not v.tampered and not v.valid


def test_the_signature_needs_no_key_so_anyone_can_recompute_it(tmp_path):
    p = make(tmp_path)
    r = core.seal(p, signer="alice")
    assert r.signature == hashlib.sha256((r.manifest.sha256 + "alice").encode()).hexdigest()[:32]


def test_large_files_are_hashed_in_chunks(tmp_path):
    p = tmp_path / "big.bin"
    data = b"x" * (8192 * 3 + 5)
    p.write_bytes(data)
    assert core.seal(str(p)).manifest.sha256 == hashlib.sha256(data).hexdigest()
