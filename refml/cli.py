import click


@click.group()
def cli():
    pass


@cli.command()
def do_it():
    """Do something..."""
    click.echo("You did it!")
    import os
    dirname = os.path.dirname(__file__)
    filename = os.path.join(dirname, 'apps/refml_app.py')
    os.system('streamlit run ' + filename)