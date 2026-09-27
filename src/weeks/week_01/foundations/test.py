import asyncio
import random
from dataclasses import dataclass

from tenacity import (
    RetryError,
    retry,
    retry_if_exception_type,
    stop_after_attempt,
    wait_exponential,
)

class APIError(TimeoutError):
    pass


@dataclass(frozen=True)
class APIRespone:
    status_code: int
    text: str


@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=1, max=5),
    retry=retry_if_exception_type(APIError),
)
async def laggy_api(requestId: int):
    p = random.random()
    # if p < 0.5:
    #     raise APIError("Something went wrong")
    print(f"Starting processing the result for ID {requestId}")
    await asyncio.sleep(random.random()*4)
    print(f"Processing the result for ID {requestId}")
    return APIRespone(requestId, text=f"laggy API Respone for {requestId}")



async def parallel_run(requestIDs):
    try:
        parallel_tasks = [asyncio.wait_for(laggy_api(requestID), 0.5) for requestID in requestIDs]
        return await asyncio.gather(*parallel_tasks)
    except TimeoutError:
        print(f"Timeout for request")
    except Exception as ex:
        print("Something went wrong")

async def serial_run(requestIDs):
    serial_tasks = [await laggy_api(requestID) for requestID in requestIDs]
    return serial_tasks




async def demo():
    task_ids = [1,2,3,4,5,6,7,8,9]
    parallel_result = await parallel_run(task_ids)
    print(parallel_result)

    # serial_results = await serial_run(task_ids)
    # print(serial_results)
if __name__ == "__main__":
    asyncio.run(demo())


