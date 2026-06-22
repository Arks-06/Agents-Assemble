# actual research agent made using agno framework and groq llm

from agno.agent import Agent
from agno.models.groq import Groq
from agno.tools.tavily import TavilyTools
from app.core.config import settings

def build_research_agent() -> Agent:
    """
    Instantiates and configures autonomous researcher.
    """
    return Agent(
        model=Groq(id="llama-3.3-70b-versatile", api_key=settings.GROQ_API_KEY),
        description="You are an elite, highly concise technical researcher.",
        instructions=[
            "Focus on factual, objective information.",
            "Use your Tavily search tool to find up-to-date data if you aren't certain.",
            "CRITICAL: You MUST return strictly valid JSON. Do not include conversational filler or markdown wrappers."
        ],
        tools=[TavilyTools(
            search_depth="advanced",
            max_tokens=6000
        )],
        tool_call_limit=3,
        debug_mode=True, 
        markdown=True
    )