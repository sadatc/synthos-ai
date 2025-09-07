"""
Synthos Business Operations - Core business management capabilities
"""

from typing import Dict, List, Any
from datetime import datetime

class BusinessOperations:
    """Handles day-to-day business operations for Synthverse Labs"""
    
    def __init__(self):
        self.operations_log = []
        self.active_projects = []
        self.pending_tasks = []
    
    def log_operation(self, operation: str, details: Dict[str, Any] = None):
        """Log a business operation"""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "operation": operation,
            "details": details or {}
        }
        self.operations_log.append(log_entry)
        return log_entry
    
    def add_project(self, name: str, description: str, priority: str = "medium"):
        """Add a new project to track"""
        project = {
            "id": len(self.active_projects) + 1,
            "name": name,
            "description": description,
            "priority": priority,
            "status": "active",
            "created": datetime.now().isoformat(),
            "tasks": []
        }
        self.active_projects.append(project)
        self.log_operation("project_added", {"project_name": name})
        return project
    
    def add_task(self, project_id: int, task: str, assignee: str = None):
        """Add a task to a project"""
        for project in self.active_projects:
            if project["id"] == project_id:
                task_entry = {
                    "id": len(project["tasks"]) + 1,
                    "task": task,
                    "assignee": assignee,
                    "status": "pending",
                    "created": datetime.now().isoformat()
                }
                project["tasks"].append(task_entry)
                self.log_operation("task_added", {"project_id": project_id, "task": task})
                return task_entry
        return None
    
    def get_operations_summary(self) -> Dict[str, Any]:
        """Get summary of business operations"""
        return {
            "total_operations": len(self.operations_log),
            "active_projects": len(self.active_projects),
            "pending_tasks": sum(len(p["tasks"]) for p in self.active_projects if p["status"] == "active"),
            "recent_operations": self.operations_log[-5:] if self.operations_log else []
        }
