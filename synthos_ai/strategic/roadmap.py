"""
Synthos Strategic Roadmap - Strategic planning and roadmap management
"""

from typing import Dict, List, Any
from datetime import datetime, timedelta

class StrategicRoadmap:
    """Manages strategic planning and roadmap for Synthverse Labs"""
    
    def __init__(self):
        self.strategic_goals = []
        self.roadmap_items = []
        self.milestones = []
        self.resources = []
    
    def add_strategic_goal(self, goal: str, description: str, timeframe: str, priority: str):
        """Add strategic goal"""
        goal_entry = {
            "id": len(self.strategic_goals) + 1,
            "goal": goal,
            "description": description,
            "timeframe": timeframe,
            "priority": priority,
            "status": "active",
            "created": datetime.now().isoformat()
        }
        self.strategic_goals.append(goal_entry)
        return goal_entry
    
    def add_roadmap_item(self, item: str, description: str, target_date: str, dependencies: List[str] = None):
        """Add roadmap item"""
        roadmap_entry = {
            "id": len(self.roadmap_items) + 1,
            "item": item,
            "description": description,
            "target_date": target_date,
            "dependencies": dependencies or [],
            "status": "planned",
            "created": datetime.now().isoformat()
        }
        self.roadmap_items.append(roadmap_entry)
        return roadmap_entry
    
    def add_milestone(self, milestone: str, target_date: str, success_criteria: List[str]):
        """Add strategic milestone"""
        milestone_entry = {
            "id": len(self.milestones) + 1,
            "milestone": milestone,
            "target_date": target_date,
            "success_criteria": success_criteria,
            "status": "pending",
            "created": datetime.now().isoformat()
        }
        self.milestones.append(milestone_entry)
        return milestone_entry
    
    def get_roadmap_summary(self) -> Dict[str, Any]:
        """Get roadmap summary"""
        return {
            "strategic_goals": len(self.strategic_goals),
            "roadmap_items": len(self.roadmap_items),
            "milestones": len(self.milestones),
            "upcoming_milestones": [m for m in self.milestones if m["status"] == "pending"][:3],
            "high_priority_goals": [g for g in self.strategic_goals if g["priority"] == "high"]
        }
