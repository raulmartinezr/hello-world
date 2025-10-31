import subprocess

from pytest import FixtureRequest
from pytest_bdd import parsers, scenarios, then, when

scenarios("tests/bdd/features/say_hello.feature")


@when(parsers.parse('I run "{cmd}"'))
def run_cmd(cmd: str, request: FixtureRequest) -> None:
    res = subprocess.run(cmd.split(), capture_output=True, text=True)
    request.node._last_result = res  # type: ignore[attr-defined, unused-ignore]


@then(parsers.parse('the output contains "{text}"'))
def output_contains(text: str, request: FixtureRequest) -> None:
    """
    Assert that the last captured CLI result succeeded and its stdout contains `text`.

    Expects `request.node._last_result` to be set by a prior step/fixture to an
    object implementing CompletedRun (e.g., from subprocess, click/typer runner, etc.).
    """
    # Retrieve the last result attached to the test node by a previous step/fixture
    res = getattr(request.node, "_last_result", None)  # type: ignore[attr-defined, unused-ignore]
    assert res is not None, "No _last_result found on request.node; ensure a prior step sets it."

    assert res.returncode == 0, (
        f"Expected returncode 0, got {res.returncode}. Stderr:\n{res.stderr}"
    )
    assert text in res.stdout, f'Expected to find "{text}" in stdout.\nstdout:\n{res.stdout}'
