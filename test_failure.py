import asyncio
import httpx
import time

WITHOUT_BREAKER = "http://127.0.0.1:8000/without-breaker"
WITH_BREAKER = "http://127.0.0.1:8000/with-breaker"


async def test_endpoint(url, label):

    print(f"\n===== TESTING {label} =====\n")

    async with httpx.AsyncClient(timeout=15) as client:

        tasks = []

        start = time.time()

        for i in range(10):
            tasks.append(client.get(url))

        responses = await asyncio.gather(*tasks)

        end = time.time()

        print(f"Total Time: {round(end - start, 2)} seconds\n")

        for i, response in enumerate(responses):

            print(f"Request {i+1}: {response.json()['status']}")


async def main():

    await test_endpoint(WITHOUT_BREAKER, "WITHOUT CIRCUIT BREAKER")

    print("\n\n-----------------------------------\n")

    await test_endpoint(WITH_BREAKER, "WITH CIRCUIT BREAKER")


asyncio.run(main())