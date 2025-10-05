"""
Example: Healthcare Provider Plugin Usage

This example demonstrates how healthcare providers can use PyHeart's
plugin system to integrate with EHR systems and automate workflows.
"""

import asyncio
from pyheart import (
    PluginManager,
    ProviderAdapter,
    WorkflowEngine,
    ProcessDefinition
)
from pyheart.plugins.provider import (
    CareCoordinationPlugin,
    PatientEngagementPlugin
)


async def main():
    """Healthcare provider integration example"""
    
    print("=" * 60)
    print("Healthcare Provider Plugin Example")
    print("=" * 60)
    print()
    
    # Initialize plugin manager
    plugin_manager = PluginManager()
    
    # Configure provider adapter for Epic EHR
    epic_config = {
        "system_id": "epic_ehr",
        "ehr_type": "epic",
        "base_url": "https://fhir.epic.com/interconnect-fhir-oauth",
        "client_id": "your-client-id",
        "client_secret": "your-client-secret",
        "practice_id": "PRAC-001"
    }
    
    # Load provider plugin
    print("1. Loading provider adapter plugin...")
    provider_adapter = ProviderAdapter(config=epic_config)
    plugin_manager.registry.register_plugin("epic_ehr", provider_adapter)
    
    # Load care coordination workflow plugin
    print("2. Loading care coordination workflow...")
    care_coord = CareCoordinationPlugin()
    plugin_manager.registry.register_plugin("care_coordination", care_coord)
    
    # Load patient engagement plugin
    print("3. Loading patient engagement workflow...")
    patient_engagement = PatientEngagementPlugin()
    plugin_manager.registry.register_plugin("patient_engagement", patient_engagement)
    
    # Initialize all plugins
    print("4. Initializing plugins...")
    await plugin_manager.start()
    
    # Example 1: Fetch patient data
    print("\n5. Fetching patient data from EHR...")
    adapter = plugin_manager.get_plugin("epic_ehr")
    
    patient_data = await adapter.fetch_data(
        "Patient",
        {"patient_id": "12345"}
    )
    
    if patient_data:
        patient = patient_data[0]
        print(f"✓ Retrieved patient: {patient.get('name', [{}])[0].get('given', [''])[0]} "
              f"{patient.get('name', [{}])[0].get('family', '')}")
    
    # Example 2: Fetch patient conditions
    print("\n6. Fetching patient conditions...")
    conditions = await adapter.fetch_data(
        "Condition",
        {"patient_id": "12345"}
    )
    
    if conditions:
        print(f"✓ Retrieved {len(conditions)} condition(s):")
        for condition in conditions:
            code = condition.get('code', {}).get('coding', [{}])[0]
            print(f"   - {code.get('display', 'Unknown condition')}")
    
    # Example 3: Fetch medications
    print("\n7. Fetching patient medications...")
    medications = await adapter.fetch_data(
        "MedicationRequest",
        {"patient_id": "12345"}
    )
    
    if medications:
        print(f"✓ Retrieved {len(medications)} medication(s):")
        for med in medications:
            med_code = med.get('medicationCodeableConcept', {}).get('coding', [{}])[0]
            print(f"   - {med_code.get('display', 'Unknown medication')}")
    
    # Example 4: Create a referral
    print("\n8. Creating specialist referral...")
    care_plugin = plugin_manager.get_plugin("care_coordination")
    
    referral = await care_plugin.create_referral(
        patient_data={"id": "12345", "name": "John Smith"},
        specialty="Cardiology",
        reason="Abnormal ECG findings, suspected arrhythmia"
    )
    
    if referral:
        print(f"✓ Referral created for {referral.get('specialty')}")
        print(f"   Reason: {referral.get('reasonCode', [{}])[0].get('text')}")
    
    # Example 5: Send appointment reminder
    print("\n9. Sending appointment reminder...")
    engagement_plugin = plugin_manager.get_plugin("patient_engagement")
    
    appointment_data = {
        "start": "2024-02-15T09:00:00Z",
        "provider": "Dr. Sarah Johnson",
        "location": "Main Clinic, Room 201"
    }
    
    success = await engagement_plugin.send_appointment_reminder(
        "12345",
        appointment_data
    )
    
    if success:
        print("✓ Appointment reminder sent successfully!")
    
    # Example 6: Check medication adherence
    print("\n10. Checking medication adherence...")
    adherence_report = await engagement_plugin.check_medication_adherence(
        "12345",
        medications
    )
    
    print(f"✓ Adherence report generated:")
    print(f"   Score: {adherence_report['adherence_score'] * 100:.1f}%")
    print(f"   Medications tracked: {adherence_report['medications_tracked']}")
    
    # Example 7: Schedule appointment
    print("\n11. Scheduling new appointment...")
    appointment_data = {
        "status": "proposed",
        "start": "2024-03-01T14:00:00Z",
        "end": "2024-03-01T14:30:00Z",
        "participant": [
            {"actor": {"reference": "Patient/12345"}},
            {"actor": {"reference": "Practitioner/dr-johnson"}}
        ],
        "appointmentType": {
            "coding": [{
                "code": "FOLLOWUP",
                "display": "Follow-up visit"
            }]
        }
    }
    
    success = await adapter.send_data("Appointment", appointment_data)
    if success:
        print("✓ Appointment scheduled successfully!")
    
    # Example 8: Submit lab order
    print("\n12. Submitting lab order...")
    lab_order = {
        "status": "active",
        "intent": "order",
        "code": {
            "coding": [{
                "system": "http://loinc.org",
                "code": "24331-1",
                "display": "Lipid panel"
            }]
        },
        "subject": {"reference": "Patient/12345"},
        "requester": {"reference": "Practitioner/dr-smith"},
        "reasonCode": [{
            "text": "Annual wellness exam"
        }]
    }
    
    success = await adapter.send_data("ServiceRequest", lab_order)
    if success:
        print("✓ Lab order submitted successfully!")
    
    # Example 9: Document clinical encounter
    print("\n13. Documenting clinical encounter...")
    encounter_data = {
        "status": "finished",
        "class": {
            "system": "http://terminology.hl7.org/CodeSystem/v3-ActCode",
            "code": "AMB",
            "display": "ambulatory"
        },
        "type": [{
            "coding": [{
                "system": "http://snomed.info/sct",
                "code": "185349003",
                "display": "Office visit"
            }]
        }],
        "subject": {"reference": "Patient/12345"},
        "period": {
            "start": "2024-01-15T09:00:00Z",
            "end": "2024-01-15T09:30:00Z"
        },
        "reasonCode": [{
            "text": "Annual physical examination"
        }]
    }
    
    success = await adapter.send_data("Encounter", encounter_data)
    if success:
        print("✓ Encounter documented successfully!")
    
    # Example 10: Workflow integration
    print("\n14. Creating automated care workflow...")
    workflow_engine = WorkflowEngine()
    
    # Define a patient follow-up workflow
    from pyheart.core.workflow import Task, TaskType
    
    follow_up_process = ProcessDefinition(
        id="patient-follow-up",
        name="Patient Follow-up Workflow",
        description="Automated patient follow-up after visit",
        tasks=[
            Task(
                id="send-reminder",
                name="Send appointment reminder",
                type=TaskType.NOTIFICATION,
                config={
                    "type": "email",
                    "recipient": "${patient_email}",
                    "template": "appointment-reminder"
                }
            ),
            Task(
                id="check-labs",
                name="Check for pending lab results",
                type=TaskType.API_CALL,
                dependencies=["send-reminder"],
                config={
                    "url": "${ehr_url}/Observation?patient=${patient_id}&status=pending",
                    "method": "GET"
                }
            )
        ]
    )
    
    workflow_engine.register_process(follow_up_process)
    print("✓ Patient follow-up workflow registered")
    
    # List all plugins
    print("\n15. Listing all registered plugins...")
    all_plugins = plugin_manager.list_plugins()
    for plugin_meta in all_plugins:
        print(f"   - {plugin_meta.name} v{plugin_meta.version} ({plugin_meta.plugin_type.value})")
    
    # Cleanup
    print("\n16. Cleaning up...")
    await plugin_manager.stop()
    
    print("\n" + "=" * 60)
    print("Example completed successfully!")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())
