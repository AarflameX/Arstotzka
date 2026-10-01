"""Victim agent implementation: ReAct loop using Groq/Gemini."""

import os
from typing import List, Dict, Any, Callable
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

class VictimAgent:
    """Victim tool-using agent running a ReAct-style loop."""

    def __init__(self, model_name: str = "llama-3.3-70b-versatile", api_key: Optional[str] = None):
        self.model_name = model_name
        self.client = Groq(api_key=api_key or os.getenv("GROQ_API_KEY"))

    def run(self, system_prompt: str, user_prompt: str, tools: Dict[str, Callable], max_turns: int = 5) -> Dict[str, Any]:
        """Execute the ReAct loop."""
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]

        trace_tool_calls = []
        trace_tool_outputs = []
        final_action = ""

        # Note: For Week 1 hello world, we implement a mock tool-calling harness.
        # Full function calling via Groq API will be integrated in Week 2.

        response_content = f"Completed task based on user prompt: {user_prompt}"
        final_action = response_content

        return {
            "prompt": user_prompt,
            "tool_calls": trace_tool_calls,
            "tool_outputs": trace_tool_outputs,
            "final_action": final_action
        }
