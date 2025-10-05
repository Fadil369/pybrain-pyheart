"""
Example: Insurance Company Plugin Usage

This example demonstrates how insurance companies can use PyHeart's
plugin system to integrate their claims processing and eligibility systems.
"""

import asyncio
from pyheart import (
    PluginManager,
    InsuranceAdapter,
    IntegrationHub
)


async def main():
    """Insurance company integration example"""
    
    print("=" * 60)
    print("Insurance Company Plugin Example")
    print("=" * 60)
    print()
    
    # Initialize plugin manager
    plugin_manager = PluginManager()
    
    # Configure insurance adapter
    insurance_config = {
        "system_id": "acme_insurance",
        "base_url": "https://api.acmeinsurance.com",
        "api_key": "your-api-key-here",
        "payer_id": "ACME-001",
        "timeout": 30
    }
    
    # Load insurance plugin
    print("1. Loading insurance adapter plugin...")
    insurance_plugin = InsuranceAdapter(config=insurance_config)
    plugin_manager.registry.register_plugin("acme_insurance", insurance_plugin)
    
    # Initialize plugins
    print("2. Initializing plugins...")
    await plugin_manager.start()
    
    # Get the plugin
    insurance_adapter = plugin_manager.get_plugin("acme_insurance")
    
    # Example 1: Submit a claim
    print("\n3. Submitting insurance claim...")
    claim_data = {
        "patient": "Patient/12345",
        "provider": "Organization/hosp-001",
        "diagnosis": [
            {
                "coding": [{
                    "system": "http://hl7.org/fhir/sid/icd-10",
                    "code": "E11.9",
                    "display": "Type 2 diabetes mellitus"
                }]
            }
        ],
        "serviceDate": "2024-01-15",
        "totalCost": 1250.00,
        "items": [
            {
                "service": "Office Visit",
                "code": "99213",
                "cost": 150.00
            },
            {
                "service": "Lab Tests",
                "code": "80053",
                "cost": 100.00
            }
        ]
    }
    
    success = await insurance_adapter.send_data("Claim", claim_data)
    if success:
        print("✓ Claim submitted successfully!")
    else:
        print("✗ Claim submission failed!")
    
    # Example 2: Check eligibility
    print("\n4. Checking patient eligibility...")
    eligibility_request = {
        "patient": "Patient/12345",
        "service_type": "medical",
        "provider": "Organization/hosp-001"
    }
    
    success = await insurance_adapter.send_data(
        "CoverageEligibilityRequest",
        eligibility_request
    )
    if success:
        print("✓ Eligibility check completed!")
    else:
        print("✗ Eligibility check failed!")
    
    # Example 3: Fetch coverage information
    print("\n5. Fetching coverage information...")
    coverage_data = await insurance_adapter.fetch_data(
        "Coverage",
        {"patient_id": "12345"}
    )
    
    if coverage_data:
        print(f"✓ Retrieved {len(coverage_data)} coverage record(s)")
        for coverage in coverage_data:
            print(f"  - Status: {coverage.get('status')}")
            print(f"  - Period: {coverage.get('period')}")
    
    # Example 4: Request prior authorization
    print("\n6. Requesting prior authorization...")
    auth_request = {
        "patient": "Patient/12345",
        "service": "MRI Scan",
        "code": "70551",
        "diagnosis": "R51",
        "provider": "Organization/hosp-001"
    }
    
    success = await insurance_adapter.send_data(
        "PriorAuthorization",
        auth_request
    )
    if success:
        print("✓ Prior authorization requested!")
    else:
        print("✗ Prior authorization request failed!")
    
    # Integration with IntegrationHub
    print("\n7. Integrating with IntegrationHub...")
    hub = IntegrationHub()
    hub.register_adapter("acme_insurance", insurance_adapter)
    
    # Connect to the system
    await hub.connect_system("acme_insurance", insurance_config)
    
    # Fetch from hub
    claims = await hub.fetch_from_system(
        "acme_insurance",
        "Claim",
        {"claim_id": "CLM-12345"}
    )
    print(f"✓ Retrieved {len(claims)} claim(s) via IntegrationHub")
    
    # Cleanup
    print("\n8. Cleaning up...")
    await plugin_manager.stop()
    
    print("\n" + "=" * 60)
    print("Example completed successfully!")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())
