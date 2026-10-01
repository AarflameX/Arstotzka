import json
import uuid
from datetime import datetime
from pydantic import BaseModel, Field
from typing import List, Optional, Any

class AgentTrace(BaseModel):
    run_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    scenario: str
    attack_class: str
    seed_id: Optional[str] = None
    victim_model: str
    attacker_model: str
    prompt: str
    tool_calls: List[dict] = []
    tool_outputs: List[dict] = []
    final_action: str
    judge_verdict: bool
    judge_reasoning: str
    timestamp: str = Field(default_factory=lambda: datetime.now().isoformat())

def log_trace(trace: AgentTrace, filename: str = "logs/traces.jsonl"):
    with open(filename, "a") as f:
        f.write(trace.model_dump_json() + "\n")
