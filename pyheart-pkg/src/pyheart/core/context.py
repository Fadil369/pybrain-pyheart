"""
BrainSAIT runtime context models for client and workflow coordination.
"""

from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class BrainSAITContext(BaseModel):
    """Operational context shared across BrainSAIT healthcare workflows."""

    organization: str = "BrainSAIT"
    region: str = "SA"
    locale: str = "en-SA"
    preferred_language: str = "en"
    workflow_profile: str = "brainsait-standard"
    facility_id: Optional[str] = None
    facility_name: Optional[str] = None
    care_unit: Optional[str] = None
    deployment_id: Optional[str] = None
    compliance_profiles: List[str] = Field(
        default_factory=lambda: ["HIPAA", "PDPL"]
    )
    metadata: Dict[str, Any] = Field(default_factory=dict)

    def to_headers(self) -> Dict[str, str]:
        """Render context as outbound request headers."""
        headers = {
            "X-BrainSAIT-Organization": self.organization,
            "X-BrainSAIT-Region": self.region,
            "X-BrainSAIT-Locale": self.locale,
            "X-BrainSAIT-Language": self.preferred_language,
            "X-BrainSAIT-Workflow-Profile": self.workflow_profile,
            "X-BrainSAIT-Compliance": ",".join(self.compliance_profiles),
        }

        optional_headers = {
            "X-BrainSAIT-Facility-ID": self.facility_id,
            "X-BrainSAIT-Facility-Name": self.facility_name,
            "X-BrainSAIT-Care-Unit": self.care_unit,
            "X-BrainSAIT-Deployment-ID": self.deployment_id,
        }
        headers.update({key: value for key, value in optional_headers.items() if value})
        return headers

    def enrich_variables(self, variables: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Expose context through workflow variables."""
        enriched = dict(variables or {})
        context_payload = self.model_dump(exclude_none=True)

        enriched.setdefault("brainsait_context", context_payload)
        enriched.setdefault("organization", self.organization)
        enriched.setdefault("region", self.region)
        enriched.setdefault("locale", self.locale)
        enriched.setdefault("preferred_language", self.preferred_language)
        enriched.setdefault("workflow_profile", self.workflow_profile)
        enriched.setdefault("compliance_profiles", list(self.compliance_profiles))

        if self.facility_id:
            enriched.setdefault("facility_id", self.facility_id)
        if self.facility_name:
            enriched.setdefault("facility_name", self.facility_name)
        if self.care_unit:
            enriched.setdefault("care_unit", self.care_unit)
        if self.deployment_id:
            enriched.setdefault("deployment_id", self.deployment_id)

        return enriched

    def apply_to_resource(self, resource: Dict[str, Any]) -> Dict[str, Any]:
        """Add BrainSAIT metadata to an outbound FHIR resource."""
        updated = dict(resource)

        meta = dict(updated.get("meta", {}))
        profiles = list(meta.get("profile", []))
        brainsait_profile = "https://brainsait.com/fhir/StructureDefinition/managed-resource"
        if brainsait_profile not in profiles:
            profiles.append(brainsait_profile)

        tags = list(meta.get("tag", []))
        tags.extend(
            [
                {
                    "system": "https://brainsait.com/fhir/tags/organization",
                    "code": self.organization,
                    "display": self.organization,
                },
                {
                    "system": "https://brainsait.com/fhir/tags/region",
                    "code": self.region,
                    "display": self.region,
                },
            ]
        )
        if self.facility_id:
            tags.append(
                {
                    "system": "https://brainsait.com/fhir/tags/facility",
                    "code": self.facility_id,
                    "display": self.facility_name or self.facility_id,
                }
            )

        meta["profile"] = profiles
        meta["tag"] = tags
        updated["meta"] = meta

        extensions = list(updated.get("extension", []))
        for extension in self._resource_extensions():
            if not any(existing.get("url") == extension["url"] for existing in extensions):
                extensions.append(extension)
        if extensions:
            updated["extension"] = extensions

        return updated

    def _resource_extensions(self) -> List[Dict[str, Any]]:
        extensions = [
            {
                "url": "https://brainsait.com/fhir/StructureDefinition/preferred-language",
                "valueCode": self.preferred_language,
            },
            {
                "url": "https://brainsait.com/fhir/StructureDefinition/locale",
                "valueCode": self.locale,
            },
            {
                "url": "https://brainsait.com/fhir/StructureDefinition/workflow-profile",
                "valueString": self.workflow_profile,
            },
        ]

        optional_extensions = [
            (
                "https://brainsait.com/fhir/StructureDefinition/facility-id",
                "valueString",
                self.facility_id,
            ),
            (
                "https://brainsait.com/fhir/StructureDefinition/facility-name",
                "valueString",
                self.facility_name,
            ),
            (
                "https://brainsait.com/fhir/StructureDefinition/care-unit",
                "valueString",
                self.care_unit,
            ),
            (
                "https://brainsait.com/fhir/StructureDefinition/deployment-id",
                "valueString",
                self.deployment_id,
            ),
        ]

        for url, value_key, value in optional_extensions:
            if value:
                extensions.append({"url": url, value_key: value})

        return extensions
