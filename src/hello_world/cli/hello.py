from asyncio import run as aiorun

import typer
from rich.console import Console

hello = typer.Typer(
    help="Hello commands",
    no_args_is_help=True,
)
console = Console()


async def _main(name: str) -> None:
    console.print(f"👋 Hello, [bold]{name}[/]!")


@hello.command("say")
def say(name: str = typer.Argument(..., help="Name to say hello to")) -> None:
    aiorun(_main(name=name))
