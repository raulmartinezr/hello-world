from typing import Optional
import typer
from rich.console import Console
from hello_world import __version__
from hello_world.cli.commands.hello import hello
from hello_world.cli.config import Settings

app = typer.Typer(help="hello-world: CLI generado con Typer + Rich")
console = Console()

@app.callback()
def main(
    ctx: typer.Context,
    verbose: int = typer.Option(
        0, "--verbose", "-v", count=True, help="Aumenta verbosidad (-v, -vv)"
    ),
    config_file: Optional[str] = typer.Option(
        None, "--config", "-c", help="Ruta a fichero de configuración"
    ),
    version: bool = typer.Option(False, "--version", help="Muestra versión y sale"),
) -> None:
    # Callback global: carga configuración y opciones comunes.
    if version:
        console.print(f"[bold]hello-world[/] {__version__}")
        raise typer.Exit(code=0)

    ctx.obj = Settings.from_file(config_file) if config_file else Settings()

# Subcomandos
app.add_typer(hello, name="hello")

