"""
Autonomous AI agents with access to system resources
"""
import os
import json
from GPTAgents import tools, llm, memory

chatbot = llm.Chatbot(api_key=os.getenv("OPENAI_KEY"), engine="gpt-4", temperature=0)

## Initialize memory
interactions_history = memory.client.get_or_create_collection("interactions")
knowledge_base = memory.client.get_or_create_collection("knowledge_base")
pending_tasks = memory.client.get_or_create_collection("pending_tasks")
completed_tasks = memory.client.get_or_create_collection("completed_tasks")

## Human input to set goals
print("Enter the goals you want the AI to achieve")
goal = input()

## Step 1: Generate a plan to achieve the goals
print("Generating a plan to achieve the goals...")
prompt = f"""
You are an artificial general intelligence (AGI) that has been tasked with achieving the following goal:
'''
{goal}
'''
Your task is to plan a general sequence of actions that will achieve this goal.
Be as concise as possible and have minimal steps in the plan. Do not include actions that are not necessary to achieve the goal.
If the goal is limited, do not go beyond the exact goal.

The AI has access to a wide variety of tools and therefore perform actions a human can do on a computer.

For example, it can git clone a repository, list the contents of the repository, and decide which files to read

Return the plan as a JSON array of strings, where each string is a step in the plan. Do not include the tools to use.
"""

print(prompt)

try:
    response = json.loads(chatbot.ask(prompt, max_tokens=500))
except json.JSONDecodeError as err:
    raise Exception(
        "The response from the AI was not a valid JSON array of strings"
    ) from err

print(response)
