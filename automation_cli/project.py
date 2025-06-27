from typing import List, Optional
import typer
from pathlib import Path
from automation_db.models import Project
from automation_db.crud import ProjectCRUD
from automation_db.config import DbConfig


def project_app(config: DbConfig) -> typer.Typer:
    app = typer.Typer()
    crud = ProjectCRUD(config.project)

    def create_project(name: str, path: Path, deps: List[str] = [], reqs: List[str] = []) -> None:
        project = Project(name=name, path=path, dependencies=deps, requirements=reqs)
        crud.create(project)
        typer.echo(f"Created project '{name}' at {path}")

    def read_project() -> None:
        project = crud.read()
        if project:
            typer.echo(f"\nProject: {project.name}")
            typer.echo(f"Path: {project.path}")
            typer.echo(f"Dependencies: {', '.join(project.dependencies)}")
            typer.echo(f"Requirements: {', '.join(project.requirements)}\n")
        else:
            typer.echo("No project found")

    def update_project(name: Optional[str] = None, path: Optional[Path] = None) -> None:
        updates = {}
        if name:
            updates['name'] = name
        if path:
            updates['path'] = path
        updated = crud.update(updates)
        if updated:
            typer.echo("Project updated successfully")
        else:
            typer.echo("Failed to update project", err=True)

    def add_dependency(dependency: str) -> None:
        crud.add_dependency(dependency)
        typer.echo(f"Added dependency {dependency}")

    def remove_dependency(dependency: str) -> None:
        crud.remove_dependency(dependency)
        typer.echo(f"Removed dependency {dependency}")

    def update_dependency(old: str, new: str) -> None:
        crud.update_dependency(old, new)
        typer.echo(f"Updated dependency from {old} to {new}")

    def add_requirement(requirement: str) -> None:
        crud.add_requirement(requirement)
        typer.echo(f"Added requirement: {requirement}")

    def remove_requirement(requirement: str) -> None:
        crud.remove_requirement(requirement)
        typer.echo(f"Removed requirement: {requirement}")

    def update_requirement(old: str, new: str) -> None:
        updated = crud.update_requirement(old, new)
        if updated:
            typer.echo(f"Updated requirement from '{old}' to '{new}'")
        else:
            typer.echo(f"Failed to update requirement '{old}'", err=True)

    app.command()(create_project)
    app.command()(read_project)
    app.command()(update_project)
    app.command()(add_dependency)
    app.command()(remove_dependency)
    app.command()(update_dependency)
    app.command()(add_requirement)
    app.command()(remove_requirement)
    app.command()(update_requirement)

    return app