from pathlib import Path
from typing import List
import typer
from automation_db.models import Feature
from automation_db.crud import FeatureCRUD


def feature_app(db_path: Path) -> typer.Typer:
    app = typer.Typer()
    crud = FeatureCRUD(db_path)

    def create_feature(name: str, reqs: List[str]) -> None:
        feature = Feature(name=name, requirements=reqs)
        created = crud.create(feature)
        if created:
            typer.echo(f"Successfully created feature '{name}'.")
        else:
            typer.echo(f"Failed to create feature '{name}'. It may already exist or input was invalid.", err=True)

    def list_features() -> None:
        features = crud.read_all()
        if not features:
            typer.echo("No features found.")
            return
        for i, feature in enumerate(features, 1):
            typer.echo(f"\nFeature {i}: {feature.name}")
            typer.echo(f"Requirements: {', '.join(feature.requirements)}")
        typer.echo()

    def get_feature(name: str) -> None:
        feature = crud.read_by_name(name)
        if feature:
            typer.echo(f"Feature: {feature.name}")
            typer.echo(f"Requirements: {', '.join(feature.requirements)}")
        else:
            typer.echo(f"No feature found with name '{name}'.", err=True)

    def remove_feature(name: str) -> None:
        removed = crud.remove(name)
        if removed:
            typer.echo(f"Successfully removed feature '{name}'.")
        else:
            typer.echo(f"Failed to remove feature '{name}'. It may not exist.", err=True)

    def update_feature(name: str, new_name: str = None) -> None: # type: ignore
        updates: dict[str, str] = {}
        if new_name:
            updates['name'] = new_name
        if not updates:
            typer.echo("No updates provided. Use --new-name to rename the feature.", err=True)
            return
        updated = crud.update(name, updates)
        if updated:
            typer.echo(f"Successfully updated feature '{name}'.")
        else:
            typer.echo(f"Failed to update feature '{name}'. It may not exist.", err=True)

    def add_requirement(name: str, requirement: str) -> None:
        added = crud.add_requirement(name, requirement)
        if added:
            typer.echo(f"Successfully added requirement to feature '{name}'.")
        else:
            typer.echo(f"Failed to add requirement. Feature '{name}' may not exist.", err=True)

    def remove_requirement(name: str, requirement: str) -> None:
        removed = crud.remove_requirement(name, requirement)
        if removed:
            typer.echo(f"Successfully removed requirement from feature '{name}'.")
        else:
            typer.echo(f"Failed to remove requirement. Feature '{name}' or requirement may not exist.", err=True)

    def update_requirement(name: str, old: str, new: str) -> None:
        updated = crud.update_requirement(name, old, new)
        if updated:
            typer.echo(f"Successfully updated requirement in feature '{name}'.")
        else:
            typer.echo(f"Failed to update requirement. Feature '{name}' or old requirement may not exist.", err=True)

    app.command()(create_feature)
    app.command()(list_features)
    app.command()(get_feature)
    app.command()(remove_feature)
    app.command()(update_feature)
    app.command()(add_requirement)
    app.command()(remove_requirement)
    app.command()(update_requirement)

    return app