import click
from dishka import FromDishka
from dishka.integrations.click import inject

from lumen.application.dtos import AddNoteCommand
from lumen.application.use_cases import AddNoteInteractor
from lumen.presentation.cli.utils import handle_failure, process_result, void


@click.group()
def notes():
    """Commands for managing notes."""
    pass


@notes.command(name="add")
@click.argument("text")
@click.option("--mood", "-m", multiple=True, help="Mood associated with the note.")
@inject
def add_note(
    text: str,
    mood: list[str],
    interactor: FromDishka[AddNoteInteractor],
) -> None:
    """Create a new note and retrieve resonating wisdom.

    This command persists your state and immediately returns quotes that
    semantically align with your entry, creating a reflective dialogue.

    Args:
        text: The content of your note or experience.
        mood: Optional emotional keywords or tags.
        interactor: The application service for note persistence and resonance search.
    """
    command = AddNoteCommand(text=text, moods=list(mood))
    result = interactor.execute(command)

    return process_result(
        result=result,
        on_success=lambda quotes: void(
            (
                click.secho("Запис збережено.", fg="green"),
                [
                    (
                        click.echo(click.style(f'"{q.text}"', fg="white", italic=True)),
                        click.echo(
                            click.style(f"  — {q.author}", fg="cyan", bold=True)
                        ),
                        click.echo(),
                    )
                    for q in quotes
                ]
                if quotes
                else None,
            )
        ),
        on_failure=handle_failure,
    )
