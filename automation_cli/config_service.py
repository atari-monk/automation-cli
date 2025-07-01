from pathlib import Path
import toml
import sys
from typing import TypedDict, Dict, cast


class DatabaseConfig(TypedDict):
    selected: str
    available: Dict[str, str]


class ConfigData(TypedDict):
    databases: Dict[str, DatabaseConfig]


def load_config(config_path: Path) -> ConfigData:
    try:
        config = toml.load(config_path)
        if not all(key in config.get("databases", {}) for key in ["shared", "projects"]):
            raise ValueError("Invalid config structure - missing required keys")
        return cast(ConfigData, config)
    except Exception as e:
        print(f"Error loading config: {str(e)}", file=sys.stderr)
        sys.exit(1)


def get_db_paths(config_path: Path) -> tuple[Path, Path]:
    config = load_config(config_path)
    databases = config["databases"]
    
    shared = databases["shared"]
    selected_shared = shared["selected"]
    available_shared = shared["available"]
    
    projects = databases["projects"]
    selected_project = projects["selected"]
    available_projects = projects["available"]
    
    if selected_shared not in available_shared:
        print(f"Error: Selected shared path '{selected_shared}' not found", file=sys.stderr)
        sys.exit(1)
    
    if selected_project not in available_projects:
        print(f"Error: Selected project path '{selected_project}' not found", file=sys.stderr)
        sys.exit(1)
    
    return Path(available_shared[selected_shared]).absolute(), Path(available_projects[selected_project]).absolute()