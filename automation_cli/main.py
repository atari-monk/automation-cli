from pathlib import Path
import typer
import sys
import click
import toml
from automation_cli.agent import agent_app
from automation_cli.code_style import code_style_app
from automation_cli.feature import feature_app
from automation_cli.project import project_app
from automation_cli.task import task_app


def load_config() -> dict[str, dict[str, str]]:
    """Load and validate configuration from TOML file."""
    config_path = Path(r"C:\atari-monk\code\cli\automation-cli\automation_cli\config.toml")
    try:
        config = toml.load(config_path)
        if not all(key in config.get("paths", {}) for key in ["selected", "available"]):
            raise ValueError("Invalid config structure - missing required keys")
        return config
    except Exception as e:
        print(f"Error loading config: {str(e)}", file=sys.stderr)
        sys.exit(1)


def get_db_path() -> Path:
    """Get the database path from configuration."""
    config = load_config()
    paths = config["paths"]
    selected = paths["selected"]
    available = paths["available"]
    
    if selected not in available:
        print(f"Error: Selected path '{selected}' not found in available paths", file=sys.stderr)
        sys.exit(1)
    
    return Path(available[selected]).absolute()


def create_app(db_path: Path) -> typer.Typer:
    """Create the CLI application with all subcommands."""
    app = typer.Typer()
    app.add_typer(agent_app(db_path), name="agent")
    app.add_typer(code_style_app(db_path), name="code_style")
    app.add_typer(feature_app(db_path), name="feature")
    app.add_typer(project_app(db_path), name="project")
    app.add_typer(task_app(db_path), name="task")
    return app


def main():
    """Entry point for the CLI application."""
    try:
        # Get path from config and ensure it exists
        path = get_db_path()
        path.mkdir(parents=True, exist_ok=True)
        
        # Run the app
        app = create_app(path)
        app()
    except (click.exceptions.Abort, KeyboardInterrupt):
        print("\nOperation cancelled by user.", file=sys.stderr)
        sys.exit(0)
    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()