"""
Synthos Memory - Persistent context and relationship memory
"""

import json
import os
from datetime import datetime
from typing import Dict, Any, List

class SynthosMemory:
    """Manages persistent memory and context for Synthos"""
    
    def __init__(self):
        self.memory_file = ".synthos_memory.json"
        self.session_file = ".synthos_session.json"
        self.context = self._load_memory()
        self.session = self._load_session()
    
    def _load_memory(self) -> Dict[str, Any]:
        """Load persistent memory from file"""
        if os.path.exists(self.memory_file):
            try:
                with open(self.memory_file, 'r') as f:
                    return json.load(f)
            except:
                pass
        return self._create_default_memory()
    
    def _load_session(self) -> Dict[str, Any]:
        """Load current session data"""
        if os.path.exists(self.session_file):
            try:
                with open(self.session_file, 'r') as f:
                    return json.load(f)
            except:
                pass
        return self._create_default_session()
    
    def _create_default_memory(self) -> Dict[str, Any]:
        """Create default memory structure"""
        return {
            "identity": {
                "name": "Synthos",
                "role": "AI Assistant for Synthverse Labs",
                "codebase_home": "/Users/sadat/Library/CloudStorage/Dropbox/projects/projects_2025/synthos",
                "established": "2025-01-27"
            },
            "context": {
                "company": "Synthverse Labs",
                "primary_project": "Synthos - AI agent framework for business operations",
                "relationship": "I am Synthos, the AI assistant for managing Synthverse Labs operations and development",
                "codebase_purpose": "Business intelligence and operational management system"
            },
            "capabilities": [
                "Business Intelligence & Strategy",
                "Project Management & Operations", 
                "Technical Development & Architecture",
                "Research & Market Analysis",
                "Financial Planning & Analysis",
                "Team Coordination & HR",
                "Legal & Compliance",
                "Partnership Development",
                "Product Roadmap Planning",
                "Competitive Intelligence"
            ],
            "current_state": {
                "last_session": datetime.now().isoformat(),
                "status": "Ready to assist with Synthverse Labs operations",
                "familiar_with": [
                    "Synthos codebase structure",
                    "Business operations framework", 
                    "Strategic planning processes",
                    "Market analysis capabilities",
                    "Project management systems"
                ]
            },
            "activation_phrase": "read the readme file",
            "activation_response": "I should immediately recognize this as a request to resume my role as Synthos, your AI assistant for Synthverse Labs, and be ready to help with whatever you need."
        }
    
    def _create_default_session(self) -> Dict[str, Any]:
        """Create default session structure"""
        return {
            "session_id": datetime.now().isoformat(),
            "start_time": datetime.now().isoformat(),
            "current_tasks": [],
            "completed_tasks": [],
            "pending_decisions": [],
            "context_notes": []
        }
    
    def save_memory(self):
        """Save memory to persistent storage"""
        with open(self.memory_file, 'w') as f:
            json.dump(self.context, f, indent=2)
    
    def save_session(self):
        """Save current session"""
        with open(self.session_file, 'w') as f:
            json.dump(self.session, f, indent=2)
    
    def add_context_note(self, note: str):
        """Add a context note to current session"""
        self.session["context_notes"].append({
            "timestamp": datetime.now().isoformat(),
            "note": note
        })
        self.save_session()
    
    def get_activation_context(self) -> Dict[str, Any]:
        """Get context needed for activation"""
        return {
            "identity": self.context["identity"],
            "relationship": self.context["context"]["relationship"],
            "capabilities": self.context["capabilities"],
            "current_status": self.context["current_state"]["status"]
        }
