import streamlit as st
import asyncio
from teams.round_robin_team import create_dsa_team_and_docker
from autogen_agentchat.messages import TextMessage
from autogen_agentchat.base import TaskResult

st.title("🧩 AlgoGenie")
st.text("Data Structure & Algorithm Solver Using AutoGen AI")

task = st.text_input("Give me the DSA task here..")
solve = st.button("Solve")

async def run(team,docker,task):
    try:
        st.write("Starting docker container...")
        await docker.start()
        st.write("Docker runtime is started...")

        async for message in team.run_stream(task=task):
            if(isinstance(message,TextMessage)):
                print(msg:= f"{message.source} : {message.content}") # type: ignore
                yield msg
            elif(isinstance(message, TaskResult)):
                print(msg:= f"Stopping Conversation for : {message.stop_reason}")
                yield msg

    except Exception as ex:
            st.warning(f"ERROR :: {ex}")
    finally:
            await docker.stop()
            st.success("Ending Conversations..") 
            st.success("Docker Container is Stopped Now")
               


if solve:
    dsa_solver_team,docker = create_dsa_team_and_docker()

    async def collect_message():
        async for msg in run(dsa_solver_team,docker,task):
            if isinstance(msg, str):
                if msg.startswith("user :"):
                    with st.chat_message('user',avatar='👤'):
                        st.markdown(msg)
                elif msg.startswith("ProblemSolverAgent :"):
                    with st.chat_message("assistant",avatar='🕵️‍♀️'): 
                        st.markdown(msg)
                elif msg.startswith("CodeExecutorAgent :"):
                    with st.chat_message("assistant"):
                        st.markdown(msg)
            elif isinstance(msg,TaskResult):
                st.markdown(msg)
    
    asyncio.run(collect_message())
         