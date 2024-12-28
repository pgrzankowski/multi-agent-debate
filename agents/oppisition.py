from pydantic import BaseModel, Field
from pydantic_ai import Agent, RunContext
from dataclasses import dataclass
from prompts import opposition_prompt
from dotenv import load_dotenv
import os


load_dotenv()

MODEL=os.getenv("MODEL")

@dataclass
class OppositionDependencies:
    thesis: str

class OppositionResult(BaseModel):
    argument: str = Field(description="Argument denying the thesis")

# Agent denying the thesis
opposition = Agent(
    model=MODEL,
    deps_type=OppositionDependencies,
    result_type=OppositionResult,
    retries=1,
    model_settings={'temperature': 0.9}
)

@opposition.system_prompt
def get_system_prompt(ctx: RunContext[OppositionDependencies]) -> str:
    thesis = ctx.deps.thesis
    return opposition_prompt.format(thesis=thesis)
