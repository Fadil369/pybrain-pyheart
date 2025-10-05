"""
Complete Workflow Example: Healthcare Data Flow

This example demonstrates a complete healthcare workflow using all three plugin types:
1. Provider (EHR) - Detects a reportable condition
2. Government - Reports the condition to public health
3. Insurance - Processes associated claims

Scenario: A provider diagnoses a patient with COVID-19, triggering:
- Public health reporting to state agency
- Insurance claim for testing and treatment
- Patient engagement for follow-up care
"""

import asyncio
from pyheart import (
    PluginManager,
    InsuranceAdapter,
    GovernmentAdapter,
    ProviderAdapter
)
from pyheart.plugins.insurance import ClaimsAutomationPlugin
from pyheart.plugins.government import PublicHealthReportingPlugin
from pyheart.plugins.provider import PatientEngagementPlugin


async def complete_healthcare_workflow():
    """
    Complete healthcare workflow demonstrating plugin integration
    """
    
    print("=" * 80)
    print("COMPLETE HEALTHCARE WORKFLOW EXAMPLE")
    print("Scenario: COVID-19 Diagnosis and Management")
    print("=" * 80)
    print()
    
    # ========================================================================
    # SETUP: Initialize Plugin Manager and Load All Plugins
    # ========================================================================
    
    print("📦 STEP 1: Setting up plugin system...")
    plugin_manager = PluginManager()
    
    # Provider (EHR) Plugin
    print("  Loading provider (EHR) plugin...")
    provider = ProviderAdapter(config={
        "system_id": "hospital_ehr",
        "ehr_type": "epic",
        "base_url": "https://fhir.hospital.com",
        "client_id": "client-id",
        "client_secret": "secret"
    })
    plugin_manager.registry.register_plugin("ehr", provider)
    
    # Government Plugin
    print("  Loading government (public health) plugin...")
    government = GovernmentAdapter(config={
        "system_id": "state_health_dept",
        "agency_type": "public_health",
        "base_url": "https://api.health.state.gov",
        "jurisdiction": "CA"
    })
    plugin_manager.registry.register_plugin("government", government)
    
    # Insurance Plugin
    print("  Loading insurance plugin...")
    insurance = InsuranceAdapter(config={
        "system_id": "patient_insurance",
        "base_url": "https://api.insurance.com",
        "api_key": "insurance-api-key",
        "payer_id": "INS-001"
    })
    plugin_manager.registry.register_plugin("insurance", insurance)
    
    # Workflow Plugins
    print("  Loading workflow automation plugins...")
    ph_reporting = PublicHealthReportingPlugin(config={"jurisdiction": "CA"})
    claims_auto = ClaimsAutomationPlugin()
    patient_engage = PatientEngagementPlugin()
    
    plugin_manager.registry.register_plugin("ph_reporting", ph_reporting)
    plugin_manager.registry.register_plugin("claims_auto", claims_auto)
    plugin_manager.registry.register_plugin("patient_engage", patient_engage)
    
    # Initialize all plugins
    print("\n  Initializing all plugins...")
    results = await plugin_manager.start()
    print(f"  ✓ {sum(results.values())}/{len(results)} plugins initialized successfully")
    
    # ========================================================================
    # SCENARIO: Patient Visit and COVID-19 Diagnosis
    # ========================================================================
    
    print("\n" + "=" * 80)
    print("📋 STEP 2: Patient Visit - COVID-19 Diagnosis")
    print("=" * 80)
    
    # Patient information
    patient_id = "Patient/12345"
    patient_name = "Jane Doe"
    patient_email = "jane.doe@email.com"
    
    print(f"\n  Patient: {patient_name} (ID: {patient_id})")
    print("  Chief Complaint: Fever, cough, fatigue")
    print("  Diagnosis: COVID-19 (U07.1)")
    
    # Fetch patient data from EHR
    print("\n  Fetching patient data from EHR...")
    ehr = plugin_manager.get_plugin("ehr")
    patient_data = await ehr.fetch_data("Patient", {"patient_id": "12345"})
    
    if patient_data:
        print(f"  ✓ Patient record retrieved")
    
    # Document the encounter
    print("\n  Documenting clinical encounter in EHR...")
    encounter_data = {
        "status": "finished",
        "class": {"code": "AMB", "display": "ambulatory"},
        "type": [{"coding": [{"code": "185349003", "display": "Office visit"}]}],
        "subject": {"reference": patient_id},
        "period": {"start": "2024-01-15T09:00:00Z", "end": "2024-01-15T09:45:00Z"},
        "reasonCode": [{"text": "COVID-19 testing and diagnosis"}]
    }
    
    await ehr.send_data("Encounter", encounter_data)
    print("  ✓ Encounter documented")
    
    # ========================================================================
    # PUBLIC HEALTH REPORTING
    # ========================================================================
    
    print("\n" + "=" * 80)
    print("🏛️  STEP 3: Public Health Reporting")
    print("=" * 80)
    
    # Check if condition is reportable
    ph_plugin = plugin_manager.get_plugin("ph_reporting")
    
    if ph_plugin.is_reportable("COVID-19"):
        print("\n  ⚠️  COVID-19 is a reportable condition")
        
        # Generate public health report
        print("  Generating public health case report...")
        report = await ph_plugin.generate_report(
            patient_data={
                "id": patient_id,
                "name": patient_name,
                "age": 35,
                "provider": "Dr. Sarah Johnson"
            },
            condition_data={
                "code": "COVID-19",
                "onsetDateTime": "2024-01-13",
                "severity": "moderate"
            }
        )
        
        print(f"  ✓ Report generated")
        print(f"    - Jurisdiction: {report['jurisdiction']}")
        print(f"    - Condition: {report['condition']}")
        print(f"    - Onset Date: {report['onsetDate']}")
        
        # Submit to state health department
        print("\n  Submitting to state health department...")
        gov = plugin_manager.get_plugin("government")
        success = await gov.send_data("PublicHealthCase", report)
        
        if success:
            print("  ✓ Public health report submitted successfully")
        else:
            print("  ✗ Public health report submission failed")
    
    # ========================================================================
    # INSURANCE CLAIMS PROCESSING
    # ========================================================================
    
    print("\n" + "=" * 80)
    print("💼 STEP 4: Insurance Claims Processing")
    print("=" * 80)
    
    # Create claim for COVID-19 testing and treatment
    print("\n  Creating insurance claim...")
    claim_data = {
        "patient": patient_id,
        "provider": "Organization/hospital-001",
        "diagnosis": [
            {
                "coding": [{
                    "system": "http://hl7.org/fhir/sid/icd-10",
                    "code": "U07.1",
                    "display": "COVID-19"
                }]
            }
        ],
        "serviceDate": "2024-01-15",
        "totalCost": 750.00,
        "items": [
            {"service": "Office Visit - Level 4", "code": "99214", "cost": 200.00},
            {"service": "COVID-19 PCR Test", "code": "87635", "cost": 150.00},
            {"service": "Chest X-Ray", "code": "71046", "cost": 250.00},
            {"service": "Medications", "code": "MEDS", "cost": 150.00}
        ]
    }
    
    print(f"  Claim Details:")
    print(f"    - Total Cost: ${claim_data['totalCost']:.2f}")
    print(f"    - Services: {len(claim_data['items'])}")
    
    # Validate claim
    print("\n  Validating claim...")
    claims_plugin = plugin_manager.get_plugin("claims_auto")
    validation = await claims_plugin.process_claim(claim_data)
    
    if validation["valid"]:
        print("  ✓ Claim validation passed")
        
        # Submit to insurance
        print("\n  Submitting claim to insurance company...")
        ins = plugin_manager.get_plugin("insurance")
        success = await ins.send_data("Claim", claim_data)
        
        if success:
            print("  ✓ Claim submitted successfully")
            print("    - Claim will be processed within 24-48 hours")
        else:
            print("  ✗ Claim submission failed")
    else:
        print("  ✗ Claim validation failed:")
        for error in validation["errors"]:
            print(f"    - {error}")
    
    # Check eligibility
    print("\n  Verifying patient eligibility...")
    coverage = await ins.fetch_data("Coverage", {"patient_id": "12345"})
    
    if coverage:
        print(f"  ✓ Coverage confirmed")
        print(f"    - Status: {coverage[0]['status']}")
        print(f"    - Payer: {coverage[0]['payor'][0]['reference']}")
    
    # ========================================================================
    # PATIENT ENGAGEMENT
    # ========================================================================
    
    print("\n" + "=" * 80)
    print("📱 STEP 5: Patient Engagement & Follow-up")
    print("=" * 80)
    
    # Send isolation instructions
    print("\n  Sending patient education materials...")
    engage = plugin_manager.get_plugin("patient_engage")
    
    # Schedule follow-up appointment
    print("  Scheduling follow-up telemedicine appointment...")
    follow_up_data = {
        "start": "2024-01-22T10:00:00Z",
        "provider": "Dr. Sarah Johnson",
        "location": "Telemedicine",
        "type": "Follow-up"
    }
    
    success = await engage.send_appointment_reminder(patient_id.split("/")[1], follow_up_data)
    
    if success:
        print("  ✓ Follow-up appointment scheduled")
        print(f"    - Date: {follow_up_data['start']}")
        print(f"    - Type: {follow_up_data['type']}")
    
    # Submit prescription
    print("\n  Submitting prescription to pharmacy...")
    prescription = {
        "status": "active",
        "intent": "order",
        "medicationCodeableConcept": {
            "coding": [{
                "code": "PAXLOVID",
                "display": "Paxlovid (Nirmatrelvir/Ritonavir)"
            }]
        },
        "subject": {"reference": patient_id},
        "dosageInstruction": [{
            "text": "Take as directed for 5 days"
        }]
    }
    
    await ehr.send_data("MedicationRequest", prescription)
    print("  ✓ Prescription sent to pharmacy")
    
    # ========================================================================
    # SUMMARY
    # ========================================================================
    
    print("\n" + "=" * 80)
    print("📊 WORKFLOW SUMMARY")
    print("=" * 80)
    
    print(f"""
  ✓ Patient Diagnosis: COVID-19 confirmed and documented
  ✓ Public Health: Report submitted to state health department
  ✓ Insurance: Claim validated and submitted ($750.00)
  ✓ Patient Care: Follow-up scheduled and prescription sent
  
  All systems integrated seamlessly using PyHeart plugins!
  
  Active Plugins: {len(plugin_manager.list_plugins())}
  """)
    
    # List all active plugins
    print("  Active Plugin Details:")
    for plugin_meta in plugin_manager.list_plugins():
        print(f"    • {plugin_meta.name} v{plugin_meta.version} ({plugin_meta.plugin_type.value})")
    
    # ========================================================================
    # CLEANUP
    # ========================================================================
    
    print("\n" + "=" * 80)
    print("🧹 Cleaning up...")
    await plugin_manager.stop()
    print("✓ All plugins stopped successfully")
    print("=" * 80)
    
    print("\n✅ Workflow completed successfully!")
    print("\nThis example demonstrated:")
    print("  • Provider (EHR) integration for clinical documentation")
    print("  • Government reporting for public health surveillance")
    print("  • Insurance claims automation and eligibility verification")
    print("  • Patient engagement and care coordination")
    print("\nAll using PyHeart's plug-and-play plugin system! 🎉")


if __name__ == "__main__":
    asyncio.run(complete_healthcare_workflow())
