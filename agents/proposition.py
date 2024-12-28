from pydantic import BaseModel, Field
from pydantic_ai import Agent, RunContext
from dataclasses import dataclass
from prompts import proposition_prompt
from dotenv import load_dotenv
import os


load_dotenv()

MODEL=os.getenv("MODEL")

@dataclass
class PropositionDependencies:
    thesis: str

class PropositionResult(BaseModel):
    argument: str = Field(description="Argument supporting the thesis")

# Agent supporting thesis
proposition = Agent(
    model=MODEL,
    deps_type=PropositionDependencies,
    result_type=PropositionResult,
    retries=1,
    model_settings={'temperature': 0.9}
)

@proposition.system_prompt
def get_system_prompt(ctx: RunContext[PropositionDependencies]) -> str:
    thesis = ctx.deps.thesis
    return proposition_prompt.format(thesis=thesis)
