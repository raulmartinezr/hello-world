import pytest

@pytest.fixture(scope="session")
def cli_bin() -> str:
    return "hello-world"

