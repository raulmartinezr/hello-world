import sys

import typer
from loguru import logger
from rich.console import Console

from hello_world import __version__
from hello_world.cli.config import Settings
from hello_world.cli.hello import hello

app = typer.Typer(
    help="hello-world: CLI generado con Typer + Rich",
    no_args_is_help=True,
)
console = Console()


def setup_logging(verbose: int, log_file: str|None = None) -> None:
    """
    Configure Loguru based on verbosity level.
    0 -> WARNING, 1 -> INFO, 2 -> DEBUG, >=3 -> TRACE
    """
    # Map -v occurrences to Loguru levels
    levels = ["WARNING", "INFO", "DEBUG", "TRACE"]
    level = levels[min(verbose, len(levels) - 1)]

    # Remove default handlers and add a new one to stderr
    logger.remove()
    logger.add(
        sys.stderr,
        level=level,
        backtrace=True,  # shows full stack traces for nested exceptions
        diagnose=False,  # set True for detailed introspection during dev
        format="<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
        "<level>{level: <7}</level> | "
        "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - "
        "<level>{message}</level>",
    )

    # Optional file sink if a log file path is provided
    if log_file:
        logger.add(
            log_file,
            level=level,
            rotation="10 MB",
            retention="7 days",
            enqueue=True,  # makes file writing thread/process safe
            compression="zip",
            format="{time:YYYY-MM-DD HH:mm:ss.SSS} | {level: <7} | "
            "{name}:{function}:{line} - {message}",
        )

    logger.debug("Loguru configured (level={})", level)


@app.callback(invoke_without_command=True)
def main(
    ctx: typer.Context,
    verbose: int = typer.Option(
        0, "--verbose", "-v", count=True, help="Aumenta verbosidad (-v, -vv)"
    ),
    config_file: str | None = typer.Option(
        None, "--config", "-c", help="Ruta a fichero de configuración"
    ),
    version: bool = typer.Option(False, "--version", help="Muestra versión y sale"),
) -> None:
    # Callback global: carga configuración y opciones comunes.
    if version:
        console.print(f"[bold]hello-world[/] {__version__}")
        raise typer.Exit(code=0)

    settings = Settings.from_file(config_file) if config_file else Settings()

    # Optional log file coming from settings
    log_file = getattr(settings, "log_file", None)

    # Configure Loguru based on verbosity
    setup_logging(verbose=verbose, log_file=log_file)

    # Store settings in context for subcommands
    ctx.obj = settings
    logger.debug("Settings loaded: {}", settings)


# Subcomandos
app.add_typer(hello, name="hello")
