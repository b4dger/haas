import click


@click.group()
@click.pass_context
def cli(ctx, **kwargs):
    """Cluster related operations
    """
    ctx.obj = kwargs


@cli.command()
@click.pass_context
def start(ctx):
    pass


@cli.command()
@click.pass_context
def stop(ctx):
    pass


@cli.command()
@click.pass_context
def restart(ctx):
    pass


@cli.command()
@click.pass_context
def status(ctx):
    pass
