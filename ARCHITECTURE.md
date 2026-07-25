# RubblePass AI — Technical Architecture & Domain Model

## 1. Executive Overview
RubblePass AI is architected as a modular, high-throughput cleantech platform that transforms fragmented construction demolition data into actionable circular economy logistics. This document describes the core backend data schemas, facility matching heuristics, and digital passport generation pipeline.

---

## 2. Core Domain Models (Pydantic Schema Definitions)

### 2.1 Digital Material Passport (DMP)
Every batch of salvaged material is assigned a unique cryptographic-style UUID that persists throughout its lifecycle from site extraction to secondary manufacturing.
* **Attributes:** `passport_id`, `material_id`, `purity_percentage`, `condition_score`, `contaminant_risk`, `chain_of_custody`.

### 2.2 Immutable Chain of Custody
To prevent greenwashing and guarantee structural compliance, every physical transfer is recorded as an immutable log entry:
* **Log Structure:** `timestamp`, `event_type` (SITE_ASSESSMENT, SALVAGE_DISPATCH, FACILITY_RECEIPT, REPURPOSE_CERTIFIED), `actor`, `location`.

---

## 3. Facility Matching Algorithm
When an engineer logs a salvage request via the field interface (`POST /api/v1/assess`), the backend executes a multi-factor matching algorithm:
1. **Category Filtering:** Evaluates regional facilities accepting the designated material class (e.g., Structural Steel, Aggregates, Vintage Timber).
2. **Capacity Validation:** Verifies that the target facility's available `max_daily_capacity_kg` exceeds the estimated load weight.
3. **Proximity & Efficiency Scoring:** Ranks candidates using a weighted scoring formula:
   $$\text{FinalScore} = \frac{\text{BaseScore}}{\text{DistanceKm}^{0.2}}$$
   This ensures optimal transport distance while prioritizing certified circular salvage hubs over standard downcycling crushers.

---

## 4. Carbon (CO₂) Reduction Accounting
The estimation engine applies verified embodied carbon emission factors to compute greenhouse gas savings compared to virgin material manufacturing:
* **Structural Metals:** 1.80 kg CO₂ saved per kg salvaged.
* **Architectural Timber:** 2.40 kg CO₂ saved per kg salvaged.
* **Glass & Concrete:** 0.80 and 0.18 kg CO₂ saved per kg respectively.
