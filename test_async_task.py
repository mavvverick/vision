import asyncio
import random


async def grab_proxy(taskid):
    await asyncio.sleep(random.uniform(0.1, 1))
    result = random.choice([None, None, None, 'result'])
    print(f'Task #{taskid} producing result {result!r}')
    return result


async def task_manager():
    tasks = [grab_proxy(i) for i in range(10)]
    while tasks:
        finished, unfinished = await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)
        for x in finished:
            result = x.result()
            print(f"Finished task produced {result!r}")
            if result:
                # cancel the other tasks, we have a result. We need to wait for the cancellations
                # to propagate.
                print(f"Cancelling {len(unfinished)} remaining tasks")
                for task in unfinished:
                    task.cancel()
                await asyncio.wait(unfinished)
                return result
        tasks = unfinished


def get_proxy_loop():
    loop = asyncio.new_event_loop()
    proxy = loop.run_until_complete(task_manager())
    loop.close()
    return proxy


get_proxy_loop()
