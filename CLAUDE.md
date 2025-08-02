# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This repository contains a healthcare system unification SDK consisting of two main packages:

- **PyBrain**: AI-powered healthcare intelligence platform providing data harmonization, clinical NLP, decision support, and predictive analytics
- **PyHeart**: Healthcare interoperability and workflow engine providing FHIR integration, legacy system adapters, and workflow orchestration

Together, these packages create a unified healthcare platform that combines artificial intelligence with seamless integration capabilities.

## Architecture

The project follows a layered architecture:

```
Clinical Applications (EHR, Patient Portal)
           ↓
PyBrain (Intelligence Layer)
- AI Services, Analytics, Decision Support
           ↓  
PyHeart (Integration Layer)
- FHIR Integration, Workflow Engine, Security
           ↓
Healthcare Systems (FHIR Servers, HL7, Legacy)
```

### PyBrain Structure
- `core/ai/`: AI models and engines for clinical analysis
- `core/harmonizer/`: Data transformation to FHIR format
- `core/analytics/`: Healthcare analytics and population health
- `core/decision/`: Clinical decision support systems
- `core/knowledge/`: Medical knowledge graphs and ontologies

### PyHeart Structure  
- `core/client/`: FHIR and healthcare system clients
- `core/server/`: API gateway and FHIR server implementation
- `core/workflow/`: Healthcare process orchestration engine
- `core/integration/`: System adapters and connectors
- `core/security/`: Authentication, authorization, and compliance

## Development Commands

This project uses Python packaging with pyproject.toml configuration. Based on the package definitions:

### Testing
```bash
# Run tests (from package definitions)
pytest
pytest --cov=pybrain --cov=pyheart
pytest tests/integration --integration
```

### Code Quality
```bash
# Formatting and linting (from package definitions)
black .
flake8 .
isort .
mypy .
```

### CLI Usage
The packages provide command-line interfaces:

```bash
# PyBrain CLI
pybrain analyze -t "Clinical text to analyze"
pybrain harmonize -i input.json -f hl7v2 -r Patient
pybrain serve --port 8000

# PyHeart CLI  
pyheart fhir -s https://fhir.example.com -r Patient -i 12345
pyheart workflow -f workflow.json --watch
pyheart serve --port 8000
pyheart sync -s source_url -t target_url -r Patient
```

### Development Installation
```bash
# Install in development mode
pip install -e ".[dev]"

# Install with all optional dependencies
pip install -e ".[dev,ml,nlp,cloud,legacy]"
```

## Key Features

### PyBrain Capabilities
- Clinical NLP with Bio_ClinicalBERT model
- AI-powered risk assessment and prediction
- FHIR data harmonization from multiple formats
- Medical entity extraction from clinical notes
- Federated learning for privacy-preserving AI

### PyHeart Capabilities
- Universal FHIR client with async/sync operations
- Workflow engine for healthcare process automation
- Event-driven architecture with real-time streaming
- Security and compliance (HIPAA, GDPR) automation
- Legacy system integration (HL7v2, DICOM, X12)

## Integration Patterns

The packages are designed to work together seamlessly:

```python
from pybrain import AIEngine, DataHarmonizer
from pyheart import FHIRClient, WorkflowEngine

# Data access through PyHeart
client = FHIRClient("https://fhir.example.com")
patient_data = client.get_patient("12345")

# AI analysis through PyBrain
ai = AIEngine()
risk_score = ai.predict_risk_score(patient_data)

# Workflow orchestration
engine = WorkflowEngine()
if risk_score > 0.8:
    await engine.start_process("high-risk-intervention", {
        "patient_id": "12345",
        "risk_score": risk_score
    })
```

## Important Dependencies

### Core Dependencies
- fhir.resources>=6.5.0 (FHIR resource models)
- fastapi>=0.100.0 (API framework)
- pydantic>=2.0 (data validation)
- torch>=2.0.0 (AI models)
- transformers>=4.30.0 (NLP models)

### Infrastructure
- redis>=4.5.0 (caching and sessions)
- kafka (event streaming)
- postgresql (workflow state)
- prometheus (monitoring)

## Healthcare Standards Support

- **FHIR R4**: Primary healthcare data standard
- **HL7v2**: Legacy healthcare messaging
- **DICOM**: Medical imaging integration
- **X12**: Healthcare transactions
- **LOINC**: Laboratory data codes
- **SNOMED CT**: Clinical terminology
- **ICD-10**: Diagnosis codes

## Security and Compliance

The system includes comprehensive security features:
- AES-256-GCM encryption
- OAuth2/SMART on FHIR authentication
- Complete audit logging
- HIPAA, GDPR, ISO27001 compliance
- Patient consent management

## Example Workflows

The system supports complex healthcare workflows like:
- Patient admission protocols
- Medication reconciliation
- Emergency response procedures
- Chronic disease management
- Population health monitoring

## Docker Deployment

The repository includes docker-compose.yml for full infrastructure:
- FHIR server (HAPI)
- Redis for caching
- Kafka for events
- PostgreSQL for workflows
- Prometheus/Grafana for monitoring

Run with: `docker-compose up -d`

## File Extensions and Types

- `.py`: Python source code (primary language)
- `.json`: Configuration files, workflow definitions
- `.md`: Documentation (architecture overview)
- `.yml/.yaml`: Docker and configuration files
- `.toml`: Python project configuration (pyproject.toml)