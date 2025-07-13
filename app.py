from autogen_ext.code_executors.docker import DockerCommandLineCodeExecutor
from autogen_agentchat.agents import CodeExecutorAgent,AssistantAgent
from autogen_agentchat.messages import TextMessage
from autogen_core import CancellationToken
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.conditions import TextMentionTermination
from autogen_agentchat.base import TaskResult

import asyncio
from dotenv import load_dotenv
import os

load_dotenv()
GEMINI_API_KEY = os.getenv('GOOGLE_API_KEY')
if not GEMINI_API_KEY:
    raise ValueError("GEMINI API Key is not pres")

llm_client = OpenAIChatCompletionClient(model='gemini-2.5-flash',api_key=GEMINI_API_KEY)

async def main():

    docker = DockerCommandLineCodeExecutor(
        work_dir='/temp',
        timeout=120
    )

    code_executor_agent = CodeExecutorAgent(
        name="CodeExecutorAgent",
        code_executor=docker
    )

    problemSolverAgent = AssistantAgent(
        name = "ProblemSolverAgent",
        description="An assistant agent that help to solve DSA problem & write code",
        model_client= llm_client,
        system_message="""
        you are the code solver agent that very expert in data structure and algorithm and solve any that related coding problem.
        you will be working with code executor agent to execute code.
        you will given problem or task , you will solve.
        At first explain your approach and then give the answer with in simple block of code in python language only.
        then pass block of code to code-executor-agent to execute along with 2 test cases.
        if the code is executed successfully and test cases are passed, then you have the result.

        in the end if all are satisfied , then you have to say "STOP" to end conversation.
    """
    )

    termination_call = TextMentionTermination("STOP")

    team = RoundRobinGroupChat(
        participants= [problemSolverAgent, code_executor_agent],
        termination_condition= termination_call,
        max_turns=10
    )

    try:
        task = " Write a function for fibonacci series "
        await docker.start()

        async for message in team.run_stream(task=task):
            if(isinstance(message,TextMessage)):
                print("==="*20)
                print(f" {message.source} :: {message.content}") # type: ignore
                print("==="*20)
            elif(isinstance(message, TaskResult)):
                print(f"Stopping Conversation for : {message.stop_reason}")

    except Exception as ex:
        print(f"ERROR :: {ex}")
    finally:
        await docker.stop()


if __name__ == "__main__":
    asyncio.run(main())
