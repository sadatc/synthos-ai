"""
Synthos Activation Protocol - Handles activation and initialization
"""

from typing import Dict, Any

class ActivationProtocol:
    """Manages Synthos activation and initialization"""
    
    def __init__(self):
        self.activation_phrases = [
            "read the readme file",
            "activate synthos",
            "synthos, are you there?",
            "resume synthos"
        ]
        self.is_active = False
    
    def initialize(self, identity, memory):
        """Initialize Synthos with identity and memory"""
        self.is_active = True
        context = memory.get_activation_context()
        
        return {
            "status": "activated",
            "identity": identity.get_identity_summary(),
            "context": context,
            "message": f"Hello! I'm {identity.name}, your AI assistant for {identity.company}. I'm ready to help with whatever Synthverse Labs needs."
        }
    
    def check_activation_phrase(self, phrase: str) -> bool:
        """Check if phrase should activate Synthos"""
        return phrase.lower().strip() in self.activation_phrases
    
    def get_activation_response(self) -> str:
        """Get standard activation response"""
        return "I'm Synthos, your AI assistant for Synthverse Labs. I'm ready to help with business operations, strategy, development, or whatever you need."
