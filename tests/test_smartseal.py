from sf_smartseal import cli

def test_demo_runs():
    assert cli.main(["--demo"]) == 0

def test_demo_produces_output():
    out = cli.core_demo()
    assert isinstance(out, str) and len(out) > 0
