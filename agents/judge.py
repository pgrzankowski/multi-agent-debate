from pydantic import BaseModel, Field
from pydantic_ai import Agent, RunContext
from dataclasses import dataclass
from prompts import judge_prompt
from dotenv import load_dotenv
import os


load_dotenv()

MODEL=os.getenv("MODEL")

@dataclass
class JudgeDependencies:
    thesis: str

class JudgeResult(BaseModel):
    class Score(BaseModel):
        proposition: float = Field(description="Score for the proposition side")
        opposition: float = Field(description="Score for the opposition side")
    score: Score
    explanation: str = Field(description="Short and brief explanation of your decision")

# Agent denying thesis
judge = Agent(
    model=MODEL,
    deps_type=JudgeDependencies,
    result_type=JudgeResult,
    retries=1
)

@judge.system_prompt
def get_system_prompt(ctx: RunContext[JudgeDependencies]) -> str:
    thesis = ctx.deps.thesis
    return judge_prompt.format(thesis=thesis)
