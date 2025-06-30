from pathlib import Path
from typing import List
import typer
from automation_db.models import CodeStyle
from automation_db.crud import CodeStyleCRUD


def code_style_app(db_path: Path) -> typer.Typer:
    app = typer.Typer()
    crud = CodeStyleCRUD(db_path)

    def create(reqs: List[str]) -> None:
        code_style = CodeStyle(requirements=reqs)
        created = crud.create(code_style)
        if created:
            typer.echo("Successfully created code style configuration.")
        else:
            typer.echo("Failed to create code style configuration.", err=True)

    def read() -> None:
        code_style = crud.read()
        if code_style:
            typer.echo(f"\nCode Style: {', '.join(code_style.requirements)}\n")
        else:
            typer.echo("No code style configuration found.", err=True)

    def add(requirement: str) -> None:
        added = crud.add_requirement(requirement)
        if added:
            typer.echo("Successfully added requirement to code style config.")
        else:
            typer.echo("Failed to add requirement.", err=True)

    def remove(requirement: str) -> None:
        removed = crud.remove_requirement(requirement)
        if removed:
            typer.echo("Successfully removed requirement from code style config.")
        else:
            typer.echo("Failed to remove requirement; it may not exist.", err=True)

    def update(old: str, new: str) -> None:
        updated = crud.update_requirement(old, new)
        if updated:
            typer.echo("Successfully updated requirement in code style config.")
        else:
            typer.echo("Failed to update requirement; old requirement may not exist.", err=True)

    app.command()(create)
    app.command()(read)
    app.command()(add)
    app.command()(remove)
    app.command()(update)

    return app