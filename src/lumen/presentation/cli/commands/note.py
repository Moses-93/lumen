from datetime import datetime

import click
from dishka import FromDishka
from dishka.integrations.click import inject

from lumen.application.dtos import (
    AddNoteCommand,
    FindSimilarNotesQuery,
    GetNotesQuery,
)
from lumen.application.use_cases import (
    AddNoteInteractor,
    FindSimilarNotesInteractor,
    GetNotesInteractor,
)
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


@notes.command(name="show")
@click.option(
    "--from", "from_date", type=click.DateTime(), help="Start date (ISO8601)."
)
@click.option("--to", "to_date", type=click.DateTime(), help="End date (ISO8601).")
@click.option(
    "--limit", "-l", type=int, default=10, help="Maximum number of notes to display."
)
@inject
def show_notes(
    from_date: datetime | None,
    to_date: datetime | None,
    limit: int,
    interactor: FromDishka[GetNotesInteractor],
) -> None:
    """Display saved notes.

    Retrieves and displays chronologically ordered notes within the specified
    timeframe, serving as a chronological view of the user's recorded states.

    Args:
        from_date: Optional start date for filtering notes.
        to_date: Optional end date for filtering notes.
        limit: The maximum number of notes to display.
        interactor: The application service for note retrieval.
    """
    query = GetNotesQuery(
        limit=limit,
        from_date=from_date,
        to_date=to_date,
    )
    result = interactor.execute(query)

    return process_result(
        result=result,
        on_success=lambda notes_list: void(
            [
                (
                    click.echo(
                        click.style(
                            f"[{n.created_at.isoformat(sep=' ', timespec='minutes')}]",
                            fg="yellow",
                        )
                    ),
                    click.echo(click.style(n.text, fg="white")),
                    click.echo(
                        click.style(
                            f"Moods: {', '.join(n.moods)}", fg="cyan", italic=True
                        )
                    )
                    if n.moods
                    else None,
                    click.echo("-" * 40),
                )
                for n in notes_list
            ]
            if notes_list
            else click.secho("Записів не знайдено.", fg="yellow")
        ),
        on_failure=handle_failure,
    )


@notes.command(name="similar")
@click.argument("text")
@click.option(
    "--limit",
    "-l",
    type=int,
    default=5,
    help="Maximum number of similar notes to return.",
)
@click.option(
    "--threshold", "-t", type=float, default=0.28, help="Similarity threshold."
)
@click.option(
    "--from", "from_date", type=click.DateTime(), help="Start date (ISO8601)."
)
@click.option("--to", "to_date", type=click.DateTime(), help="End date (ISO8601).")
@inject
def similar_notes(
    text: str,
    limit: int,
    threshold: float,
    from_date: datetime | None,
    to_date: datetime | None,
    interactor: FromDishka[FindSimilarNotesInteractor],
) -> None:
    """Find notes similar to a given mood or state.

    Performs a semantic search against previously recorded notes to find
    entries that resonate with the provided query, helping to identify
    recurring emotional patterns.

    Args:
        text: The mood, feeling, or state to search for.
        limit: The maximum number of similar notes to return.
        threshold: The cosine distance threshold for semantic similarity.
        from_date: Optional start date for filtering notes.
        to_date: Optional end date for filtering notes.
        interactor: The application service for semantic note search.
    """
    query = FindSimilarNotesQuery(
        text=text,
        limit=limit,
        threshold=threshold,
        from_date=from_date,
        to_date=to_date,
    )
    result = interactor.execute(query)

    return process_result(
        result=result,
        on_success=lambda notes_list: void(
            [
                (
                    click.echo(
                        click.style(
                            f"[{n.created_at.isoformat(sep=' ', timespec='minutes')}]",
                            fg="yellow",
                        )
                    ),
                    click.echo(click.style(n.text, fg="white")),
                    click.echo(
                        click.style(
                            f"Moods: {', '.join(n.moods)}", fg="cyan", italic=True
                        )
                    )
                    if n.moods
                    else None,
                    click.echo("-" * 40),
                )
                for n in notes_list
            ]
            if notes_list
            else click.secho("Схожих записів не знайдено.", fg="yellow")
        ),
        on_failure=handle_failure,
    )
