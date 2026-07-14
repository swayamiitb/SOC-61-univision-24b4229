"""Week 4: an async FastAPI gateway with strict Pydantic validation.

Rejects malformed inference payloads with a 422 before they reach the model.
Run with:  uvicorn api:app --reload
"""
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

app = FastAPI(title="Uni_Vision Inference Gateway")


class InferenceRequestSchema(BaseModel):
    # Pydantic enforces types and bounds at the parser level
    camera_id: str = Field(..., min_length=3, max_length=15)
    confidence_threshold: float = Field(..., ge=0.1, le=0.99)
    enable_gpu_accel: bool = True


class InferenceResponseSchema(BaseModel):
    status_code: int
    message: str
    active_threads: int


@app.post("/api/v1/configure", response_model=InferenceResponseSchema)
async def configure_pipeline(payload: InferenceRequestSchema):
    """Async endpoint. Frees the event loop while waiting on I/O."""
    try:
        # by here, payload is guaranteed valid
        print(f"Configuring {payload.camera_id} at thresh {payload.confidence_threshold}")
        return InferenceResponseSchema(
            status_code=200,
            message="Pipeline configured successfully.",
            active_threads=4,
        )
    except Exception:
        # never leak an internal stack trace to the client
        raise HTTPException(status_code=500, detail="Internal AI Core Failure")
