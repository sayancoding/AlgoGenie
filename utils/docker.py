from autogen_ext.code_executors.docker import DockerCommandLineCodeExecutor

def docker_executor():
    docker = DockerCommandLineCodeExecutor(
        work_dir='/temp',
        timeout=120
    )
    return docker

async def start_docker():
    await docker_executor().start()

async def stop_docker():
    await docker_executor().stop()
