import random
import asyncio
import time

# Circuit breaker state
failure_count = 0
circuit_open = False
last_failure_time = 0

FAILURE_THRESHOLD = 3
RESET_TIMEOUT = 10


async def actual_llm_call():

    # Simulate failing API
    if random.random() < 0.8:

        print("LLM FAILED")

        await asyncio.sleep(8)

        raise Exception("LLM timeout")

    print("LLM SUCCESS")

    await asyncio.sleep(1)

    return {
        "status": "success",
        "response": "AI generated notes successfully."
    }


async def llm_with_fallback(use_breaker=True):

    global failure_count
    global circuit_open
    global last_failure_time

    # -----------------------------
    # CIRCUIT BREAKER LOGIC
    # -----------------------------

    if use_breaker:

        # Check if breaker should reset
        if circuit_open:

            current_time = time.time()

            if current_time - last_failure_time > RESET_TIMEOUT:

                print("RESETTING CIRCUIT")

                circuit_open = False
                failure_count = 0

            else:

                print("CIRCUIT OPEN → FAIL FAST")

                return {
                    "status": "circuit_open",
                    "response": "LLM unavailable. Cached response returned instantly."
                }

    # -----------------------------
    # TRY ACTUAL API CALL
    # -----------------------------

    try:

        result = await actual_llm_call()

        failure_count = 0

        return result

    except Exception:

        failure_count += 1

        print(f"FAIL COUNT = {failure_count}")

        # Open breaker
        if failure_count >= FAILURE_THRESHOLD:

            circuit_open = True
            last_failure_time = time.time()

            print("CIRCUIT BREAKER ACTIVATED")

        return {
            "status": "fallback",
            "response": "Temporary AI failure."
        }