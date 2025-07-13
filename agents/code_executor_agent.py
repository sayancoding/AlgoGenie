from autogen_agentchat.agents import CodeExecutorAgent
from utils.docker import docker_executor

def get_code_executor_agent_and_docker():
    docker = docker_executor()
    code_executor_agent = CodeExecutorAgent(
            name="CodeExecutorAgent",
            code_executor=docker
        )
    return code_executor_agent,docker