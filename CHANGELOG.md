# Changelog

All notable changes to PyBrain & PyHeart will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.3.0] - 2026-04-11

### Added
- **BrainSAIT Runtime Context**: Added `BrainSAITContext` so PyHeart clients and workflows can carry organization, facility, language, compliance, and workflow-profile metadata through requests and process execution.
- **FHIR Metadata Enrichment**: PyHeart resource create, update, async, and batch operations can now stamp BrainSAIT tags, extensions, and request headers without custom per-call glue code.
- **Workflow Context Propagation**: Workflow instances now persist BrainSAIT context, support dotted variable resolution, retain task outputs and statuses, and allow synchronous completion for orchestration-style flows.
- **Regional Patient Harmonization**: PyBrain now normalizes bilingual Arabic/English names, preferred language, regional identifiers, and facility/region extensions for BrainSAIT-aligned patient records.
- **Population Context Analytics**: PyBrain analytics now surface language and region distributions together with BrainSAIT-oriented care coordination recommendations.

### Changed
- **Package Distribution Names**: Updated primary installation documentation to use `brainsait-pybrain` and `brainsait-pyheart`, matching published package metadata.
- **Release Surface**: Aligned package metadata and exported versions on `0.3.0` and corrected the release workflow install snippet to strip the leading `v` from tags.

### Fixed
- **Import Safety**: Reworked `pybrain` and `pyheart` top-level exports to lazy-load optional modules so core client and analytics imports no longer require the full server and ML dependency stack at import time.

## [0.2.0] - 2026-04-11

### Added - PyHeart Plugin System
- **Plugin Architecture**: Full plug-and-play SDK with `Plugin`, `PluginManager`, `PluginRegistry`, and `PluginType` abstractions
- **Insurance Plugin**: `InsuranceAdapter` and `ClaimsAutomationPlugin` for claims processing, prior authorization, and eligibility verification
- **Government Plugin**: `GovernmentAdapter`, `PublicHealthReportingPlugin`, and `ImmunizationRegistryPlugin` for regulatory reporting
- **Provider Plugin**: `ProviderAdapter`, `CareCoordinationPlugin`, and `PatientEngagementPlugin` for EHR connectivity
- **Plugin Discovery**: Automatic plugin discovery from packages via `PluginRegistry.discover_plugins()`
- **Hook System**: Event-driven hooks with `register_hook` / `trigger_hook` for plugin-to-plugin communication
- **Plugin Documentation**: `PLUGINS.md`, `PLUGIN_ARCHITECTURE.md`, `QUICKSTART_PLUGINS.md`, and example scripts

### Fixed
- **Security (Critical)**: Replaced fake SHA-256 "encryption" in `EncryptionManager.encrypt_data()` with real AES-256-GCM via the `cryptography` library; `decrypt_data()` now correctly reverses the encryption
- **Bug**: `FHIRClient.close()` no longer calls `asyncio.create_task()` outside an async context (was a `RuntimeError`)
- **Bug**: `PluginRegistry.unregister_plugin()` no longer calls `asyncio.create_task()` outside an async context
- **Deprecation**: Replaced `datetime.utcnow()` (deprecated in Python 3.12) with `datetime.now(timezone.utc)` across all modules
- **Code Quality**: Replaced bare `except:` clauses with `except Exception:` in `harmonizer.py` and `analytics.py`
- **Code Quality**: Replaced f-string log calls with `%`-style parameterized logging in `harmonizer.py`
- **Import Order**: Moved `import logging` to the top of `pybrain/__init__.py`

### Changed
- **pyproject.toml (both)**: Updated GitHub URLs to `Fadil369/pybrain-pyheart`
- **pyproject.toml (both)**: Removed unused `setuptools-scm` from build requirements
- **pyproject.toml (pybrain)**: Updated `langchain` minimum version `>=0.0.200` → `>=0.2.0`
- **pyproject.toml (both)**: Added Python 3.12 classifier; build matrix updated to 3.9–3.12
- **release.yml**: Updated `actions/setup-python` `@v4` → `@v5`
- **release.yml**: Updated `actions/upload-artifact` / `download-artifact` `@v3` → `@v4`
- **release.yml**: Updated `softprops/action-gh-release` `@v1` → `@v2`
- **release.yml**: Fixed pip install command in release body (`pybrain` → `brainsait-pybrain`, `pyheart` → `brainsait-pyheart`)
- **release.yml**: Removed hardcoded `PYPI_API_TOKEN` from publish steps in favour of OIDC trusted publisher

## [0.1.0] - 2024-08-02

### Added - PyBrain (Intelligence Layer)
- **AI Engine**: Clinical NLP with medical entity extraction
- **Data Harmonization**: HL7v2, CDA, CSV to FHIR transformation
- **Predictive Analytics**: Risk assessment (readmission, fall, adherence)
- **Decision Support**: Clinical rule engine with evidence-based recommendations
- **Knowledge Graphs**: Medical concept relationships and patient similarity
- **Population Health**: Analytics and forecasting capabilities
- **CLI Tools**: Command-line interface for analysis and harmonization

### Added - PyHeart (Integration Layer)
- **FHIR Client**: Universal R4 client with async/sync operations
- **Workflow Engine**: Healthcare process orchestration with dependencies
- **Integration Hub**: Multi-system connectivity with adapters
- **Security Manager**: OAuth2, SMART on FHIR, audit logging
- **API Gateway**: RESTful interface for healthcare systems
- **Legacy Support**: HL7v2, DICOM, X12 adapters
- **CLI Tools**: System management and diagnostic utilities

### Added - Infrastructure
- **Testing**: Comprehensive test suites for both packages
- **Documentation**: Rich README files and deployment guides
- **Build System**: Modern Python packaging with pyproject.toml
- **CI/CD Ready**: GitHub Actions workflows prepared
- **Compliance**: HIPAA, GDPR frameworks implemented

### Security
- AES-256-GCM encryption for data protection
- Complete audit logging for compliance
- Role-based access controls
- Patient consent management

[0.3.0]: https://github.com/Fadil369/pybrain-pyheart/compare/v0.2.0...v0.3.0
[0.2.0]: https://github.com/Fadil369/pybrain-pyheart/compare/v0.1.0...v0.2.0
[0.1.0]: https://github.com/Fadil369/pybrain-pyheart/releases/tag/v0.1.0
