import click
import time
from rich.console import Console

from dasshh.core.logging import setup_logging
from dasshh.ui.utils import load_config, DEFAULT_CONFIG_PATH

__version__ = "0.1.2"


@click.group(
    context_settings={
        "help_option_names": ["-h", "--help"],
    },
    invoke_without_command=True,
)
@click.version_option(version=__version__)
@click.option(
    "--log-file",
    help="Path to log file. Default is ~/.dasshh/logs/dasshh.log",
    type=click.Path(),
)
@click.option(
    "--debug",
    is_flag=True,
    help="Enable debug logging",
)
@click.pass_context
def main(ctx, version: bool = False, log_file=None, debug=False) -> None:
    import logging

    log_level = logging.DEBUG if debug else logging.INFO
    setup_logging(log_file=log_file, log_level=log_level)
    logger = logging.getLogger("dasshh.main")

    if version:
        click.echo(__version__)
        logger.debug(f"Version {__version__} requested")
        ctx.exit()

    if ctx.invoked_subcommand is None:
        console = Console()
        with console.status("Starting Dasshh 🗲 ", spinner="dots"):
            time.sleep(1.2)
            console.clear()
            from dasshh.ui.app import Dasshh

        app = Dasshh()
        app.run()


@main.command()
def init_config():
    """Initialize the configuration file."""
    load_config()
    click.echo(f"Config file created at: {DEFAULT_CONFIG_PATH}")
    click.echo("Please edit this file to set your model API key before starting the application.")


if __name__ == "__main__":
    main()
