import subprocess


def test_version(cli_bin: str) -> None:
    res = subprocess.run([cli_bin, "--version"], capture_output=True, text=True)
    assert res.returncode == 0
    assert "hello-world" in res.stdout
