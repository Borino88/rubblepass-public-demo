# RubblePass AI — Cleantech Circular Recovery & Material Assessment Demonstration

[![CI Pipeline](https://github.com/Borino88/rubblepass-public-demo/actions/workflows/docker-publish.yml/badge.svg)](https://github.com/Borino88/rubblepass-public-demo/actions/workflows/docker-publish.yml)
[![Docker Hub](https://img.shields.io/docker/v/borino88/rubblepass-public-demo?label=docker&logo=docker)](https://hub.docker.com/r/borino88/rubblepass-public-demo)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110+-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![Docker](https://img.shields.io/badge/Docker_Compose-Ready-2496ED?style=for-the-badge&logo=docker&logoColor=white)](https://www.docker.com)
[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org)

This repository serves as an open-source **architectural and technical demonstration** of the backend mechanics behind **RubblePass AI** — a cleantech software platform founded by **Mahdi Fattahi** focused on pre-demolition material assessment, circular recovery routing, and verifiable digital material passports.

---

## ⚠️ Intellectual Property & Confidentiality Notice
To safeguard core commercial algorithms and proprietary client datasets, this repository utilizes a **synthetic demonstration dataset** (`data/synthetic_materials.json` and `data/facilities.json`). While the mathematical matching logic, chain-of-custody data schemas, and API structures accurately reflect our enterprise production design, proprietary machine learning model weights, live recycler pricing integrations, and customer databases remain strictly confidential within our private enterprise infrastructure.

---

## 🌟 Why Digital Material Passports for Construction?
The demolition and construction sector is responsible for over 30% of global landfill waste. Traditional demolition practices fail to salvage high-value structural steel, masonry, and architectural timber due to lack of verified condition data, uncertain material purity, and fragmented logistics.

**RubblePass AI** solves this bottleneck by providing a mobile-first field assessment tool that calculates material volume, assigns condition scores, estimates carbon savings, and binds every salvaged batch to an immutable **Digital Material Passport (DMP)** accessible via QR code.

---

## 🏗️ Architecture & Simulation Pipeline

```text
+-------------------------------------------------------------------------------+
|                    MOBILE-FIRST FIELD ASSESSMENT INTERFACE                    |
|        [On-Site Engineer Ingests Volume, Material Category & Condition]       |
+-------------------------------------------------------------------------------+
                                        |
                                        v (POST /api/v1/assess)
+-------------------------------------------------------------------------------+
|                      FASTAPI RECOVERY ESTIMATION ENGINE                       |
|   - Density & Weight Simulation -> Carbon (CO2) Reduction Calculation         |
|   - Proximity & Capacity Routing -> Facility Matching Algorithm               |
+-------------------------------------------------------------------------------+
                                        |
                                        v
+-------------------------------------------------------------------------------+
|                    DIGITAL MATERIAL PASSPORT (DMP) CREATION                   |
|   - Unique UUID Binding (MAT-ID & PSP-ID) -> Immutable Chain of Custody Log   |
+-------------------------------------------------------------------------------+
                                        |
                 +----------------------+----------------------+
                 |                                             |
                 v                                             v
+----------------------------------+        +----------------------------------+
|   QR CODE PASSPORT ENDPOINT      |        |   MATCHED RECOVERY ROUTE DISPATCH |
|   - Verifiable Chain of Custody  |        |   - Direct Facility Instructions |
+----------------------------------+        +----------------------------------+
```

---

## ⚡ Quick Start (Container & Local)

### 1. Run with Docker Quick-Start (Recommended)
Run the prebuilt, hardened multi-stage container instantly:
```bash
docker run -d --name rubblepass-demo -p 8000:8000 borino88/rubblepass-public-demo:latest
```
* **Interactive Field Portal:** Navigate to `http://localhost:8000`
* **OpenAPI Documentation (Swagger UI):** Navigate to `http://localhost:8000/docs`
* **Health Check Endpoint:** Navigate to `http://localhost:8000/health`

### 2. Run with Docker Compose
You can launch the entire demonstration service with a single command:
```bash
git clone https://github.com/Borino88/rubblepass-public-demo.git
cd rubblepass-public-demo

docker-compose up --build
```
* **Interactive Field Portal:** Navigate to `http://localhost:8000`
* **OpenAPI Documentation (Swagger UI):** Navigate to `http://localhost:8000/docs`

### 2. Run with Python Virtual Environment
```bash
# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Launch FastAPI server
uvicorn src.api.main:app --reload --host 0.0.0.0 --port 8000
```

---

## 🧪 Automated Testing
The repository is validated using a comprehensive `pytest` suite covering REST endpoints, matching algorithms, and Pydantic data schemas:
```bash
pytest tests/ -v
```

---

## 📂 Repository Structure
```text
├── data/
│   ├── synthetic_materials.json    # Sample building materials (steel, timber, aggregate)
│   └── facilities.json             # Synthetic recycling & salvage facility network
├── src/
│   ├── api/
│   │   └── main.py                 # FastAPI application and route controllers
│   ├── models/
│   │   └── custody.py              # Pydantic schemas (Passports, Chain-of-Custody logs)
│   └── pipeline/
│       └── estimation.py           # Volume-weight simulation & facility matching engine
├── static/
│   └── index.html                  # Responsive, mobile-first field assessment UI demo
├── tests/
│   └── test_api.py                 # Pytest integration and endpoint test suite
├── Dockerfile                      # Containerization blueprint
├── docker-compose.yml              # One-command orchestration
└── ARCHITECTURE.md                 # In-depth engineering design documentation
```

---

## 📬 Founder & Technical Contact
* **Founder & Lead Architect:** [Mahdi Fattahi](https://fattahi.xyz)
* **Email:** [a.borino88@gmail.com](mailto:a.borino88@gmail.com)
* **LinkedIn:** [Mahdi Fattahi](https://www.linkedin.com/in/mahdi-fattahi-685964120/)
* **GitHub Profile:** [Borino88](https://github.com/Borino88)

---
*© 2026 RubblePass AI. Released under the MIT License for architectural demonstration purposes.*
