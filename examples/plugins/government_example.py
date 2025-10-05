"""
Example: Government Office Plugin Usage

This example demonstrates how government healthcare offices can use PyHeart's
plugin system for public health reporting and registry management.
"""

import asyncio
from pyheart import (
    PluginManager,
    GovernmentAdapter,
    IntegrationHub
)
from pyheart.plugins.government import (
    PublicHealthReportingPlugin,
    ImmunizationRegistryPlugin
)


async def main():
    """Government office integration example"""
    
    print("=" * 60)
    print("Government Healthcare Office Plugin Example")
    print("=" * 60)
    print()
    
    # Initialize plugin manager
    plugin_manager = PluginManager()
    
    # Configure government adapter for public health department
    public_health_config = {
        "system_id": "state_public_health",
        "agency_type": "public_health",
        "base_url": "https://api.statepublichealth.gov",
        "jurisdiction": "CA",
        "reporting_format": "fhir"
    }
    
    # Load government plugin
    print("1. Loading government adapter plugin...")
    gov_adapter = GovernmentAdapter(config=public_health_config)
    plugin_manager.registry.register_plugin("state_public_health", gov_adapter)
    
    # Load public health reporting workflow plugin
    print("2. Loading public health reporting workflow...")
    ph_reporting = PublicHealthReportingPlugin(config={"jurisdiction": "CA"})
    plugin_manager.registry.register_plugin("ph_reporting", ph_reporting)
    
    # Load immunization registry plugin
    print("3. Loading immunization registry plugin...")
    imm_registry = ImmunizationRegistryPlugin()
    plugin_manager.registry.register_plugin("imm_registry", imm_registry)
    
    # Initialize all plugins
    print("4. Initializing plugins...")
    results = await plugin_manager.start()
    print(f"   Initialized {sum(results.values())} plugins successfully")
    
    # Example 1: Submit public health case report
    print("\n5. Submitting public health case report...")
    case_report = {
        "patient": "Patient/67890",
        "condition": "COVID-19",
        "onsetDate": "2024-01-10",
        "reportingProvider": "Practitioner/dr-smith",
        "severity": "moderate",
        "symptoms": ["fever", "cough", "fatigue"],
        "exposureHistory": "Community exposure"
    }
    
    adapter = plugin_manager.get_plugin("state_public_health")
    success = await adapter.send_data("PublicHealthCase", case_report)
    if success:
        print("✓ Public health case report submitted!")
    else:
        print("✗ Report submission failed!")
    
    # Example 2: Check if condition is reportable
    print("\n6. Checking reportable conditions...")
    ph_plugin = plugin_manager.get_plugin("ph_reporting")
    
    test_conditions = ["COVID-19", "Common Cold", "Measles", "Influenza"]
    for condition in test_conditions:
        is_reportable = ph_plugin.is_reportable(condition)
        status = "REPORTABLE" if is_reportable else "Not reportable"
        print(f"   {condition}: {status}")
    
    # Example 3: Generate automated report
    print("\n7. Generating public health report...")
    patient_data = {
        "id": "Patient/67890",
        "name": "Jane Doe",
        "age": 35,
        "provider": "Practitioner/dr-smith"
    }
    
    condition_data = {
        "code": "COVID-19",
        "onsetDateTime": "2024-01-10",
        "severity": "moderate"
    }
    
    report = await ph_plugin.generate_report(patient_data, condition_data)
    print(f"✓ Report generated for {report['condition']}")
    print(f"   Jurisdiction: {report['jurisdiction']}")
    print(f"   Status: {report['status']}")
    
    # Example 4: Submit immunization to registry
    print("\n8. Submitting immunization to registry...")
    immunization_data = {
        "vaccineCode": "COVID-19",
        "patient": "Patient/67890",
        "occurrenceDateTime": "2024-01-15",
        "lotNumber": "LOT-12345",
        "site": "Left arm",
        "route": "Intramuscular",
        "doseQuantity": {"value": 0.5, "unit": "mL"}
    }
    
    success = await adapter.send_data("Immunization", immunization_data)
    if success:
        print("✓ Immunization submitted to registry!")
    else:
        print("✗ Immunization submission failed!")
    
    # Example 5: Forecast immunizations
    print("\n9. Forecasting due immunizations...")
    imm_plugin = plugin_manager.get_plugin("imm_registry")
    
    immunization_history = [
        {"vaccineCode": "COVID-19"},
        {"vaccineCode": "Influenza"}
    ]
    
    recommendations = await imm_plugin.forecast_immunizations(
        "Patient/67890",
        immunization_history
    )
    
    if recommendations:
        print(f"✓ {len(recommendations)} immunization(s) recommended:")
        for rec in recommendations:
            print(f"   - {rec['vaccine']}: {rec['status']} (Due: {rec['dueDate']})")
    
    # Example 6: Submit quality measure report
    print("\n10. Submitting quality measure report...")
    quality_report = {
        "measure": "Measure/diabetes-hba1c-control",
        "period": {"start": "2024-01-01", "end": "2024-12-31"},
        "reporter": "Organization/clinic-001",
        "type": "summary",
        "improvementNotation": {
            "coding": [{
                "code": "increase",
                "display": "Increased score indicates improvement"
            }]
        },
        "group": [{
            "population": [
                {"count": 100, "code": "initial-population"},
                {"count": 85, "code": "numerator"},
                {"count": 95, "code": "denominator"}
            ]
        }]
    }
    
    success = await adapter.send_data("MeasureReport", quality_report)
    if success:
        print("✓ Quality measure report submitted!")
    else:
        print("✗ Quality measure submission failed!")
    
    # Integration with IntegrationHub
    print("\n11. Integrating with IntegrationHub...")
    hub = IntegrationHub()
    hub.register_adapter("state_public_health", adapter)
    await hub.connect_system("state_public_health", public_health_config)
    
    # List all plugins
    print("\n12. Listing all registered plugins...")
    all_plugins = plugin_manager.list_plugins()
    for plugin_meta in all_plugins:
        print(f"   - {plugin_meta.name} v{plugin_meta.version} ({plugin_meta.plugin_type.value})")
    
    # Cleanup
    print("\n13. Cleaning up...")
    await plugin_manager.stop()
    
    print("\n" + "=" * 60)
    print("Example completed successfully!")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())
