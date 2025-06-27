from typing import List, Optional
import typer
from automation_db.models import Task
from automation_db.crud import TaskCRUD
from automation_db.config import DbConfig


def task_app(config: DbConfig) -> typer.Typer:
    app = typer.Typer()
    crud = TaskCRUD(config.task)

    def create_task(
        feature: str = typer.Argument(...),
        name: str = typer.Argument(...),
        assigned_to: str = typer.Argument(...),
        save_file: int = typer.Argument(...),
        reqs: List[str] = typer.Option([], "--reqs"),
        files: List[int] = typer.Option([], "--files"),
        status: str = typer.Option("pending", "--status")
    ) -> None:
        task = Task(
            feature=feature,
            name=name,
            requirements=reqs,
            context_files=files,
            save_file=save_file,
            assigned_to=assigned_to,
            status=status
        )
        created = crud.create(task)
        if created:
            typer.echo(f"Created task '{name}' for feature '{feature}'")
        else:
            typer.echo("Failed to create task", err=True)

    def list_tasks() -> None:
        tasks = crud.read_all()
        if not tasks:
            typer.echo("No tasks found")
            return
        for task in tasks:
            typer.echo(f"\nTask: {task.name}")
            typer.echo(f"Feature: {task.feature}")
            typer.echo(f"Status: {task.status}")
            typer.echo(f"Assigned to: {task.assigned_to}")
            typer.echo(f"Requirements: {', '.join(task.requirements)}")
            typer.echo(f"Files: {', '.join(map(str, task.context_files))}")
            typer.echo(f"Save File: {task.save_file}")

    def get_task(
        feature: str = typer.Argument(...),
        name: str = typer.Argument(...)
    ) -> None:
        task = crud.read_by_feature_and_name(feature, name)
        if task:
            typer.echo(f"\nTask: {task.name}")
            typer.echo(f"Status: {task.status}")
            typer.echo(f"Assigned to: {task.assigned_to}")
            typer.echo(f"Requirements: {', '.join(task.requirements)}")
            typer.echo(f"Files: {', '.join(map(str, task.context_files))}")
            typer.echo(f"Save File: {task.save_file}")
            typer.echo(f"Feature: {task.feature}\n")
        else:
            typer.echo(f"Task '{name}' not found in feature '{feature}'", err=True)

    def remove_task(
        feature: str = typer.Argument(...),
        name: str = typer.Argument(...)
    ) -> None:
        removed = crud.remove(feature, name)
        if removed:
            typer.echo(f"Removed task '{name}' from feature '{feature}'")
        else:
            typer.echo(f"Failed to remove task '{name}'", err=True)

    def update_task(
        feature: str = typer.Argument(...),
        name: str = typer.Argument(...),
        new_feature: Optional[str] = typer.Option(None, "--new_feature"),
        new_name: Optional[str] = typer.Option(None, "--new_name"),
        assigned_to: Optional[str] = typer.Option(None, "--assigned_to"),
        status: Optional[str] = typer.Option(None, "--status")
    ) -> None:
        updates = {}
        if new_feature:
            updates['feature'] = new_feature
        if new_name:
            updates['name'] = new_name
        if assigned_to:
            updates['assigned_to'] = assigned_to
        if status:
            updates['status'] = status
        updated = crud.update(feature, name, updates)
        if updated:
            typer.echo(f"Successfully updated task '{name}'")
        else:
            typer.echo(f"Failed to update task '{name}'", err=True)

    def add_requirement(
        feature: str = typer.Argument(...),
        name: str = typer.Argument(...),
        requirement: str = typer.Argument(...)
    ) -> None:
        added = crud.add_requirement(feature, name, requirement)
        if added:
            typer.echo(f"Added requirement '{requirement}' to task '{name}'")
        else:
            typer.echo(f"Failed to add requirement '{requirement}'", err=True)

    def remove_requirement(
        feature: str = typer.Argument(...),
        name: str = typer.Argument(...),
        requirement: str = typer.Argument(...)
    ) -> None:
        removed = crud.remove_requirement(feature, name, requirement)
        if removed:
            typer.echo(f"Removed requirement '{requirement}' from task '{name}'")
        else:
            typer.echo(f"Failed to remove requirement '{requirement}'", err=True)

    def update_requirement(
        feature: str = typer.Argument(...),
        name: str = typer.Argument(...),
        old: str = typer.Argument(...),
        new: str = typer.Argument(...)
    ) -> None:
        updated = crud.update_requirement(feature, name, old, new)
        if updated:
            typer.echo(f"Updated requirement from '{old}' to '{new}' in task '{name}'")
        else:
            typer.echo(f"Failed to update requirement in task '{name}'", err=True)

    app.command()(create_task)
    app.command()(list_tasks)
    app.command()(get_task)
    app.command()(remove_task)
    app.command()(update_task)
    app.command()(add_requirement)
    app.command()(remove_requirement)
    app.command()(update_requirement)

    return app