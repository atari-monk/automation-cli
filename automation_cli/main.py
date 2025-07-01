from pathlib import Path
import typer
import sys
import click
from automation_cli.config_service import get_db_paths
from automation_cli.agent import agent_app
from automation_cli.code_style import code_style_app
from automation_cli.feature import feature_app
from automation_cli.project import project_app
from automation_cli.task import task_app


def create_app(shared_db_path: Path, project_db_path: Path) -> typer.Typer:
    app = typer.Typer()
    
    app.add_typer(agent_app(db_path=shared_db_path), name="agent")
    app.add_typer(code_style_app(db_path=shared_db_path), name="code_style")
    app.add_typer(feature_app(db_path=project_db_path), name="feature")
    app.add_typer(project_app(db_path=project_db_path), name="project")
    app.add_typer(task_app(db_path=project_db_path), name="task")
    
    return app


def main():
    try:
        config_path = Path(r"C:\atari-monk\code\cli\automation-cli\automation_cli\config.toml")
        shared_path, project_path = get_db_paths(config_path)
        shared_path.mkdir(parents=True, exist_ok=True)
        project_path.mkdir(parents=True, exist_ok=True)
        
        app = create_app(shared_path, project_path)
        app()
    except (click.exceptions.Abort, KeyboardInterrupt):
        print("\nOperation cancelled by user.", file=sys.stderr)
        sys.exit(0)
    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()