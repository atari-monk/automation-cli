from typing import Optional
import typer
from automation_db.models import File
from automation_db.crud import FileCRUD
from automation_db.config import DbConfig


def file_app(config: DbConfig) -> typer.Typer:
    app = typer.Typer()
    crud = FileCRUD(config.file)

    def create(id: str, feature: str, task: str, file_name: str, path: str, class_name: Optional[str] = None) -> None:
        feature_file = File(
            id=int(id),
            feature=feature,
            task=task,
            file_name=file_name,
            class_name=class_name,
            path=path
        )
        created = crud.create(feature_file)
        if created:
            typer.echo(f"Successfully created feature file '{file_name}'.")
        else:
            typer.echo(f"Failed to create feature file '{file_name}'.")

    def list_all() -> None:
        files = crud.read_all()
        if not files:
            typer.echo("No files found.")
            return
        for i, file in enumerate(files, 1):
            typer.echo(f"\nFile {i}:")
            typer.echo(f"  ID: {file.id}")
            typer.echo(f"  File Name: {file.file_name}")
            typer.echo(f"  Class Name: {file.class_name or 'N/A'}")
            typer.echo(f"  Path: {file.path}")
            typer.echo(f"  Feature: {file.feature}")
            typer.echo(f"  Task: {file.task}")
        typer.echo()

    def get_by_feature_and_task(feature_name: str, task_name: str) -> None:
        file = crud.read_by_feature_and_task(feature_name, task_name)
        if file:
            typer.echo(f"\nFile name: {file.file_name}")
            typer.echo(f"Class name: {file.class_name or 'N/A'}")
            typer.echo(f"Path: {file.path}")
            typer.echo(f"Feature: {file.feature}")
            typer.echo(f"Task: {file.task}")
            typer.echo(f"Id: {file.id}")
        else:
            typer.echo(f"No file found with feature '{feature_name}' and task '{task_name}'.")

    def remove(feature_name: str, task_name: str) -> None:
        removed = crud.remove(feature_name, task_name)
        if removed:
            typer.echo(f"Successfully removed feature file for feature '{feature_name}' and task '{task_name}'.")
        else:
            typer.echo(f"No feature file found for feature '{feature_name}' and task '{task_name}'.")

    def update(
        feature_name: str,
        task_name: str,
        file_name: Optional[str] = None,
        class_name: Optional[str] = None,
        path: Optional[str] = None
    ) -> None:
        updates: dict[str, str] = {}
        if file_name:
            updates['file_name'] = file_name
        if class_name:
            updates['class_name'] = class_name
        if path:
            updates['path'] = path
        if not updates:
            typer.echo("No updates specified. Please provide at least one field to update.")
            return
        updated = crud.update(feature_name, task_name, updates)
        if updated:
            typer.echo(f"Successfully updated feature file for feature '{feature_name}' and task '{task_name}'.")
        else:
            typer.echo(f"Failed to update feature file for feature '{feature_name}' and task '{task_name}'.")

    app.command()(create)
    app.command()(list_all)
    app.command()(get_by_feature_and_task)
    app.command()(remove)
    app.command()(update)

    return app