from autogen_agentchat.agents import AssistantAgent
from configs.llm_clients import llm_model

llm = llm_model()

def get_problem_solver_agent():

    problemSolverAgent = AssistantAgent(
            name = "ProblemSolverAgent",
            description="An assistant agent that help to solve DSA problem & write code",
            model_client= llm,
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
    return problemSolverAgent