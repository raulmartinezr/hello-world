from importlib.metadata import PackageNotFoundError, version

__all__ = ["__version__"]

try:
    __version__ = version("hello-world")
except PackageNotFoundError:  # pragma: no cover
    __version__ = "0.0.0"
