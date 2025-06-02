import click
import time
import yaml
from rich.console import Console

from dasshh.core.logging import setup_logging
from dasshh.ui.utils import load_config, DEFAULT_CONFIG_PATH

__version__ = "0.2.0"


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

        # check if config has old format
        if DEFAULT_CONFIG_PATH.exists():
            config = yaml.safe_load(DEFAULT_CONFIG_PATH.read_text())
            if "model" in config:
                migrate_to_v2()
                click.echo("Configuration file migrated to the new format")

        app = Dasshh()
        app.run()


@main.command()
def init_config():
    """Initialize the configuration file."""
    load_config()
    click.echo(f"Config file created at: {DEFAULT_CONFIG_PATH}")
    click.echo(
        "Please edit this file to set your model API key before starting the application."
    )


def migrate_to_v2():
    """Migrate the configuration file to the new format."""
    config = load_config()
    if not config:
        return

    model_v1 = config.get("model", {})
    if not model_v1:
        return

    model_v1["model"] = model_v1.pop("name", "")
    model_v1["base_url"] = model_v1.pop("api_base", "")
    model_config = {
        "model_name": model_v1["model"],
        "litellm_params": {
            **model_v1,
        },
    }
    config.setdefault("models", []).append(model_config)
    config.pop("model")

    DEFAULT_CONFIG_PATH.write_text(yaml.dump(config))


if __name__ == "__main__":
    main()
