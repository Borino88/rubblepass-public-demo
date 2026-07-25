from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
import os

from src.models.custody import AssessmentRequest, AssessmentResponse
from src.pipeline.estimation import simulate_assessment, load_json_data

app = FastAPI(
    title="RubblePass AI — Cleantech Material Assessment API",
    description="Public architectural demonstration of AI-assisted pre-demolition material assessment, circular recovery routing, and digital material passports.",
    version="1.0.0-demo"
)

# Serve static mobile demo if available
STATIC_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "static")
if os.path.exists(STATIC_DIR):
    app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

@app.get("/", response_class=HTMLResponse)
def root_interface():
    index_path = os.path.join(STATIC_DIR, "index.html")
    if os.path.exists(index_path):
        with open(index_path, "r", encoding="utf-8") as f:
            return f.read()
    return """
    <html>
        <head><title>RubblePass AI API</title></head>
        <body style="font-family: sans-serif; padding: 2rem;">
            <h1>RubblePass AI — Demonstration API</h1>
            <p>Visit <a href="/docs">/docs</a> for interactive OpenAPI specification.</p>
        </body>
    </html>
    """

@app.get("/health", tags=["System"], summary="System health check endpoint")
def health_check():
    return {"status": "ok", "service": "rubblepass-public-demo", "version": "1.0.0-demo"}

@app.get("/api/v1/materials", summary="List synthetic demonstration building materials")
def list_materials():
    data = load_json_data("synthetic_materials.json")
    return {"status": "success", "count": len(data), "materials": data}

@app.get("/api/v1/facilities", summary="List synthetic recycling and recovery hubs")
def list_facilities():
    data = load_json_data("facilities.json")
    return {"status": "success", "count": len(data), "facilities": data}

@app.post("/api/v1/assess", response_model=AssessmentResponse, summary="Simulate AI material assessment and route matching")
def assess_material(request: AssessmentRequest):
    try:
        response = simulate_assessment(request)
        return response
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Assessment simulation failed: {str(e)}")

@app.get("/api/v1/passport/{passport_id}", summary="Retrieve digital material passport by ID")
def get_passport(passport_id: str):
    # For demo purposes, return a generated sample matching the ID
    req = AssessmentRequest(
        name="Retrieved Sample Structural Timber",
        category="Timber",
        estimated_volume_m3=10.0,
        visual_condition_score=0.90,
        origin_site="Sample Demolition Archive Site"
    )
    res = simulate_assessment(req)
    res.passport_preview.passport_id = passport_id
    return {"status": "success", "passport": res.passport_preview}
