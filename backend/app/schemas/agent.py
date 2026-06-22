# Defines the schema for AI research results and agent interactions.

from pydantic import BaseModel, Field, ConfigDict
from typing import List

class ResearchResult(BaseModel):
    """
    The exact JSON structure the agent will be forced to return.
    """

    model_config = ConfigDict(extra="forbid")

    topic: str = Field(..., description="The main topic that was researched.")
    summary: str = Field(..., description="A concise 2-sentence summary of the topic.")
    key_takeaways: List[str] = Field(..., description="Exactly 3 bullet points of critical information.")
    confidence_score: float = Field(..., description="A score from 0.0 to 1.0 indicating how confident the agent is in this data.")