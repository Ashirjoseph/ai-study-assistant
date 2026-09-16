from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.config import settings
from app.database import init_db
from app.routers import ask, flashcards, history, mcqs, summary


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(title="AI Study Assistant", version="0.1.0", lifespan=lifespan)
app.include_router(ask.router)
app.include_router(summary.router)
app.include_router(mcqs.router)
app.include_router(flashcards.router)
app.include_router(history.router)


@app.exception_handler(Exception)
async def unhandled_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    # Catch-all safety net: never leak internals/tracebacks to the client.
    return JSONResponse(status_code=500, content={"detail": "Internal server error"})


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "env": settings.APP_ENV}
