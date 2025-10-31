import subprocess
from pytest_bdd import scenarios, when, then, parsers

scenarios("tests/bdd/features/say_hello.feature")

@when(parsers.parse('I run "{cmd}"'))
def run_cmd(cmd: str, tmp_path, request):
    res = subprocess.run(cmd.split(), capture_output=True, text=True)
    request.node._last_result = res  # type: ignore[attr-defined]

@then(parsers.parse('the output contains "{text}"'))
def output_contains(text: str, request):
    res = getattr(request.node, "_last_result")
    assert res.returncode == 0
    assert text in res.stdout

