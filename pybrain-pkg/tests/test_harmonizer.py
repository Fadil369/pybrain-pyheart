"""Tests for data harmonizer."""

import pytest
from pybrain.core.harmonizer import DataHarmonizer


def test_harmonizer_initialization():
    """Test harmonizer initialization."""
    harmonizer = DataHarmonizer()
    assert "hl7v2_patient" in harmonizer.mapping_rules


def test_hl7v2_patient_harmonization():
    """Test HL7v2 patient data harmonization."""
    harmonizer = DataHarmonizer()
    
    hl7_data = {
        "PID": {
            "5": {"1": "Smith", "2": "John"},
            "7": "19800415",
            "8": "M"
        }
    }
    
    fhir_patient = harmonizer.harmonize_to_fhir(hl7_data, "hl7v2", "Patient")
    
    assert fhir_patient is not None
    assert fhir_patient["resourceType"] == "Patient"
    assert fhir_patient["name"][0]["family"] == "Smith"
    assert fhir_patient["name"][0]["given"][0] == "John"
    assert fhir_patient["birthDate"] == "1980-04-15"
    assert fhir_patient["gender"] == "male"


def test_csv_patient_harmonization():
    """Test CSV patient data harmonization."""
    harmonizer = DataHarmonizer()
    
    csv_data = {
        "first_name": "Jane",
        "last_name": "Doe",
        "birth_date": "1990-12-25",
        "gender": "female",
        "mrn": "MRN12345"
    }
    
    fhir_patient = harmonizer.harmonize_to_fhir(csv_data, "csv", "Patient")
    
    assert fhir_patient is not None
    assert fhir_patient["resourceType"] == "Patient"
    assert fhir_patient["name"][0]["family"] == "Doe"
    assert fhir_patient["name"][0]["given"][0] == "Jane"
    assert fhir_patient["gender"] == "female"
    assert fhir_patient["identifier"][0]["value"] == "MRN12345"


def test_brainsait_bilingual_patient_harmonization():
    """Test bilingual patient handling and regional BrainSAIT identifiers."""
    harmonizer = DataHarmonizer()

    custom_data = {
        "first_name": "Fatimah",
        "last_name": "Alotaibi",
        "arabic_name": "فاطمة العتيبي",
        "birth_date": "1992-07-14",
        "gender": "F",
        "mrn": "MRN-100",
        "national_id": "1029384756",
        "preferred_language": "Arabic",
        "region": "SA",
        "facility_id": "riyadh-main",
    }

    fhir_patient = harmonizer.harmonize_to_fhir(custom_data, "custom", "Patient")

    assert fhir_patient is not None
    assert len(fhir_patient["name"]) == 2
    assert fhir_patient["name"][1]["text"] == "فاطمة العتيبي"
    assert fhir_patient["identifier"][1]["value"] == "1029384756"
    assert fhir_patient["communication"][0]["language"]["coding"][0]["code"] == "ar"
    assert any(
        extension["url"].endswith("/care-region") and extension["valueCode"] == "SA"
        for extension in fhir_patient["extension"]
    )


def test_observation_harmonization():
    """Test observation data harmonization."""
    harmonizer = DataHarmonizer()
    
    obs_data = {
        "code": "2345-7",
        "display": "Glucose",
        "value": 120,
        "unit": "mg/dL",
        "patient_id": "12345"
    }
    
    fhir_obs = harmonizer.harmonize_to_fhir(obs_data, "custom", "Observation")
    
    assert fhir_obs is not None
    assert fhir_obs["resourceType"] == "Observation"
    assert fhir_obs["code"]["coding"][0]["code"] == "2345-7"
    assert fhir_obs["valueQuantity"]["value"] == 120
    assert fhir_obs["subject"]["reference"] == "Patient/12345"


def test_unsupported_resource_type():
    """Test handling of unsupported resource types."""
    harmonizer = DataHarmonizer()
    
    result = harmonizer.harmonize_to_fhir({}, "custom", "UnsupportedType")
    assert result is None
