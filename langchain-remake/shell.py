import asyncio
import shlex


async def run(code: str):
    program = f"""
# timeout after 10 seconds
import signal
def signal_handler(signum, frame):
    raise Exception("Timed out!")
signal.signal(signal.SIGALRM, signal_handler)
signal.alarm(10)
{code}
"""
    program = shlex.quote(program)

    proc = await asyncio.create_subprocess_shell(f"python3 -c {program}")
    task = asyncio.create_task(proc.wait())
    await asyncio.sleep(0)
    
    return task
