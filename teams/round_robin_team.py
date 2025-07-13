from autogen_agentchat.teams import RoundRobinGroupChat
from agents.code_executor_agent import get_code_executor_agent_and_docker
from agents.problem_solver_agent import get_problem_solver_agent
from conditions.text_termination import stop_termination

def create_dsa_team_and_docker():
    problemSolverAgent = get_problem_solver_agent()
    codeExecutorAgent,docker = get_code_executor_agent_and_docker()

    team = RoundRobinGroupChat(
            participants= [problemSolverAgent, codeExecutorAgent],
            termination_condition= stop_termination(),
            max_turns=10
        )
    return team,docker