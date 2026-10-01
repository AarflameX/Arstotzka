"""Mocked tool environments for the three scenarios."""

from .email_assistant import EmailEnvironment
from .research_assistant import ResearchEnvironment
from .support_agent import SupportEnvironment

__all__ = ["EmailEnvironment", "ResearchEnvironment", "SupportEnvironment"]