from datetime import datetime, timezone
from typing import List, Optional
from pydantic import BaseModel, Field

class CustodyLogEntry(BaseModel):
    timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    event_type: str = Field(..., description="e.g., SITE_ASSESSMENT, SALVAGE_DISPATCH, FACILITY_RECEIPT, REPURPOSE_CERTIFIED")
    actor: str = Field(..., description="Authorized handler or auditor ID")
    location: str = Field(..., description="Physical coordinates or site identifier")
    notes: Optional[str] = None

class DigitalMaterialPassport(BaseModel):
    passport_id: str
    material_id: str
    name: str
    category: str
    estimated_weight_kg: float
    condition_score: float
    purity_percentage: float
    contaminant_risk: str
    origin_facility: str
    recommended_recovery_route: str
    estimated_co2_savings_kg: float
    qr_payload_url: str
    chain_of_custody: List[CustodyLogEntry]

class AssessmentRequest(BaseModel):
    name: str
    category: str
    estimated_volume_m3: float
    density_factor_kg_m3: float = 2400.0
    visual_condition_score: float = Field(..., ge=0.0, le=1.0)
    origin_site: str
    notes: Optional[str] = None

class AssessmentResponse(BaseModel):
    assessment_id: str
    material_id: str
    estimated_weight_kg: float
    confidence_interval_percentage: float
    recommended_route: str
    matched_facility: dict
    estimated_co2_savings_kg: float
    passport_preview: DigitalMaterialPassport
