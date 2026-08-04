"""SmartSeal CLI — run `smartseal --demo`."""
import os, sys, json
from . import core
from ._version import __version__


def _demo_dir():
    return os.path.join(os.path.dirname(__file__), "..", "..", "demo")


def main(argv=None):
    argv = argv if argv is not None else sys.argv[1:]
    if "--version" in argv:
        print(f"SmartSeal {__version__}"); return 0
    demo = "--demo" in argv or not argv
    print(f"\n🦔 SmartSeal {__version__}  ·  IAIso §3 · Provenance")
    result = core_demo()
    print(result)
    print(f"\nBacked by IAIso §3 · Provenance · part of the Smart* family · https://smarttasks.cloud\n")
    return 0


def core_demo() -> str:
    return _DEMO()


def _DEMO():
    import tempfile
    p = os.path.join(tempfile.gettempdir(), "smartseal_demo.txt")
    open(p, "w").write("shipped artifact v1")
    rc = core.seal(p)
    ok = core.verify(p, rc)
    open(p, "a").write(" TAMPERED")
    bad = core.verify(p, rc)
    return (f"sealed {rc.manifest.artifact}  sha256:{rc.manifest.sha256[:16]}…\n"
            f"  verify (unchanged): valid={ok.valid} tampered={ok.tampered}\n"
            f"  verify (after edit): valid={bad.valid} tampered={bad.tampered}")

if __name__ == "__main__":
    sys.exit(main())
