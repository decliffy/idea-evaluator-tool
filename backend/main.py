import logging

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, field_validator
from evaluator import evaluate_idea

logger = logging.getLogger("app")
logger.setLevel(logging.INFO)

app = FastAPI(title="Idea Evaluator")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["POST"],
    allow_headers=["Content-Type"],
)


class IdeaRequest(BaseModel):
    idea: str

    @field_validator("idea")
    @classmethod
    def idea_must_have_content(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("Idea cannot be empty")
        if len(v) < 30:
            raise ValueError("Please describe your idea in at least 30 characters")
        return v


@app.post("/api/evaluate")
async def evaluate(request: IdeaRequest):
    logger.info("evaluate: route entered, idea length=%d", len(request.idea))
    try:
        result = await evaluate_idea(request.idea)
        logger.info("evaluate: completed, total_score=%s", result.get("total_score"))
        return result
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Evaluation failed: {str(e)}")


# AWS Lambda entry point (used by API Gateway via Mangum). Imported lazily so
# local `uvicorn main:app` dev does not require mangum to be installed.
try:
    from mangum import Mangum

    # lifespan="off": API Gateway/Lambda invokes one request at a time and the
    # app has no startup/shutdown work, so skip the ASGI lifespan handshake
    # (which can hang the invocation under Mangum).
    handler = Mangum(app, lifespan="off")
except ImportError:  # pragma: no cover - mangum only needed in Lambda
    handler = None
