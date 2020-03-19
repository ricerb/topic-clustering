import click


@click.group()
def cli():
    pass


@cli.command()
def do_it():
    """Do something..."""
    click.echo("You did it!")
