from pathlib import Path
import typer
from automation_cli.agent import agent_app
from automation_cli.code_style import code_style_app
from automation_cli.feature import feature_app
from automation_cli.project import project_app
from automation_cli.task import task_app


def create_app(db_path: Path) -> typer.Typer:
    app = typer.Typer()
    app.add_typer(agent_app(db_path), name="agent")
    app.add_typer(code_style_app(db_path), name="code_style")
    app.add_typer(feature_app(db_path), name="feature")
    app.add_typer(project_app(db_path), name="project")
    app.add_typer(task_app(db_path), name="task")
    return app


def main(db_path: Path | None = typer.Option(None, "--db-path", "-d")):
    if db_path is None:
        db_path = typer.prompt("Enter database directory path")
    if db_path is None:
        print('Exiting. No path provided.')
        return
    path = Path(db_path).absolute()
    if not path.exists():
        path.mkdir(parents=True)
    
    app = create_app(path)
    app()


if __name__ == "__main__":
    typer.run(main)