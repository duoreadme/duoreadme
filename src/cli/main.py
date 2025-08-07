"""
Main CLI entry module

Provides the main entry point for the command line interface.
"""

import click
from .commands import gen_command, config_command, trans_command, set_command, export_command


@click.group()
@click.version_option(version="1.0.0", prog_name="DuoReadme")
def cli():
    """
    DuoReadme - Multi-language README generation tool
    
    A powerful CLI tool for automatically generating multi-language README documents from project code and README files.
    """
    pass


# Add all subcommands
cli.add_command(gen_command, name="gen")
cli.add_command(trans_command, name="trans")
cli.add_command(config_command, name="config")
cli.add_command(set_command, name="set")
cli.add_command(export_command, name="export")


def main():
    """Main function - CLI entry point"""
    cli()


if __name__ == "__main__":
    main() 