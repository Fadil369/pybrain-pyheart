# 🚀 Quick Start: PyHeart Plugin System

Get started with PyHeart's plug-and-play SDK in **5 minutes**!

## 📋 Prerequisites

```bash
pip install pyheart
```

## 🏥 For Healthcare Providers

### Connect to Your EHR System

```python
import asyncio
from pyheart import PluginManager, ProviderAdapter

async def connect_to_ehr():
    # Step 1: Create plugin manager
    plugin_manager = PluginManager()
    
    # Step 2: Configure your EHR connection
    ehr_config = {
        "system_id": "my_epic",
        "ehr_type": "epic",  # or "cerner", "allscripts", etc.
        "base_url": "https://fhir.epic.com/interconnect-fhir-oauth",
        "client_id": "your-client-id",
        "client_secret": "your-client-secret"
    }
    
    # Step 3: Load the provider plugin
    ehr_plugin = ProviderAdapter(config=ehr_config)
    plugin_manager.registry.register_plugin("my_ehr", ehr_plugin)
    
    # Step 4: Initialize
    await plugin_manager.start()
    
    # Step 5: Use it!
    adapter = plugin_manager.get_plugin("my_ehr")
    
    # Fetch patient data
    patients = await adapter.fetch_data("Patient", {"patient_id": "12345"})
    print(f"Retrieved patient: {patients[0]['name']}")
    
    # Fetch medications
    meds = await adapter.fetch_data("MedicationRequest", {"patient_id": "12345"})
    print(f"Patient has {len(meds)} medications")
    
    # Cleanup
    await plugin_manager.stop()

# Run it
asyncio.run(connect_to_ehr())
```

### Automate Patient Engagement

```python
from pyheart.plugins.provider import PatientEngagementPlugin

async def automate_engagement():
    plugin_manager = PluginManager()
    
    # Load patient engagement plugin
    engagement = PatientEngagementPlugin()
    plugin_manager.registry.register_plugin("engagement", engagement)
    await plugin_manager.start()
    
    # Send appointment reminder
    await engagement.send_appointment_reminder(
        patient_id="12345",
        appointment_data={
            "start": "2024-02-15T09:00:00Z",
            "provider": "Dr. Smith",
            "location": "Main Clinic, Room 201"
        }
    )
    
    # Check medication adherence
    adherence = await engagement.check_medication_adherence(
        patient_id="12345",
        medications=patient_medications
    )
    
    print(f"Adherence score: {adherence['adherence_score'] * 100:.1f}%")
    
    await plugin_manager.stop()
```

## 💼 For Insurance Companies

### Automate Claims Processing

```python
import asyncio
from pyheart import PluginManager, InsuranceAdapter
from pyheart.plugins.insurance import ClaimsAutomationPlugin

async def process_claims():
    plugin_manager = PluginManager()
    
    # Step 1: Configure insurance connection
    insurance_config = {
        "system_id": "my_insurance",
        "base_url": "https://api.insurance.com",
        "api_key": "your-api-key",
        "payer_id": "INS-001"
    }
    
    # Step 2: Load plugins
    insurance = InsuranceAdapter(config=insurance_config)
    claims_automation = ClaimsAutomationPlugin()
    
    plugin_manager.registry.register_plugin("insurance", insurance)
    plugin_manager.registry.register_plugin("claims_auto", claims_automation)
    
    await plugin_manager.start()
    
    # Step 3: Process a claim
    claim_data = {
        "patient": "Patient/12345",
        "provider": "Organization/hosp-001",
        "diagnosis": [{"code": "E11.9", "display": "Type 2 diabetes"}],
        "serviceDate": "2024-01-15",
        "totalCost": 1250.00
    }
    
    # Validate claim
    claims_plugin = plugin_manager.get_plugin("claims_auto")
    validation = await claims_plugin.process_claim(claim_data)
    
    if validation["valid"]:
        # Submit to insurance system
        adapter = plugin_manager.get_plugin("insurance")
        success = await adapter.send_data("Claim", claim_data)
        print(f"Claim submitted: {success}")
    else:
        print(f"Claim validation failed: {validation['errors']}")
    
    await plugin_manager.stop()

asyncio.run(process_claims())
```

### Check Patient Eligibility

```python
async def check_eligibility():
    plugin_manager = PluginManager()
    
    insurance = InsuranceAdapter(config={
        "system_id": "insurance",
        "base_url": "https://api.insurance.com",
        "api_key": "your-key",
        "payer_id": "INS-001"
    })
    
    plugin_manager.registry.register_plugin("insurance", insurance)
    await plugin_manager.start()
    
    # Check eligibility
    adapter = plugin_manager.get_plugin("insurance")
    eligibility_request = {
        "patient": "Patient/12345",
        "service_type": "medical",
        "provider": "Organization/hosp-001"
    }
    
    success = await adapter.send_data(
        "CoverageEligibilityRequest",
        eligibility_request
    )
    
    print(f"Eligibility check: {success}")
    
    # Fetch coverage details
    coverage = await adapter.fetch_data("Coverage", {"patient_id": "12345"})
    print(f"Coverage status: {coverage[0]['status']}")
    
    await plugin_manager.stop()
```

## 🏛️ For Government Offices

### Automate Public Health Reporting

```python
import asyncio
from pyheart import PluginManager, GovernmentAdapter
from pyheart.plugins.government import PublicHealthReportingPlugin

async def report_public_health():
    plugin_manager = PluginManager()
    
    # Step 1: Configure government connection
    gov_config = {
        "system_id": "public_health",
        "agency_type": "public_health",
        "base_url": "https://api.health.gov",
        "jurisdiction": "CA"
    }
    
    # Step 2: Load plugins
    government = GovernmentAdapter(config=gov_config)
    ph_reporting = PublicHealthReportingPlugin(config={"jurisdiction": "CA"})
    
    plugin_manager.registry.register_plugin("government", government)
    plugin_manager.registry.register_plugin("ph_reporting", ph_reporting)
    
    await plugin_manager.start()
    
    # Step 3: Check if condition is reportable
    ph_plugin = plugin_manager.get_plugin("ph_reporting")
    
    if ph_plugin.is_reportable("COVID-19"):
        # Generate report
        report = await ph_plugin.generate_report(
            patient_data={
                "id": "Patient/67890",
                "name": "Jane Doe",
                "provider": "Dr. Smith"
            },
            condition_data={
                "code": "COVID-19",
                "onsetDateTime": "2024-01-10",
                "severity": "moderate"
            }
        )
        
        # Submit to public health agency
        adapter = plugin_manager.get_plugin("government")
        success = await adapter.send_data("PublicHealthCase", report)
        print(f"Report submitted: {success}")
    
    await plugin_manager.stop()

asyncio.run(report_public_health())
```

### Manage Immunization Registry

```python
from pyheart.plugins.government import ImmunizationRegistryPlugin

async def manage_immunizations():
    plugin_manager = PluginManager()
    
    # Load plugins
    government = GovernmentAdapter(config={
        "system_id": "registry",
        "agency_type": "state_registry",
        "base_url": "https://api.registry.gov",
        "jurisdiction": "CA"
    })
    
    imm_registry = ImmunizationRegistryPlugin()
    
    plugin_manager.registry.register_plugin("government", government)
    plugin_manager.registry.register_plugin("imm_registry", imm_registry)
    
    await plugin_manager.start()
    
    # Submit immunization to registry
    adapter = plugin_manager.get_plugin("government")
    immunization_data = {
        "vaccineCode": "COVID-19",
        "patient": "Patient/67890",
        "occurrenceDateTime": "2024-01-15",
        "lotNumber": "LOT-12345"
    }
    
    await adapter.send_data("Immunization", immunization_data)
    
    # Forecast due immunizations
    imm_plugin = plugin_manager.get_plugin("imm_registry")
    recommendations = await imm_plugin.forecast_immunizations(
        "Patient/67890",
        immunization_history=[{"vaccineCode": "COVID-19"}]
    )
    
    print(f"Due immunizations: {len(recommendations)}")
    for rec in recommendations:
        print(f"  - {rec['vaccine']}: {rec['status']}")
    
    await plugin_manager.stop()
```

## ⚙️ Configuration-Based Setup

Instead of code, use a YAML configuration file:

**plugins.yaml:**
```yaml
plugins:
  my_insurance:
    class: "pyheart.plugins.insurance.InsuranceAdapter"
    enabled: true
    config:
      system_id: "my_insurance"
      base_url: "https://api.insurance.com"
      api_key: "${INSURANCE_API_KEY}"
      payer_id: "INS-001"
  
  my_ehr:
    class: "pyheart.plugins.provider.ProviderAdapter"
    enabled: true
    config:
      system_id: "my_ehr"
      ehr_type: "epic"
      base_url: "https://fhir.epic.com"
      client_id: "${EHR_CLIENT_ID}"
      client_secret: "${EHR_CLIENT_SECRET}"
```

**Load and use:**
```python
import asyncio
import yaml
from pyheart import PluginManager

async def main():
    # Load config
    with open('plugins.yaml', 'r') as f:
        config = yaml.safe_load(f)
    
    # Load plugins from config
    plugin_manager = PluginManager()
    plugin_manager.load_plugins_from_config(config)
    
    # Start plugins
    await plugin_manager.start()
    
    # Use any plugin
    insurance = plugin_manager.get_plugin("my_insurance")
    ehr = plugin_manager.get_plugin("my_ehr")
    
    # ... your code here ...
    
    await plugin_manager.stop()

asyncio.run(main())
```

## 🔧 Common Operations

### List All Plugins
```python
plugins = plugin_manager.list_plugins()
for plugin_meta in plugins:
    print(f"{plugin_meta.name} v{plugin_meta.version} ({plugin_meta.plugin_type.value})")
```

### Filter by Type
```python
from pyheart import PluginType

# Get only adapter plugins
adapters = plugin_manager.list_plugins(plugin_type=PluginType.ADAPTER)

# Get only workflow plugins
workflows = plugin_manager.list_plugins(plugin_type=PluginType.WORKFLOW)
```

### Check Plugin Status
```python
plugin = plugin_manager.get_plugin("my_insurance")
if plugin.initialized:
    print("Plugin is ready to use")
```

## 🎓 Next Steps

1. **Read the full documentation**: [PLUGINS.md](PLUGINS.md)
2. **Explore examples**: [examples/plugins/](examples/plugins/)
3. **Create custom plugins**: See the "Creating Custom Plugins" section in PLUGINS.md
4. **Join the community**: GitHub Discussions and Issues

## 🆘 Getting Help

- **Documentation**: https://pyheart.readthedocs.io
- **Examples**: `examples/plugins/` directory
- **GitHub Issues**: https://github.com/Fadil369/pybrain-pyheart/issues
- **Email**: healthcare@brainsait.com

## 📄 License

Apache License 2.0 - See LICENSE file for details
