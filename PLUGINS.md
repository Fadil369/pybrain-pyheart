# 🔌 PyHeart Plugin System

## Overview

PyHeart's plugin architecture provides a **plug-and-play SDK** that enables healthcare organizations to seamlessly integrate their systems and automate workflows with minimal code. The plugin system is designed specifically for healthcare providers, insurance companies, and government offices.

## 🎯 Key Benefits

### For Healthcare Providers
- **EHR Integration Made Easy**: Connect to Epic, Cerner, Allscripts, or any FHIR-compliant system
- **Patient Engagement Automation**: Automated appointment reminders, medication adherence tracking
- **Care Coordination**: Streamlined referral management and care team collaboration
- **Clinical Workflows**: Pre-built workflows for common clinical processes

### For Insurance Companies
- **Claims Automation**: Validate and submit claims automatically with error checking
- **Real-time Eligibility**: Instant benefit verification and coverage checks
- **Prior Authorization**: Streamlined authorization workflow management
- **Network Management**: Provider directory integration and updates

### For Government Offices
- **Public Health Reporting**: Automated detection and reporting of notifiable conditions
- **Registry Management**: Immunization, disease, and quality measure registries
- **CMS Integration**: Quality reporting and Medicare/Medicaid claims processing
- **Compliance**: Built-in HIPAA, GDPR, and regulatory compliance

## 🏗️ Architecture

The plugin system consists of three main components:

```
┌─────────────────────────────────────────┐
│         Plugin Manager                  │
│  - Discovery & Registration             │
│  - Lifecycle Management                 │
│  - Configuration Loading                │
└────────────┬────────────────────────────┘
             │
┌────────────▼────────────────────────────┐
│         Plugin Registry                 │
│  - Plugin Catalog                       │
│  - Hook Management                      │
│  - Type Filtering                       │
└────────────┬────────────────────────────┘
             │
┌────────────▼────────────────────────────┐
│         Individual Plugins              │
│  - Adapters (System Integration)        │
│  - Workflows (Process Automation)       │
│  - Transformers (Data Conversion)       │
│  - Validators (Data Validation)         │
└─────────────────────────────────────────┘
```

## 📦 Plugin Types

### 1. Adapter Plugins
System integration adapters for connecting to external healthcare systems.

**Built-in Adapters:**
- `InsuranceAdapter` - Insurance company integration
- `GovernmentAdapter` - Government agency integration
- `ProviderAdapter` - Healthcare provider EHR integration
- `FHIRAdapter` - FHIR server integration
- `HL7Adapter` - HL7v2 system integration
- `DICOMAdapter` - Medical imaging system integration

### 2. Workflow Plugins
Automated workflow templates for common healthcare processes.

**Built-in Workflows:**
- `ClaimsAutomationPlugin` - Automated claims processing
- `PublicHealthReportingPlugin` - Public health surveillance
- `ImmunizationRegistryPlugin` - Immunization management
- `CareCoordinationPlugin` - Care coordination workflows
- `PatientEngagementPlugin` - Patient engagement automation

### 3. Transformer Plugins
Data transformation and format conversion plugins.

### 4. Validator Plugins
Data validation and business rule enforcement plugins.

### 5. Authenticator Plugins
Authentication and authorization provider plugins.

### 6. Notifier Plugins
Notification delivery plugins (email, SMS, push).

## 🚀 Quick Start

### 1. Basic Plugin Usage

```python
import asyncio
from pyheart import PluginManager, InsuranceAdapter

async def main():
    # Initialize plugin manager
    plugin_manager = PluginManager()
    
    # Configure and load plugin
    config = {
        "system_id": "my_insurance",
        "base_url": "https://api.insurance.com",
        "api_key": "your-api-key",
        "payer_id": "PAYER-001"
    }
    
    plugin = InsuranceAdapter(config=config)
    plugin_manager.registry.register_plugin("my_insurance", plugin)
    
    # Initialize plugins
    await plugin_manager.start()
    
    # Use the plugin
    adapter = plugin_manager.get_plugin("my_insurance")
    result = await adapter.send_data("Claim", claim_data)
    
    # Cleanup
    await plugin_manager.stop()

asyncio.run(main())
```

### 2. Configuration-Based Loading

Create a `plugins.yaml` configuration file:

```yaml
plugins:
  acme_insurance:
    class: "pyheart.plugins.insurance.InsuranceAdapter"
    enabled: true
    config:
      system_id: "acme_insurance"
      base_url: "https://api.acmeinsurance.com"
      api_key: "${INSURANCE_API_KEY}"
      payer_id: "ACME-001"
```

Load plugins from configuration:

```python
import asyncio
import yaml
from pyheart import PluginManager

async def main():
    with open('plugins.yaml', 'r') as f:
        config = yaml.safe_load(f)
    
    plugin_manager = PluginManager()
    plugin_manager.load_plugins_from_config(config)
    
    await plugin_manager.start()
    # Use plugins...
    await plugin_manager.stop()

asyncio.run(main())
```

### 3. Auto-Discovery

Automatically discover and load plugins from packages:

```python
from pyheart import get_plugin_manager

plugin_manager = get_plugin_manager()

# Discover plugins in a package
count = plugin_manager.registry.discover_plugins("pyheart.plugins")
print(f"Discovered {count} plugins")

# Discover custom plugins
count = plugin_manager.registry.discover_plugins("my_custom_plugins")
```

## 💼 Use Case Examples

### Insurance Company - Claims Processing

```python
from pyheart import PluginManager, InsuranceAdapter
from pyheart.plugins.insurance import ClaimsAutomationPlugin

async def process_claims():
    plugin_manager = PluginManager()
    
    # Load insurance adapter
    insurance = InsuranceAdapter(config={
        "system_id": "claims_system",
        "base_url": "https://api.claims.com",
        "api_key": "key"
    })
    plugin_manager.registry.register_plugin("claims_system", insurance)
    
    # Load claims automation workflow
    claims_auto = ClaimsAutomationPlugin()
    plugin_manager.registry.register_plugin("claims_automation", claims_auto)
    
    await plugin_manager.start()
    
    # Process claim
    claim_data = {...}
    
    # Validate claim first
    validation = await claims_auto.process_claim(claim_data)
    
    if validation["valid"]:
        # Submit to insurance system
        adapter = plugin_manager.get_plugin("claims_system")
        success = await adapter.send_data("Claim", claim_data)
    
    await plugin_manager.stop()
```

### Government Office - Public Health Reporting

```python
from pyheart import PluginManager, GovernmentAdapter
from pyheart.plugins.government import PublicHealthReportingPlugin

async def report_public_health():
    plugin_manager = PluginManager()
    
    # Load government adapter
    gov = GovernmentAdapter(config={
        "system_id": "public_health",
        "agency_type": "public_health",
        "base_url": "https://api.health.gov",
        "jurisdiction": "CA"
    })
    plugin_manager.registry.register_plugin("public_health", gov)
    
    # Load reporting workflow
    ph_reporting = PublicHealthReportingPlugin(config={"jurisdiction": "CA"})
    plugin_manager.registry.register_plugin("ph_reporting", ph_reporting)
    
    await plugin_manager.start()
    
    # Check if condition is reportable
    if ph_reporting.is_reportable("COVID-19"):
        # Generate report
        report = await ph_reporting.generate_report(patient_data, condition_data)
        
        # Submit to public health agency
        adapter = plugin_manager.get_plugin("public_health")
        await adapter.send_data("PublicHealthCase", report)
    
    await plugin_manager.stop()
```

### Healthcare Provider - EHR Integration

```python
from pyheart import PluginManager, ProviderAdapter
from pyheart.plugins.provider import PatientEngagementPlugin

async def manage_patients():
    plugin_manager = PluginManager()
    
    # Load EHR adapter
    ehr = ProviderAdapter(config={
        "system_id": "epic_ehr",
        "ehr_type": "epic",
        "base_url": "https://fhir.epic.com",
        "client_id": "client-id",
        "client_secret": "secret"
    })
    plugin_manager.registry.register_plugin("epic_ehr", ehr)
    
    # Load patient engagement workflow
    engagement = PatientEngagementPlugin()
    plugin_manager.registry.register_plugin("engagement", engagement)
    
    await plugin_manager.start()
    
    # Fetch patient data
    adapter = plugin_manager.get_plugin("epic_ehr")
    patients = await adapter.fetch_data("Patient", {"patient_id": "12345"})
    
    # Send appointment reminder
    await engagement.send_appointment_reminder("12345", appointment_data)
    
    # Check medication adherence
    medications = await adapter.fetch_data("MedicationRequest", {"patient_id": "12345"})
    adherence = await engagement.check_medication_adherence("12345", medications)
    
    await plugin_manager.stop()
```

## 🛠️ Creating Custom Plugins

### Step 1: Define Your Plugin Class

```python
from pyheart.core.plugins import Plugin, PluginMetadata, PluginType
from typing import Dict, Any

class MyCustomAdapter(Plugin):
    """Custom healthcare system adapter"""
    
    def get_metadata(self) -> PluginMetadata:
        return PluginMetadata(
            name="My Custom Adapter",
            version="1.0.0",
            plugin_type=PluginType.ADAPTER,
            description="Integration with custom healthcare system",
            author="Your Organization",
            dependencies=["httpx", "fhir.resources"],
            config_schema={
                "system_id": {"type": "string", "required": True},
                "api_url": {"type": "string", "required": True},
                "api_key": {"type": "string", "required": True}
            }
        )
    
    async def initialize(self) -> bool:
        """Initialize the plugin"""
        api_url = self.config.get("api_url")
        # Setup your connection, clients, etc.
        return True
    
    async def cleanup(self) -> bool:
        """Cleanup resources"""
        # Close connections, release resources
        return True
    
    # Add your custom methods
    async def fetch_data(self, resource_type: str, params: Dict[str, Any]):
        """Fetch data from your system"""
        # Implementation here
        pass
```

### Step 2: Register Your Plugin

```python
plugin_manager = PluginManager()

custom_plugin = MyCustomAdapter(config={
    "system_id": "my_system",
    "api_url": "https://api.mysystem.com",
    "api_key": "key"
})

plugin_manager.registry.register_plugin("my_system", custom_plugin)
await plugin_manager.start()
```

### Step 3: Use Your Plugin

```python
adapter = plugin_manager.get_plugin("my_system")
data = await adapter.fetch_data("Patient", {"id": "123"})
```

## 🔐 Security Best Practices

### 1. Credential Management
```python
import os

config = {
    "api_key": os.environ.get("API_KEY"),  # Use environment variables
    "client_secret": os.environ.get("CLIENT_SECRET")
}
```

### 2. Plugin Validation
```python
# The plugin system validates plugins before registration
# Override validate_config for custom validation
class SecurePlugin(Plugin):
    def validate_config(self, config: Dict[str, Any]) -> bool:
        if not config.get("api_key"):
            return False
        if len(config.get("api_key")) < 32:
            return False
        return True
```

### 3. Audit Logging
```python
# All plugin operations are automatically logged
# Plugin activities appear in structured logs
```

## 📋 Plugin Configuration Schema

Each plugin can define its configuration requirements:

```python
config_schema = {
    "system_id": {
        "type": "string",
        "required": True,
        "description": "Unique system identifier"
    },
    "base_url": {
        "type": "string",
        "required": True,
        "pattern": "^https://.*"
    },
    "timeout": {
        "type": "integer",
        "default": 30,
        "minimum": 1,
        "maximum": 300
    },
    "retry_enabled": {
        "type": "boolean",
        "default": True
    }
}
```

## 🔄 Plugin Lifecycle

1. **Registration**: Plugin is registered with the plugin manager
2. **Validation**: Configuration is validated against schema
3. **Initialization**: Plugin's `initialize()` method is called
4. **Active**: Plugin is ready to use
5. **Cleanup**: Plugin's `cleanup()` method is called on shutdown

## 🎣 Hooks and Events

Plugins can register hooks to react to system events:

```python
plugin_manager = PluginManager()

# Register a hook
def on_data_received(data):
    print(f"Data received: {data}")

plugin_manager.registry.register_hook("data_received", on_data_received)

# Trigger the hook
await plugin_manager.registry.trigger_hook("data_received", data={"patient_id": "123"})
```

## 📊 Plugin Discovery and Listing

```python
from pyheart import get_plugin_manager, PluginType

plugin_manager = get_plugin_manager()

# List all plugins
all_plugins = plugin_manager.list_plugins()
for plugin in all_plugins:
    print(f"{plugin.name} v{plugin.version}")

# List only adapter plugins
adapters = plugin_manager.list_plugins(plugin_type=PluginType.ADAPTER)

# Get plugins by type from registry
workflow_plugins = plugin_manager.registry.get_plugins_by_type(PluginType.WORKFLOW)
```

## 🧪 Testing Plugins

```python
import pytest
from pyheart import PluginManager
from my_plugins import MyCustomAdapter

@pytest.mark.asyncio
async def test_custom_plugin():
    plugin_manager = PluginManager()
    
    plugin = MyCustomAdapter(config={
        "system_id": "test",
        "api_url": "https://test.api.com",
        "api_key": "test-key"
    })
    
    # Register plugin
    success = plugin_manager.registry.register_plugin("test", plugin)
    assert success
    
    # Initialize
    await plugin_manager.start()
    
    # Test functionality
    adapter = plugin_manager.get_plugin("test")
    assert adapter is not None
    
    # Cleanup
    await plugin_manager.stop()
```

## 📚 Additional Resources

- **Examples**: See `examples/plugins/` for complete working examples
- **API Documentation**: Full API reference at https://pyheart.readthedocs.io
- **GitHub**: https://github.com/Fadil369/pybrain-pyheart
- **Support**: healthcare@brainsait.com

## 🤝 Contributing

We welcome custom plugins! To contribute:

1. Create your plugin following the guidelines above
2. Add tests and documentation
3. Submit a pull request with your plugin
4. Include example usage in your PR

## 📄 License

Apache License 2.0 - See LICENSE file for details
