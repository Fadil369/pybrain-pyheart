"""
PyHeart Plugins Package

Pre-built plugins for common healthcare use cases:
- Provider integrations
- Insurance company adapters  
- Government office connectors
- Automation workflows
"""

from pyheart.plugins.insurance import InsuranceAdapter
from pyheart.plugins.government import GovernmentAdapter
from pyheart.plugins.provider import ProviderAdapter

__all__ = [
    "InsuranceAdapter",
    "GovernmentAdapter", 
    "ProviderAdapter",
]
