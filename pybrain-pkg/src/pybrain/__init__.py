"""
PyBrain - Unified Healthcare Intelligence Platform

AI-powered healthcare data harmonization, clinical NLP, and decision support
for building the next generation of intelligent healthcare systems.
"""

import logging
from importlib import import_module
from typing import TYPE_CHECKING, Any, Dict, Tuple

__version__ = "0.3.0"
__author__ = "BrainSAIT Healthcare Innovation Lab"
__email__ = "healthcare@brainsait.com"

if TYPE_CHECKING:
    from pybrain.core.ai import AIEngine, ModelRegistry
    from pybrain.core.analytics import AnalyticsEngine, HealthMetrics
    from pybrain.core.decision import ClinicalRules, DecisionEngine
    from pybrain.core.harmonizer import DataHarmonizer, FHIRMapper
    from pybrain.core.knowledge import KnowledgeGraph, MedicalOntology

__all__ = [
    "AIEngine",
    "ModelRegistry",
    "AnalyticsEngine",
    "HealthMetrics",
    "DecisionEngine",
    "ClinicalRules",
    "DataHarmonizer",
    "FHIRMapper",
    "KnowledgeGraph",
    "MedicalOntology",
]

_EXPORTS: Dict[str, Tuple[str, str]] = {
    "AIEngine": ("pybrain.core.ai", "AIEngine"),
    "ModelRegistry": ("pybrain.core.ai", "ModelRegistry"),
    "AnalyticsEngine": ("pybrain.core.analytics", "AnalyticsEngine"),
    "HealthMetrics": ("pybrain.core.analytics", "HealthMetrics"),
    "DecisionEngine": ("pybrain.core.decision", "DecisionEngine"),
    "ClinicalRules": ("pybrain.core.decision", "ClinicalRules"),
    "DataHarmonizer": ("pybrain.core.harmonizer", "DataHarmonizer"),
    "FHIRMapper": ("pybrain.core.harmonizer", "FHIRMapper"),
    "KnowledgeGraph": ("pybrain.core.knowledge", "KnowledgeGraph"),
    "MedicalOntology": ("pybrain.core.knowledge", "MedicalOntology"),
}


def __getattr__(name: str) -> Any:
    if name not in _EXPORTS:
        raise AttributeError(f"module 'pybrain' has no attribute {name!r}")

    module_name, attr_name = _EXPORTS[name]
    value = getattr(import_module(module_name), attr_name)
    globals()[name] = value
    return value


def __dir__() -> list[str]:
    return sorted(list(globals().keys()) + __all__)


logging.getLogger(__name__).addHandler(logging.NullHandler())
