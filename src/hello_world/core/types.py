"""Defining types"""

from collections.abc import Awaitable, Callable
from typing import Any

AsyncCallable = Callable[..., Awaitable[Any]]
