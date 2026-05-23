from starlette.middleware.base import BaseHTTPMiddleware

STUDENT_ID = "BSCS23077"

class StudentHeaderMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request, call_next):
        response = await call_next(request)

        response.headers["X-Student-ID"] = STUDENT_ID

        return response