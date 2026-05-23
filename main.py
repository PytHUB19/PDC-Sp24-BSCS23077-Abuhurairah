from fastapi import FastAPI
from llm_service import llm_with_fallback
from middleware import StudentHeaderMiddleware

app = FastAPI()

app.add_middleware(StudentHeaderMiddleware)


@app.get("/")
async def home():

    return {
        "message": "StudySync Backend Running"
    }


# WITHOUT circuit breaker
@app.get("/without-breaker")
async def without_breaker():

    result = await llm_with_fallback(use_breaker=False)

    return result


# WITH circuit breaker
@app.get("/with-breaker")
async def with_breaker():

    result = await llm_with_fallback(use_breaker=True)

    return result