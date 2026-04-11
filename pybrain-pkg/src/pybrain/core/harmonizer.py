"""
Data Harmonization Engine - Transform healthcare data to unified formats
"""

from typing import Any, Dict, List, Optional, Union
from datetime import datetime, timezone
import json
from pydantic import BaseModel, Field
import logging

logger = logging.getLogger(__name__)


class MappingRule(BaseModel):
    """Rule for mapping data between formats"""
    
    source_field: str
    target_field: str
    transform: Optional[str] = None
    value_map: Optional[Dict[str, str]] = None


class DataHarmonizer:
    """
    Harmonize healthcare data from various formats to FHIR
    
    Supports:
    - HL7v2 to FHIR
    - CDA to FHIR
    - Custom EHR formats to FHIR
    - CSV/Excel to FHIR
    """
    
    def __init__(self):
        self.mapping_rules: Dict[str, List[MappingRule]] = {}
        self._load_default_mappings()
    
    def _load_default_mappings(self):
        """Load default mapping rules"""
        # HL7v2 to FHIR mappings
        self.mapping_rules["hl7v2_patient"] = [
            MappingRule(
                source_field="PID.5",
                target_field="name.family"
            ),
            MappingRule(
                source_field="PID.5.2",
                target_field="name.given"
            ),
            MappingRule(
                source_field="PID.7",
                target_field="birthDate",
                transform="parse_hl7_date"
            ),
            MappingRule(
                source_field="PID.8",
                target_field="gender",
                value_map={"M": "male", "F": "female", "O": "other"}
            )
        ]
    
    def harmonize_to_fhir(self, 
                         data: Dict[str, Any], 
                         source_format: str,
                         resource_type: str) -> Optional[Dict[str, Any]]:
        """
        Harmonize data to FHIR format
        
        Args:
            data: Source data to harmonize
            source_format: Format of source data (hl7v2, cda, csv, etc)
            resource_type: Target FHIR resource type
            
        Returns:
            FHIR resource dict or None if harmonization fails
        """
        try:
            if resource_type == "Patient":
                return self._harmonize_patient(data, source_format)
            elif resource_type == "Observation":
                return self._harmonize_observation(data, source_format)
            elif resource_type == "MedicationRequest":
                return self._harmonize_medication(data, source_format)
            else:
                logger.error("Unsupported resource type: %s", resource_type)
                return None
        except Exception as e:
            logger.error("Harmonization failed: %s", e)
            return None
    
    def _harmonize_patient(self, data: Dict[str, Any], source_format: str) -> Dict[str, Any]:
        """Harmonize patient data to FHIR Patient resource"""
        patient_data = {
            "resourceType": "Patient",
            "active": True,
            "communication": [],
            "extension": []
        }
        
        if source_format == "hl7v2":
            # Apply HL7v2 mappings
            pid_data = data.get("PID", {})
            family_name = pid_data.get("5", {}).get("1", "")
            given_name = pid_data.get("5", {}).get("2", "")
            arabic_name = pid_data.get("5", {}).get("8", "")
            patient_data["name"] = self._build_human_names(family_name, given_name, arabic_name)
            
            # Parse birth date
            if "7" in pid_data:
                patient_data["birthDate"] = self._parse_hl7_date(pid_data["7"])
            
            # Map gender
            gender_map = {"M": "male", "F": "female", "O": "other"}
            if "8" in pid_data:
                patient_data["gender"] = gender_map.get(pid_data["8"], "unknown")

            self._add_identifier(
                patient_data,
                pid_data.get("3", {}).get("1"),
                "http://brainsait.com/fhir/mrn",
                "MRN",
            )
            self._add_identifier(
                patient_data,
                pid_data.get("18", {}).get("1"),
                "http://brainsait.com/fhir/visit-number",
                "Visit Number",
            )

            preferred_language = pid_data.get("15", {}).get("1") or data.get("PV1", {}).get("2")
            self._add_language(patient_data, self._normalize_language(preferred_language))
        
        elif source_format == "csv" or source_format == "custom":
            # Direct mapping for CSV/custom data
            family_name = data.get("last_name", data.get("family_name", ""))
            given_name = data.get("first_name", data.get("given_name", ""))
            arabic_name = data.get("arabic_name", data.get("name_ar", ""))
            patient_data["name"] = self._build_human_names(family_name, given_name, arabic_name)
            patient_data["birthDate"] = data.get("birth_date", data.get("birthDate", ""))
            patient_data["gender"] = self._normalize_gender(data.get("gender", "unknown"))
            
            # Add identifier if present
            if data.get("mrn") or data.get("id"):
                self._add_identifier(
                    patient_data,
                    data.get("mrn", data.get("id", "")),
                    "http://brainsait.com/fhir/mrn",
                    "MRN",
                )
            self._add_identifier(
                patient_data,
                data.get("national_id"),
                "http://brainsait.com/fhir/national-id",
                "National ID",
            )
            self._add_identifier(
                patient_data,
                data.get("iqama"),
                "http://brainsait.com/fhir/iqama",
                "Iqama",
            )
            self._add_identifier(
                patient_data,
                data.get("passport_number"),
                "http://brainsait.com/fhir/passport",
                "Passport",
            )

            self._add_language(patient_data, self._normalize_language(data.get("preferred_language")))
            self._add_extension(
                patient_data,
                "https://brainsait.com/fhir/StructureDefinition/care-region",
                "valueCode",
                data.get("region"),
            )
            self._add_extension(
                patient_data,
                "https://brainsait.com/fhir/StructureDefinition/care-facility",
                "valueString",
                data.get("facility_id", data.get("facility")),
            )

        self._cleanup_patient_resource(patient_data)
        
        return patient_data
    
    def _harmonize_observation(self, data: Dict[str, Any], source_format: str) -> Dict[str, Any]:
        """Harmonize observation data to FHIR Observation resource"""
        obs_data = {
            "resourceType": "Observation",
            "status": "final",
            "code": {
                "coding": [{
                    "system": "http://loinc.org",
                    "code": data.get("code", ""),
                    "display": data.get("display", "")
                }]
            }
        }
        
        # Add value based on type
        if "value" in data:
            if isinstance(data["value"], (int, float)):
                obs_data["valueQuantity"] = {
                    "value": data["value"],
                    "unit": data.get("unit", ""),
                    "system": "http://unitsofmeasure.org"
                }
            else:
                obs_data["valueString"] = str(data["value"])
        
        # Add subject reference if patient ID provided
        if data.get("patient_id"):
            obs_data["subject"] = {"reference": f"Patient/{data['patient_id']}"}
        
        # Add effective date
        obs_data["effectiveDateTime"] = data.get("date", datetime.now(timezone.utc).isoformat())
        
        return obs_data
    
    def _harmonize_medication(self, data: Dict[str, Any], source_format: str) -> Dict[str, Any]:
        """Harmonize medication data to FHIR MedicationRequest resource"""
        med_data = {
            "resourceType": "MedicationRequest",
            "status": "active",
            "intent": "order",
            "medicationCodeableConcept": {
                "coding": [{
                    "system": "http://www.nlm.nih.gov/research/umls/rxnorm",
                    "code": data.get("code", ""),
                    "display": data.get("medication_name", "")
                }]
            },
            "dosageInstruction": [{
                "text": data.get("dosage_instructions", ""),
                "timing": {
                    "repeat": {
                        "frequency": data.get("frequency", 1),
                        "period": 1,
                        "periodUnit": "d"
                    }
                }
            }]
        }
        
        # Add subject reference if patient ID provided
        if data.get("patient_id"):
            med_data["subject"] = {"reference": f"Patient/{data['patient_id']}"}
        
        return med_data
    
    def _parse_hl7_date(self, date_str: str) -> str:
        """Parse HL7 date format to FHIR date"""
        try:
            # HL7 format: YYYYMMDD
            if len(date_str) >= 8:
                year = date_str[:4]
                month = date_str[4:6]
                day = date_str[6:8]
                return f"{year}-{month}-{day}"
            return date_str
        except Exception:
            return ""

    def _build_human_names(
        self,
        family_name: str,
        given_name: str,
        arabic_name: str = "",
    ) -> List[Dict[str, Any]]:
        names: List[Dict[str, Any]] = []
        if family_name or given_name:
            names.append({
                "use": "official",
                "family": family_name,
                "given": [value for value in [given_name] if value],
            })
        if arabic_name:
            names.append({
                "use": "usual",
                "text": arabic_name,
                "extension": [{
                    "url": "http://hl7.org/fhir/StructureDefinition/language",
                    "valueCode": "ar",
                }],
            })
        return names or [{"text": "Unknown"}]

    def _normalize_language(self, language: Optional[str]) -> Optional[str]:
        if not language:
            return None

        value = str(language).strip().lower()
        mappings = {
            "ar": "ar",
            "ara": "ar",
            "arabic": "ar",
            "en": "en",
            "eng": "en",
            "english": "en",
        }
        return mappings.get(value, value[:2])

    def _normalize_gender(self, gender: str) -> str:
        value = str(gender).strip().lower()
        mappings = {
            "m": "male",
            "male": "male",
            "f": "female",
            "female": "female",
            "o": "other",
            "other": "other",
        }
        return mappings.get(value, "unknown")

    def _add_identifier(
        self,
        patient_data: Dict[str, Any],
        value: Optional[str],
        system: str,
        label: str,
    ):
        if not value:
            return
        patient_data.setdefault("identifier", []).append(
            {
                "system": system,
                "value": value,
                "type": {"text": label},
            }
        )

    def _add_language(self, patient_data: Dict[str, Any], language_code: Optional[str]):
        if not language_code:
            return
        patient_data["communication"].append(
            {
                "language": {
                    "coding": [{
                        "system": "urn:ietf:bcp:47",
                        "code": language_code,
                    }]
                },
                "preferred": True,
            }
        )

    def _add_extension(
        self,
        patient_data: Dict[str, Any],
        url: str,
        value_key: str,
        value: Optional[str],
    ):
        if not value:
            return
        patient_data["extension"].append({"url": url, value_key: value})

    def _cleanup_patient_resource(self, patient_data: Dict[str, Any]):
        if not patient_data.get("communication"):
            patient_data.pop("communication", None)
        if not patient_data.get("extension"):
            patient_data.pop("extension", None)
    
    def add_custom_mapping(self, 
                          source_format: str,
                          resource_type: str,
                          rules: List[MappingRule]):
        """Add custom mapping rules"""
        key = f"{source_format}_{resource_type.lower()}"
        self.mapping_rules[key] = rules
        logger.info("Added %d mapping rules for %s", len(rules), key)


class FHIRMapper:
    """
    Advanced FHIR mapping with semantic understanding
    """
    
    def __init__(self, harmonizer: DataHarmonizer):
        self.harmonizer = harmonizer
        self.terminology_service = self._init_terminology_service()
    
    def _init_terminology_service(self) -> Dict[str, Any]:
        """Initialize terminology service for code mapping"""
        return {
            "icd10_to_snomed": {},
            "loinc_mappings": {},
            "rxnorm_mappings": {}
        }
    
    def map_with_semantics(self, 
                          data: Dict[str, Any],
                          source_format: str,
                          target_profile: str) -> Any:
        """
        Map data using semantic understanding and terminology services
        
        Args:
            data: Source data
            source_format: Format of source
            target_profile: Target FHIR profile
            
        Returns:
            Mapped FHIR resource with semantic enhancements
        """
        # First, do basic harmonization
        resource = self.harmonizer.harmonize_to_fhir(
            data, 
            source_format,
            target_profile.split("/")[-1]  # Extract resource type
        )
        
        if not resource:
            return None
        
        # Enhance with semantic mappings
        if resource.get("code") and resource["code"].get("coding"):
            # Map codes using terminology service
            enhanced_codings = self._enhance_codings(resource["code"]["coding"])
            resource["code"]["coding"] = enhanced_codings
        
        return resource
    
    def _enhance_codings(self, codings: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Enhance codings with additional terminology mappings"""
        enhanced = codings.copy()
        
        for coding in codings:
            system = coding.get("system", "")
            code = coding.get("code", "")
            
            # Add SNOMED mappings for ICD-10
            if "icd10" in system.lower():
                snomed_code = self.terminology_service["icd10_to_snomed"].get(code)
                if snomed_code:
                    enhanced.append({
                        "system": "http://snomed.info/sct",
                        "code": snomed_code,
                        "display": coding.get("display", "")
                    })
        
        return enhanced
