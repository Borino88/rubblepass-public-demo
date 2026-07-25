import json
import os
import uuid
from typing import List, Dict, Any
from src.models.custody import AssessmentRequest, AssessmentResponse, DigitalMaterialPassport, CustodyLogEntry

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "data")

def load_json_data(filename: str) -> List[Dict[str, Any]]:
    path = os.path.join(DATA_DIR, filename)
    if not os.path.exists(path):
        return []
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def calculate_co2_savings(category: str, weight_kg: float) -> float:
    # Synthetic CO2 emission reduction factors (kg CO2 saved per kg recovered material)
    factors = {
        "Metals": 1.80,
        "Masonry & Concrete": 0.18,
        "Timber": 2.40,
        "Glass": 0.80
    }
    factor = factors.get(category, 0.50)
    return round(weight_kg * factor, 2)

def match_recovery_facility(category: str, weight_kg: float, facilities: List[Dict[str, Any]]) -> Dict[str, Any]:
    valid_facilities = [
        f for f in facilities if category in f.get("accepted_categories", [])
        and f.get("max_daily_capacity_kg", 0) >= weight_kg
    ]
    if not valid_facilities:
        # Fallback facility
        return {
            "facility_id": "FAC-GENERIC",
            "name": "Regional Municipal Sorting Hub",
            "distance_km": 45.0,
            "matching_score": 0.65
        }
    
    # Rank by matching score weighted by proximity
    best = sorted(valid_facilities, key=lambda x: (x.get("base_matching_score", 0.8) / (max(1.0, x.get("distance_km", 10.0)) ** 0.2)), reverse=True)[0]
    best["matching_score"] = round(best.get("base_matching_score", 0.85), 2)
    return best

def simulate_assessment(req: AssessmentRequest) -> AssessmentResponse:
    facilities = load_json_data("facilities.json")
    
    # Estimate weight
    estimated_weight = round(req.estimated_volume_m3 * req.density_factor_kg_m3, 2)
    co2_savings = calculate_co2_savings(req.category, estimated_weight)
    matched_facility = match_recovery_facility(req.category, estimated_weight, facilities)
    
    # Calculate synthetic confidence interval based on visual condition score
    confidence = round(70.0 + (req.visual_condition_score * 25.0), 1)
    
    mat_id = f"MAT-DEMO-{uuid.uuid4().hex[:6].upper()}"
    passport_id = f"PSP-{uuid.uuid4().hex[:8].upper()}"
    
    initial_log = CustodyLogEntry(
        event_type="SITE_ASSESSMENT_COMPLETED",
        actor="AI_ESTIMATION_ENGINE_V1",
        location=req.origin_site,
        notes=f"Initial field assessment logged. Estimated volume: {req.estimated_volume_m3} m3."
    )
    
    passport = DigitalMaterialPassport(
        passport_id=passport_id,
        material_id=mat_id,
        name=req.name,
        category=req.category,
        estimated_weight_kg=estimated_weight,
        condition_score=req.visual_condition_score,
        purity_percentage=round(req.visual_condition_score * 98.0, 1),
        contaminant_risk="Low" if req.visual_condition_score > 0.8 else "Medium",
        origin_facility=req.origin_site,
        recommended_recovery_route=f"Direct routing to {matched_facility['name']}",
        estimated_co2_savings_kg=co2_savings,
        qr_payload_url=f"https://rubblepass.demo/passport/{passport_id}",
        chain_of_custody=[initial_log]
    )
    
    return AssessmentResponse(
        assessment_id=f"AST-{uuid.uuid4().hex[:8].upper()}",
        material_id=mat_id,
        estimated_weight_kg=estimated_weight,
        confidence_interval_percentage=confidence,
        recommended_route=passport.recommended_recovery_route,
        matched_facility=matched_facility,
        estimated_co2_savings_kg=co2_savings,
        passport_preview=passport
    )
