import typer
from rich.console import Console

hello = typer.Typer(help="Comandos de saludo")
console = Console()

@hello.command("say")
def say(name: str = typer.Argument(..., help="Nombre a saludar")) -> None:
    # Imprime un saludo sencillo.
    console.print(f"👋 Hello, [bold]{name}[/]!")

