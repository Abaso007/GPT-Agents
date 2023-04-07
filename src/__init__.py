"""
Autonomous AI agents with access to system resources
"""
import os
from GPTAgents import tools, paths, llm, memory

chatbot = llm.Chatbot(api_key=os.getenv("OPENAI_KEY"))
