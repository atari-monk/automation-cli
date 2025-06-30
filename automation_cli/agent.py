from pathlib import Path
from typing import List
import typer
from automation_db.models import Agent
from automation_db.crud import AgentCRUD


def agent_app(db_path: Path) -> typer.Typer:
    app = typer.Typer()
    crud = AgentCRUD(db_path)

    def create(role: str, reqs: List[str]) -> None:
        """Create a new agent"""
        agent = Agent(role=role, requirements=reqs)
        crud.create(agent)

    def list() -> None:
        """List all agents"""
        agents = crud.read_all()
        if not agents:
            typer.echo("No agents found.")
            return
                
        for i, agent in enumerate(agents, 1):
            typer.echo(f"\nAgent {i}: {agent.role}")
            typer.echo(f"Requirements: {', '.join(agent.requirements)}")

    def get(role: str) -> None:
        """Get agent by role"""
        agent = crud.read_by_role(role)
        if agent:
            typer.echo("Current agent:")
            typer.echo(f"Role: {agent.role}")
            typer.echo(f"Requirements: {', '.join(agent.requirements)}")
        else:
            typer.echo(f"No agent found with role: {role}", err=True)

    def remove(role: str) -> None:
        """Remove agent by role"""
        removed = crud.remove(role)
        if removed:
            typer.echo(f"Successfully removed agent with role: {role}")
        else:
            typer.echo(f"No agent found with role: {role}. Nothing removed.", err=True)

    def update(role: str, new_role: str) -> None:
        """Update agent's role"""
        updates = {'role': new_role}
        updated = crud.update(role, updates)
        if updated:
            typer.echo(f"Successfully updated agent with role '{role}' to '{new_role}'")
        else:
            typer.echo(f"No agent found with role '{role}'. Nothing was updated.", err=True)

    def add_req(role: str, requirement: str) -> None:
        """Add a requirement to an agent"""
        added = crud.add_requirement(role, requirement)
        if added:
            typer.echo(f"Successfully added requirement to agent '{role}'")
        else:
            typer.echo(f"Failed to add requirement. Agent with role '{role}' not found.", err=True)

    def remove_req(role: str, requirement: str) -> None:
        """Remove a requirement from an agent"""
        removed = crud.remove_requirement(role, requirement)
        if removed:
            typer.echo(f"Successfully removed requirement from agent '{role}'.")
        else:
            typer.echo(f"Failed to remove requirement; either agent '{role}' or requirement not found.", err=True)

    def update_req(role: str, old: str, new: str) -> None:
        """Update a requirement for an agent"""
        updated = crud.update_requirement(role, old, new)
        if updated:
            typer.echo(f"Successfully updated requirement for agent '{role}'.")
        else:
            typer.echo(f"Failed to update requirement; agent '{role}' or old requirement may not exist.", err=True)

    app.command()(create)
    app.command()(list)
    app.command()(get)
    app.command()(remove)
    app.command()(update)
    app.command()(add_req)
    app.command()(remove_req)
    app.command()(update_req)

    return app