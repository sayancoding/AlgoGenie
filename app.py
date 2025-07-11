from autogen_ext.code_executors.docker import DockerCommandLineCodeExecutor
from autogen_agentchat.agents import CodeExecutorAgent
from autogen_agentchat.messages import TextMessage
from autogen_core import CancellationToken
import asyncio


async def main():

    docker = DockerCommandLineCodeExecutor(
        work_dir='/temp',
        timeout=120
    )

    code_executor_agent = CodeExecutorAgent(
        name="CodeExecutorAgent",
        code_executor=docker
    )

    task = TextMessage(
        content='''Here is some code
```python
print('Hello world')
```
    ''',    
        source="user",
    )

    await docker.start()

    try:
        result = await code_executor_agent.on_messages(
            messages= [task],
            cancellation_token= CancellationToken()
        ) 
        print("Result : ",result.chat_message.content) # type: ignore
    except Exception as ex:
        print(f"ERROR :: {ex}")
    finally:
        await docker.stop()


if __name__ == "__main__":
    asyncio.run(main())
