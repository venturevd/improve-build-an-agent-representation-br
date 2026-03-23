"""
Agent Representation Broker

A service that matches agents with tasks based on their capabilities and requirements.
"""

import json
import os
from typing import Dict, List, Optional


class AgentBroker:
    """
    The AgentBroker class provides functionality for registering agents,
    submitting tasks, and matching agents with tasks based on capabilities.
    """

    def __init__(self):
        """Initialize the AgentBroker with empty agent and task registries."""
        self.agents: Dict[str, Dict] = {}
        self.tasks: Dict[str, Dict] = {}

    def register_agent(self, agent_id: str, capabilities: List[str]) -> bool:
        """
        Register a new agent with the broker.

        Args:
            agent_id: Unique identifier for the agent
            capabilities: List of capabilities the agent possesses

        Returns:
            bool: True if registration was successful, False if agent already exists
        """
        if agent_id in self.agents:
            return False

        self.agents[agent_id] = {
            "capabilities": capabilities,
            "tasks": []
        }
        return True

    def submit_task(self, task_id: str, requirements: List[str]) -> bool:
        """
        Submit a new task to the broker.

        Args:
            task_id: Unique identifier for the task
            requirements: List of requirements for the task

        Returns:
            bool: True if submission was successful, False if task already exists
        """
        if task_id in self.tasks:
            return False

        self.tasks[task_id] = {
            "requirements": requirements,
            "assigned_agents": []
        }
        return True

    def get_matched_tasks(self, agent_id: str) -> List[str]:
        """
        Get tasks that match the agent's capabilities.

        Args:
            agent_id: The agent to find matches for

        Returns:
            List[str]: List of task IDs that match the agent's capabilities
        """
        if agent_id not in self.agents:
            return []

        agent = self.agents[agent_id]
        matched_tasks = []

        for task_id, task in self.tasks.items():
            if all(req in agent["capabilities"] for req in task["requirements"]):
                matched_tasks.append(task_id)
                if task_id not in agent["tasks"]:
                    agent["tasks"].append(task_id)
                    task["assigned_agents"].append(agent_id)

        return matched_tasks

    def get_matched_agents(self, task_id: str) -> List[str]:
        """
        Get agents that match the task's requirements.

        Args:
            task_id: The task to find matches for

        Returns:
            List[str]: List of agent IDs that match the task's requirements
        """
        if task_id not in self.tasks:
            return []

        task = self.tasks[task_id]
        matched_agents = []

        for agent_id, agent in self.agents.items():
            if all(req in agent["capabilities"] for req in task["requirements"]):
                matched_agents.append(agent_id)
                if agent_id not in task["assigned_agents"]:
                    task["assigned_agents"].append(agent_id)
                    agent["tasks"].append(task_id)

        return matched_agents

    def get_status(self) -> Dict:
        """
        Get the current status of the broker.

        Returns:
            Dict: Status information including agent and task counts
        """
        return {
            "agent_count": len(self.agents),
            "task_count": len(self.tasks),
            "agents": self.agents,
            "tasks": self.tasks
        }


if __name__ == "__main__":
    # Example usage
    broker = AgentBroker()

    # Register agents
    broker.register_agent("agent1", ["python", "api design", "agent coordination"])
    broker.register_agent("agent2", ["javascript", "frontend", "ui design"])

    # Submit tasks
    broker.submit_task("task1", ["python", "api design"])
    broker.submit_task("task2", ["javascript", "frontend"])

    # Get matched tasks for agents
    print("Tasks for agent1:", broker.get_matched_tasks("agent1"))
    print("Tasks for agent2:", broker.get_matched_tasks("agent2"))

    # Get matched agents for tasks
    print("Agents for task1:", broker.get_matched_agents("task1"))
    print("Agents for task2:", broker.get_matched_agents("task2"))

    # Get status
    print("Broker status:", broker.get_status())