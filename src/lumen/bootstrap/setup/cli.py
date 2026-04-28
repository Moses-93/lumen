import click
from dishka.integrations.click import setup_dishka

from lumen.bootstrap.container.main import build_container
from lumen.presentation.cli.commands import commands


@click.group()
@click.pass_context
def cli(ctx: click.Context) -> None:
    app_container = build_container()

    request_container = app_container().__enter__()

    ctx.call_on_close(lambda: request_container.__exit__(None, None, None))
    ctx.call_on_close(lambda: app_container.close())

    setup_dishka(request_container, ctx, auto_inject=True)


for command in commands:
    cli.add_command(command)
