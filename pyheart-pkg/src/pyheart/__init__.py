"""
PyHeart - Healthcare Interoperability & Workflow Engine

Universal integration platform for seamless healthcare system connectivity,
workflow orchestration, and secure data exchange.
"""

from importlib import import_module
from typing import TYPE_CHECKING, Any, Dict, Tuple

import structlog

__version__ = "0.3.0"
__author__ = "BrainSAIT Healthcare Innovation Lab"
__email__ = "healthcare@brainsait.com"

if TYPE_CHECKING:
    from pyheart.core.client import ClientConfig, FHIRClient, HealthcareClient
    from pyheart.core.context import BrainSAITContext
    from pyheart.core.integration import Adapter, FHIRAdapter, HL7Adapter, IntegrationHub
    from pyheart.core.plugins import (
        Plugin,
        PluginManager,
        PluginMetadata,
        PluginRegistry,
        PluginType,
        get_plugin_manager,
    )
    from pyheart.core.security import AuthProvider, SecurityManager
    from pyheart.core.server import APIGateway, FHIRServer
    from pyheart.core.workflow import ProcessDefinition, Task, TaskStatus, TaskType, WorkflowEngine
    from pyheart.plugins import GovernmentAdapter, InsuranceAdapter, ProviderAdapter

__all__ = [
    "FHIRClient",
    "HealthcareClient",
    "ClientConfig",
    "BrainSAITContext",
    "FHIRServer",
    "APIGateway",
    "WorkflowEngine",
    "ProcessDefinition",
    "Task",
    "TaskStatus",
    "TaskType",
    "IntegrationHub",
    "Adapter",
    "FHIRAdapter",
    "HL7Adapter",
    "SecurityManager",
    "AuthProvider",
    "Plugin",
    "PluginManager",
    "PluginRegistry",
    "PluginType",
    "PluginMetadata",
    "get_plugin_manager",
    "InsuranceAdapter",
    "GovernmentAdapter",
    "ProviderAdapter",
]

_EXPORTS: Dict[str, Tuple[str, str]] = {
    "FHIRClient": ("pyheart.core.client", "FHIRClient"),
    "HealthcareClient": ("pyheart.core.client", "HealthcareClient"),
    "ClientConfig": ("pyheart.core.client", "ClientConfig"),
    "BrainSAITContext": ("pyheart.core.context", "BrainSAITContext"),
    "FHIRServer": ("pyheart.core.server", "FHIRServer"),
    "APIGateway": ("pyheart.core.server", "APIGateway"),
    "WorkflowEngine": ("pyheart.core.workflow", "WorkflowEngine"),
    "ProcessDefinition": ("pyheart.core.workflow", "ProcessDefinition"),
    "Task": ("pyheart.core.workflow", "Task"),
    "TaskStatus": ("pyheart.core.workflow", "TaskStatus"),
    "TaskType": ("pyheart.core.workflow", "TaskType"),
    "IntegrationHub": ("pyheart.core.integration", "IntegrationHub"),
    "Adapter": ("pyheart.core.integration", "Adapter"),
    "FHIRAdapter": ("pyheart.core.integration", "FHIRAdapter"),
    "HL7Adapter": ("pyheart.core.integration", "HL7Adapter"),
    "SecurityManager": ("pyheart.core.security", "SecurityManager"),
    "AuthProvider": ("pyheart.core.security", "AuthProvider"),
    "Plugin": ("pyheart.core.plugins", "Plugin"),
    "PluginManager": ("pyheart.core.plugins", "PluginManager"),
    "PluginRegistry": ("pyheart.core.plugins", "PluginRegistry"),
    "PluginType": ("pyheart.core.plugins", "PluginType"),
    "PluginMetadata": ("pyheart.core.plugins", "PluginMetadata"),
    "get_plugin_manager": ("pyheart.core.plugins", "get_plugin_manager"),
    "InsuranceAdapter": ("pyheart.plugins", "InsuranceAdapter"),
    "GovernmentAdapter": ("pyheart.plugins", "GovernmentAdapter"),
    "ProviderAdapter": ("pyheart.plugins", "ProviderAdapter"),
}


def __getattr__(name: str) -> Any:
    if name not in _EXPORTS:
        raise AttributeError(f"module 'pyheart' has no attribute {name!r}")

    module_name, attr_name = _EXPORTS[name]
    value = getattr(import_module(module_name), attr_name)
    globals()[name] = value
    return value


def __dir__() -> list[str]:
    return sorted(list(globals().keys()) + __all__)


structlog.configure(
    processors=[
        structlog.stdlib.filter_by_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.UnicodeDecoder(),
        structlog.processors.JSONRenderer(),
    ],
    context_class=dict,
    logger_factory=structlog.stdlib.LoggerFactory(),
    cache_logger_on_first_use=True,
)
