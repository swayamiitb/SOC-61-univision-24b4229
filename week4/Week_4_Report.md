# Week 4: APIs And JSON Contracts

## What I Studied & Researched:
I spent this week figuring out the backend communication protocols needed to bridge the AI core to my React frontend. I built a strict "API contract" using FastAPI. This basically acts as a bouncer, ensuring the AI model only receives perfectly formatted data, which is super important to keep the system from crashing.

## My Code Experiment:

```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

class ImageRequest(BaseModel):
    image_id: str
    model_name: str
    threshold: float

class AnalysisResponse(BaseModel):
    status: str
    objects_found: int

@app.post("/analyze", response_model=AnalysisResponse)
async def analyze_image(request: ImageRequest):
    if request.threshold < 0.0 or request.threshold > 1.0:
        raise HTTPException(status_code=400, detail="Invalid threshold")
    
    return AnalysisResponse(status="success", objects_found=3)
```

## How It Works Under the Hood:
* **API as a Middleman**: The FastAPI app acts like a strict traffic controller. It dictates exactly how the frontend is allowed to interact with the AI pipeline.
* **HTTP Routes**: The `@app.post("/analyze")` line creates a specific web endpoint for the frontend to hit with its data.
* **JSON**: The Pydantic models (`ImageRequest` and `AnalysisResponse`) do the heavy lifting of automatically converting my Python objects into standard JSON text for web transmission.
* **Validation**: By defining exactly what data types to expect (like forcing the threshold to be a `float`), the system automatically kicks back malformed requests. This boundary check is huge for preventing backend crashes.

## My Progress This Week

### Work Completed So Far:
I set up the backend API contracts using FastAPI to serve as the bridge between the AI model and the frontend interface. I also defined explicit JSON request and response models to keep data organized.

### Key Milestones Achieved:
* Wrote a functional, routable API endpoint with strict incoming data validation.
* Implemented error handling that cleanly rejects bad configurations (like sending a threshold of 1.5 when the max is 1.0) to prevent the whole system from failing.

### Challenges Faced:
Managing how data transitions back and forth between raw Python objects and web-friendly JSON formats was quite a headache at first. It took me a bit of reading to truly understand how Pydantic validation acts as a necessary security and stability layer for the backend.

## Resources & References
_Resources I studied this week (paste your links):_

- RESTful API principles — <add link>
- FastAPI documentation — <add link>
- Pydantic validation — <add link>
- Python `async` / `asyncio` — <add link>
- OSI model (Application Layer / Layer 7) — <add link>
