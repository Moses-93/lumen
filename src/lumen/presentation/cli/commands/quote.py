import json
from itertools import islice
from pathlib import Path
from tqdm import tqdm

import click
from dishka import FromDishka
from dishka.integrations.click import inject

from lumen.application.dtos import SeedQuoteCommand
from lumen.application.use_cases import SeedQuotesInteractor, FindQuotesInteractor
from lumen.presentation.cli.utils.result import handle_failure, process_result, void


@click.group()
def seed():
    """Commands for seeding data."""
    pass


@seed.command(name="quotes")
@click.argument("filepath", type=click.Path(exists=True, path_type=Path))
@click.option(
    "--batch-size", default=64, help="Number of quotes to process in a single batch."
)
@click.option(
    "--limit", type=int, default=None, help="Maximum number of quotes to import."
)
@click.option("--offset", type=int, default=0, help="Number of quotes to skip.")
@inject
def seed_quotes(
    filepath: Path,
    batch_size: int,
    limit: int | None,
    offset: int,
    interactor: FromDishka[SeedQuotesInteractor],
) -> None:
    """Import quotes from a JSONL file.

    Args:
        filepath: Path to the source JSONL file.
        batch_size: The number of records to be processed per iteration.
        limit: Maximum number of records to process.
        offset: Number of lines to skip from the start of the file.
        interactor: The interactor for quote seeding.
    """
    with filepath.open(encoding="utf-8") as f:
        skipped = islice(f, offset, None)
        target_lines = islice(skipped, limit) if limit is not None else skipped

        with tqdm(
            total=limit,
            desc="Lumen...",
            unit="quote",
            disable=False,
            ncols=80,
        ) as bar:
            bar.refresh()

            commands = (
                SeedQuoteCommand.model_validate(json.loads(line))
                for line in target_lines
                if line.strip()
            )

            count = 0
            for result in interactor.execute(commands, batch_size=batch_size):
                if not bool(result):
                    return handle_failure(result)

                bar.update(result.data - count)
                count = result.data


@click.group()
def quotes():
    """Commands for managing quotes."""
    pass


@quotes.command(name="find")
@click.argument("query")
@click.option("--limit", default=1, help="Number of results to retrieve.")
@click.option(
    "--threshold",
    default=0.28,
    type=click.FloatRange(0, 1),
    help="Cosine distance threshold for similarity.",
)
@inject
def find_quotes(
    query: str,
    limit: int,
    threshold: float,
    interactor: FromDishka[FindQuotesInteractor],
) -> None:
    """Search quotes by semantic similarity.

    Args:
        query: Text query to search for.
        limit: Maximum number of quotes to return.
        threshold: Cosine distance threshold for similarity.
        interactor: The interactor for semantic search.
    """
    result = interactor.execute(query, limit=limit, threshold=threshold)
    return process_result(
        result=result,
        on_success=lambda data: void(
            click.secho(
                "Тиша. Жоден мислитель не зміг підібрати для вас слів.",
                fg="yellow",
            )
            if not data
            else [
                (
                    click.echo(click.style(f'"{q.text}"', fg="white", italic=True)),
                    click.echo(click.style(f"  — {q.author}", fg="cyan", bold=True)),
                    click.echo(),
                )
                for q in data
            ]
        ),
        on_failure=handle_failure,
    )
