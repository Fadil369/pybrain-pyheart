# 🧠❤️ PyBrain & PyHeart - Healthcare Unification Platform

[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-Apache%202.0-green.svg)](LICENSE)
[![Build Status](https://img.shields.io/badge/build-passing-brightgreen.svg)](https://github.com/Fadil369/pybrain-pyheart)

A comprehensive healthcare interoperability platform combining AI-powered intelligence with seamless system integration for BrainSAIT-style bilingual, region-aware healthcare operations.

## 🚀 Overview

This repository contains two complementary Python packages that together create the most advanced healthcare interoperability platform:

### 🧠 **PyBrain** - The Intelligence Layer
AI-powered healthcare intelligence platform providing:
- **AI-Powered Data Harmonization**: Automatically maps and transforms healthcare data
- **Clinical NLP Engine**: Extracts structured data from clinical notes
- **Federated Learning Framework**: Privacy-preserving AI model training
- **Real-time Decision Support**: Evidence-based clinical recommendations
- **Predictive Analytics**: Patient outcome and population health forecasting

### ❤️ **PyHeart** - The Integration Layer  
Universal healthcare system connectivity platform providing:
- **🔌 Plug-and-Play SDK**: Pre-built plugins for providers, insurance companies, and government offices
- **Universal API Gateway**: Single interface for all healthcare integrations
- **Event-Driven Architecture**: Real-time data streaming and processing
- **Microservices Framework**: Modular, scalable healthcare services
- **Security & Compliance Engine**: HIPAA, GDPR, and regional compliance
- **Workflow Orchestration**: Complex healthcare process automation

## 📦 Quick Start

### Installation

```bash
# Install both packages
pip install brainsait-pybrain brainsait-pyheart

# Or install from this repository
pip install -e ./pybrain-pkg
pip install -e ./pyheart-pkg
```

### Basic Usage

```python
from pybrain import AIEngine, DataHarmonizer
from pyheart import FHIRClient, WorkflowEngine

# AI-powered clinical analysis
ai = AIEngine()
entities = ai.extract_clinical_entities("Patient has diabetes and hypertension")

# FHIR connectivity
client = FHIRClient("https://fhir.hospital.com")
patient = client.get_patient("12345")

# Data harmonization
harmonizer = DataHarmonizer()
fhir_data = harmonizer.harmonize_to_fhir(hl7_data, "hl7v2", "Patient")

# Workflow orchestration
engine = WorkflowEngine()
instance_id = await engine.start_process("patient-admission", variables)
```

### 🔌 Plugin System (New!)

**Plug-and-Play Integration** for healthcare organizations:

```python
from pyheart import PluginManager, InsuranceAdapter, GovernmentAdapter, ProviderAdapter

# Initialize plugin manager
plugin_manager = PluginManager()

# Load insurance plugin for claims processing
insurance = InsuranceAdapter(config={
    "system_id": "acme_insurance",
    "base_url": "https://api.insurance.com",
    "api_key": "your-key"
})
plugin_manager.registry.register_plugin("insurance", insurance)

# Load government plugin for public health reporting
government = GovernmentAdapter(config={
    "system_id": "public_health",
    "agency_type": "public_health",
    "jurisdiction": "CA"
})
plugin_manager.registry.register_plugin("government", government)

# Start all plugins
await plugin_manager.start()

# Use plugins
await insurance.send_data("Claim", claim_data)
await government.send_data("PublicHealthCase", report_data)
```

**📖 See [QUICKSTART_PLUGINS.md](QUICKSTART_PLUGINS.md) for 5-minute quickstart or [PLUGINS.md](PLUGINS.md) for complete documentation.**

## 🏗️ Architecture

```
┌─────────────────────────────────────────┐
│         Clinical Applications           │
│    (EHR, Patient Portal, Mobile)       │
└──────────────┬──────────────────────────┘
               │
┌──────────────▼──────────────────────────┐
│           🧠 PyBrain                    │
│   AI • Analytics • Decision Support    │
└──────────────┬──────────────────────────┘
               │
┌──────────────▼──────────────────────────┐
│           ❤️ PyHeart                     │
│  Integration • Workflow • Security      │
└──────────────┬──────────────────────────┘
               │
┌──────────────▼──────────────────────────┐
│        Healthcare Systems              │
│  (FHIR, HL7, Legacy, IoT Devices)     │
└─────────────────────────────────────────┘
```

## 📂 Repository Structure

```
pybrain-pyheart/
├── pybrain-pkg/              # PyBrain Intelligence Package
│   ├── src/pybrain/
│   │   ├── core/
│   │   │   ├── ai.py         # AI engines and models
│   │   │   ├── harmonizer.py # Data harmonization
│   │   │   ├── analytics.py  # Population health analytics
│   │   │   ├── decision.py   # Clinical decision support
│   │   │   └── knowledge.py  # Medical knowledge graphs
│   │   └── cli.py            # Command-line interface
│   ├── tests/                # Comprehensive test suite
│   ├── README.md             # PyBrain documentation
│   └── pyproject.toml        # Package configuration
│
├── pyheart-pkg/              # PyHeart Integration Package
│   ├── src/pyheart/
│   │   ├── core/
│   │   │   ├── client.py     # FHIR and healthcare clients
│   │   │   ├── workflow.py   # Process orchestration
│   │   │   ├── integration.py # System adapters
│   │   │   ├── security.py   # Auth and compliance
│   │   │   └── server.py     # API gateway
│   │   └── cli.py            # Command-line interface
│   ├── tests/                # Comprehensive test suite
│   ├── README.md             # PyHeart documentation
│   └── pyproject.toml        # Package configuration
│
├── examples/
│   └── plugins/              # Plugin usage examples
│       ├── insurance_example.py    # Insurance company integration
│       ├── government_example.py   # Government office integration
│       ├── provider_example.py     # Healthcare provider integration
│       └── plugin_config.yaml      # Configuration example
├── build_and_publish.py      # Automated build script
├── PLUGINS.md                # Plugin system documentation
├── DEPLOYMENT_GUIDE.md       # Publication guide
├── PACKAGE_SUMMARY.md        # Complete overview
└── CLAUDE.md                 # Development context
```

## 🔌 Plugin System - Plug-and-Play SDK

PyHeart features a comprehensive plugin architecture that enables **zero-friction integration** for healthcare organizations. Pre-built plugins are available for:

### For Insurance Companies 🏥💼
- **Claims Processing**: Automated validation and submission
- **Eligibility Verification**: Real-time benefit checks
- **Prior Authorization**: Streamlined authorization workflows
- **Provider Networks**: Network directory management

### For Government Offices 🏛️
- **Public Health Reporting**: Automated notifiable disease reporting
- **Registry Management**: Immunization and quality registries
- **CMS Integration**: Quality measures and Medicare/Medicaid
- **Compliance**: Built-in regulatory compliance

### For Healthcare Providers 🏥
- **EHR Integration**: Connect to Epic, Cerner, Allscripts, etc.
- **Patient Engagement**: Automated reminders and follow-ups
- **Care Coordination**: Referral management and team collaboration
- **Clinical Workflows**: Pre-built clinical process automation

**Quick Example:**
```python
from pyheart import PluginManager, InsuranceAdapter

# Load and use insurance plugin in 5 lines
plugin_manager = PluginManager()
insurance = InsuranceAdapter(config={"system_id": "acme", "api_key": "key"})
plugin_manager.registry.register_plugin("insurance", insurance)
await plugin_manager.start()
await insurance.send_data("Claim", claim_data)  # Submit claim!
```

📖 **[Get Started in 5 Minutes →](QUICKSTART_PLUGINS.md)** | [Full Documentation →](PLUGINS.md) | [Examples →](examples/plugins/)

## 🛠️ Development

### Building Packages

```bash
# Automated build (recommended)
python build_and_publish.py

# Manual build
cd pybrain-pkg && python -m build
cd pyheart-pkg && python -m build
```

### Running Tests

```bash
# Test PyBrain
cd pybrain-pkg && python -m pytest tests/ -v

# Test PyHeart  
cd pyheart-pkg && python -m pytest tests/ -v
```

### CLI Tools

```bash
# PyBrain CLI
pybrain analyze -t "Clinical text to analyze"
pybrain harmonize -i data.json -f hl7v2 -r Patient
pybrain serve --port 8000

# PyHeart CLI
pyheart fhir -s https://server.com -r Patient -i 123
pyheart workflow -f process.json --watch
pyheart doctor  # System diagnostics
```

## 🌟 Key Features

### AI & Intelligence (PyBrain)
- **Clinical NLP**: Medical entity extraction and normalization
- **Risk Prediction**: Readmission, fall risk, medication adherence
- **Population Analytics**: Cohort analysis and trend identification  
- **Decision Rules**: Evidence-based clinical recommendations
- **Knowledge Graphs**: Medical concept relationships and reasoning

### Integration & Workflow (PyHeart)
- **FHIR R4 Support**: Full FHIR client with async/sync operations
- **Legacy Integration**: HL7v2, DICOM, X12 adapters
- **Process Automation**: Visual workflow designer compatibility
- **Multi-System**: Federated queries across healthcare systems
- **Security**: OAuth2, SMART on FHIR, audit logging

## 🔒 Security & Compliance

- **Encryption**: AES-256-GCM for data at rest and in transit
- **Authentication**: OAuth2, SMART on FHIR, multi-factor auth
- **Compliance**: HIPAA, GDPR, ISO27001 frameworks
- **Audit Logging**: Complete traceability for regulatory requirements
- **Access Control**: Role-based permissions and consent management

## 📚 Documentation

- [PyBrain README](pybrain-pkg/README.md) - AI and intelligence features
- [PyHeart README](pyheart-pkg/README.md) - Integration and workflow features  
- [Deployment Guide](DEPLOYMENT_GUIDE.md) - Publishing to PyPI
- [Package Summary](PACKAGE_SUMMARY.md) - Complete feature overview

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.

## 🌟 Acknowledgments

Built with ❤️ by the BrainSAIT Healthcare Innovation Lab

Special thanks to:
- The FHIR community for excellent healthcare standards
- Open-source healthcare initiatives worldwide
- All contributors and healthcare developers

## 🚀 Mission

**Democratizing healthcare development through intelligent integration.**

Our vision is a world where healthcare systems seamlessly communicate, AI enhances clinical decision-making, and developers can build life-saving applications in minutes instead of months.

---

**🩺 Together, we're building the future of connected healthcare. 🌍**
