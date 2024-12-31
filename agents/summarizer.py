import os
from pydantic_ai import Agent, RunContext
from pydantic import BaseModel, Field
from dataclasses import dataclass
from dotenv import load_dotenv
from prompts import summarizer_prompt
from typing import Literal

load_dotenv()

MODEL=os.getenv("MODEL")

@dataclass
class SummarizerDependencies:
    thesis: str = Field(description="Thesis of the debate")
    proposition_score: float = Field(description="Score of proposition side")
    opposition_score: float = Field(description="Score of opposition side")


class SummarizerResult(BaseModel):
    winner: Literal['proposition', 'opposition', 'draw'] = Field(
        description="The winner of the debate (proposition/opposition/draw)"
    )
    repeated: str = Field(description="Arguments which were repeated")
    mismatch: str = Field(description="Arguments which didn't exactly stick to the thesis")
    summary: str = Field(description="Overall summary of the debate")

summarizer = Agent(
    model=MODEL,
    deps_type=SummarizerDependencies,
    result_type=SummarizerResult,
    retries=1
)

@summarizer.system_prompt
def get_system_prompt(ctx: RunContext[SummarizerDependencies]) -> str:
    thesis = ctx.deps.thesis
    return summarizer_prompt.format(thesis=thesis)

@summarizer.tool
def get_debate_winner(ctx: RunContext[SummarizerDependencies]) -> Literal['proposition', 'opposition', 'draw']:
    """Get the winner of the debate"""
    if ctx.deps.proposition_score > ctx.deps.opposition_score:
        return 'proposition'
    elif ctx.deps.proposition_score < ctx.deps.opposition_score:
        return 'opposition'
    else:
        return 'draw'
