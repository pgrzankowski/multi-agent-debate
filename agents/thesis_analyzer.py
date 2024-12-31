from pydantic_ai import Agent
from pydantic import BaseModel, Field
from dotenv import load_dotenv
from prompts import thesis_analyzer_prompt
import os


load_dotenv()
MODEL = os.getenv("MODEL")

class ThesisAnalyzerResult(BaseModel):
    debatable: bool = Field(description="Whether the thesis is debatable or not")
    explanation: str = Field(description="Explanation of the result")

thesis_analyzer = Agent(
    model=MODEL,
    result_type=ThesisAnalyzerResult,
    retries=1,
    system_prompt=thesis_analyzer_prompt
)
