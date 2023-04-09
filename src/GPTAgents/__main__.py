"""
Autonomous AI agents with access to system resources
"""
import os
import json
from GPTAgents import tools, llm, memory

chatbot = llm.Chatbot(
    api_key=os.getenv("OPENAI_KEY"), engine="gpt-4", temperature=0, system_prompt=""
)

## Initialize memory
# interactions_history = memory.client.get_or_create_collection("interactions")
# knowledge_base = memory.client.get_or_create_collection("knowledge_base")
# pending_tasks = memory.client.get_or_create_collection("pending_tasks")
# completed_tasks = memory.client.get_or_create_collection("completed_tasks")

# id_counter = 0

## Human input
print("Enter the name of the AI")
role = input()
print("Enter the goals you want the AI to achieve")
goal = input()

## Step 1: Generate a plan to achieve the goals
print("Generating a plan to achieve the goals...")
prompt = f"""
You are {role} that has been tasked with achieving the following goal:
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
    plans: list = json.loads(chatbot.ask(prompt, max_tokens=500))
    chatbot.reset()
except json.JSONDecodeError as err:
    raise Exception(
        "The response from the AI was not a valid JSON array of strings"
    ) from err

print(json.dumps(plans, indent=2))

# pending_tasks.add(
#     documents=response,
#     metadatas=[{"type": "plan", "scope": "general"} for _ in response],
#     ids=[str(id_counter := id_counter + 1) for _ in response],
# )

# print(pending_tasks.query(query_texts=["Step 1"], n_results=1).values())

## Step 2: Execute the plan
completed_tasks = []
done = False
while not done:
    current_general_task = plans.pop(0)

    prompt = f"""
    You are {role} that has been tasked with achieving the following goal:
    '''
    {goal}
    '''

    The current task is:
    '''
    {current_general_task}
    '''

    Completed tasks:
    {completed_tasks}

    Respond in JSON format: {'{ "action": "action", "parameters": "parameters" }'}
    Possible actions:
    - tool: Use a tool to perform an action
    - ask: Ask another AI to generate text
    - add_subtask: Add a subtask to the current task
    - complete: Complete the current task
    - think: Internal monologue explaining to yourself how to do something complex

    Tools:
        {tools.get_tools()}
    
    Be specific and avoid using generics. For example, instead of saying "mkdir new_project", actually name the project.
    If there is something you don't know such as popular websites, use tools to research it.
    """.strip()

    response = chatbot.ask(prompt)

    print(response)

    done = True
