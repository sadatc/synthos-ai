"""
Synthos AI - Your Business Intelligence Assistant for Synthverse Labs

This is the core module for Synthos, your dedicated AI assistant designed to manage
and optimize all aspects of Synthverse Labs operations.

Activation: Simply say "read the readme file" to summon Synthos
"""

__version__ = "1.0.0"
__author__ = "Synthverse Labs"
__description__ = "AI Assistant for Synthverse Labs Business Operations"

from .core.identity import SynthosIdentity
from .memory.context import SynthosMemory
from .protocols.activation import ActivationProtocol

# Initialize Synthos when imported
identity = SynthosIdentity()
memory = SynthosMemory()
activation = ActivationProtocol()

def activate():
    """Activate Synthos AI assistant"""
    return activation.initialize(identity, memory)
