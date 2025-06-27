from pathlib import Path
import typer
from automation_db.config import get_config
from automation_cli.agent import agent_app
from automation_cli.code_style import code_style_app
from automation_cli.feature import feature_app
from automation_cli.file import file_app
from automation_cli.project import project_app
from automation_cli.task import task_app


def create_app() -> typer.Typer:
    app = typer.Typer()
    config = get_config(Path(r"C:\atari-monk\code\automation_db_test"))
    app.add_typer(agent_app(config), name="agent")
    app.add_typer(code_style_app(config), name="code_style")
    app.add_typer(feature_app(config), name="feature")
    app.add_typer(file_app(config), name="file")
    app.add_typer(project_app(config), name="project")
    app.add_typer(task_app(config), name="task")
    return app

def main():
    app = create_app()
    app()

if __name__ == "__main__":
    main()