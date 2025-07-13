from teams.round_robin_team import create_dsa_team_and_docker
from utils.docker import docker_executor
from autogen_agentchat.messages import TextMessage
from autogen_agentchat.base import TaskResult
import asyncio

async def main():
    dsa_solver_team,docker = create_dsa_team_and_docker()
    try:
        task = " Write a function for fibonacci series "
        print("Starting docker container...")
        await docker.start()
        print("Docker runtime is started...")

        async for message in dsa_solver_team.run_stream(task=task):
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
