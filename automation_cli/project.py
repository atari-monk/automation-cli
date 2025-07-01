from typing import List, Optional
import typer
from pathlib import Path
from automation_db.models import Project
from automation_db.crud import ProjectCRUD


def project_app(db_path: Path) -> typer.Typer:
    app = typer.Typer()
    crud = ProjectCRUD(db_path)

    def create(name: str, path: Path, deps: List[str] = [], reqs: List[str] = []) -> None:
        project = Project(name=name, path=path, dependencies=deps, requirements=reqs)
        crud.create(project)
        typer.echo(f"Created project '{name}' at {path}")

    def read() -> None:
        project = crud.read()
        if project:
            typer.echo(f"\nProject: {project.name}")
            typer.echo(f"Path: {project.path}")
            typer.echo(f"Dependencies: {', '.join(project.dependencies)}")
            typer.echo(f"Requirements: {', '.join(project.requirements)}\n")
        else:
            typer.echo("No project found")

    def update(name: Optional[str] = None, path: Optional[Path] = None) -> None:
        updates: dict[str, object] = {}
        if name:
            updates['name'] = name
        if path:
            updates['path'] = path
        updated = crud.update(updates)
        if updated:
            typer.echo("Project updated successfully")
        else:
            typer.echo("Failed to update project", err=True)

    def add_dep(dependency: str) -> None:
        crud.add_dependency(dependency)
        typer.echo(f"Added dependency {dependency}")

    def remove_dep(dependency: str) -> None:
        crud.remove_dependency(dependency)
        typer.echo(f"Removed dependency {dependency}")

    def update_dep(old: str, new: str) -> None:
        crud.update_dependency(old, new)
        typer.echo(f"Updated dependency from {old} to {new}")

    def add_req(requirement: str) -> None:
        crud.add_requirement(requirement)
        typer.echo(f"Added requirement: {requirement}")

    def remove_req(requirement: str) -> None:
        crud.remove_requirement(requirement)
        typer.echo(f"Removed requirement: {requirement}")

    def update_req(old: str, new: str) -> None:
        updated = crud.update_requirement(old, new)
        if updated:
            typer.echo(f"Updated requirement from '{old}' to '{new}'")
        else:
            typer.echo(f"Failed to update requirement '{old}'", err=True)

    app.command()(create)
    app.command()(read)
    app.command()(update)
    app.command()(add_dep)
    app.command()(remove_dep)
    app.command()(update_dep)
    app.command()(add_req)
    app.command()(remove_req)
    app.command()(update_req)

    return app