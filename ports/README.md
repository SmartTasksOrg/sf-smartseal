# SmartSeal \u2014 language ports

Native Go / Node / Java / PHP re-implementations of `seal()` / `verify()`.
Each reproduces the Python reference (`src/sf_smartseal/core.py`): the SHA-256 content
digest, the 32-hex signature `sha256(digest+signer)`, and the tamper/valid checks.

The reference also stamps a `created` timestamp; that field is **non-deterministic**
and deliberately excluded from the port contract \u2014 only the content-addressed
fields are verified. Run `conformance/run.sh` to check every installed runtime.
