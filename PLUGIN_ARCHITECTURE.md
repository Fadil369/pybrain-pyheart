# 🏗️ PyHeart Plugin Architecture

## Overview

The PyHeart plugin architecture provides a modular, extensible framework that enables healthcare organizations to integrate their systems with minimal code. This document describes the technical architecture and design patterns used.

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────┐
│                        Healthcare Application                       │
│                     (Provider, Insurance, Government)               │
└────────────────────────────────┬────────────────────────────────────┘
                                 │
                                 │ Uses
                                 ▼
┌─────────────────────────────────────────────────────────────────────┐
│                         Plugin Manager                              │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │ • Plugin Discovery                                           │  │
│  │ • Configuration Loading (YAML, JSON, Dict)                  │  │
│  │ • Lifecycle Management (start, stop, cleanup)               │  │
│  │ • Error Handling & Logging                                  │  │
│  └──────────────────────────────────────────────────────────────┘  │
└────────────────────────────────┬────────────────────────────────────┘
                                 │
                                 │ Manages
                                 ▼
┌─────────────────────────────────────────────────────────────────────┐
│                         Plugin Registry                             │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │ • Plugin Catalog (metadata, versions, dependencies)         │  │
│  │ • Type Filtering (Adapter, Workflow, Transformer, etc.)     │  │
│  │ • Hook System (event-driven callbacks)                      │  │
│  │ • Priority Management                                        │  │
│  └──────────────────────────────────────────────────────────────┘  │
└────────────────────────────────┬────────────────────────────────────┘
                                 │
                                 │ Organizes
                                 ▼
┌─────────────────────────────────────────────────────────────────────┐
│                         Plugin Instances                            │
│  ┌───────────────┐  ┌───────────────┐  ┌──────────────────────┐   │
│  │   Adapters    │  │   Workflows   │  │   Other Plugins      │   │
│  ├───────────────┤  ├───────────────┤  ├──────────────────────┤   │
│  │ • Insurance   │  │ • Claims      │  │ • Transformers       │   │
│  │ • Government  │  │   Automation  │  │ • Validators         │   │
│  │ • Provider    │  │ • Public      │  │ • Authenticators     │   │
│  │ • FHIR        │  │   Health      │  │ • Notifiers          │   │
│  │ • HL7         │  │ • Care Coord  │  │                      │   │
│  │ • DICOM       │  │ • Patient     │  │                      │   │
│  │               │  │   Engagement  │  │                      │   │
│  └───────────────┘  └───────────────┘  └──────────────────────┘   │
└─────────────────────────────────────────────────────────────────────┘
                                 │
                                 │ Integrates with
                                 ▼
┌─────────────────────────────────────────────────────────────────────┐
│                    External Healthcare Systems                      │
│  ┌────────────┐  ┌──────────────┐  ┌─────────────────────────┐    │
│  │ Insurance  │  │ Government   │  │ Healthcare Providers    │    │
│  │ Systems    │  │ Agencies     │  │ (EHR/EMR Systems)       │    │
│  └────────────┘  └──────────────┘  └─────────────────────────┘    │
└─────────────────────────────────────────────────────────────────────┘
```

## Component Details

### 1. Plugin Base Class

All plugins inherit from the `Plugin` abstract base class:

```python
class Plugin(ABC):
    """Base class for all PyHeart plugins"""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or {}
        self.initialized = False
    
    @abstractmethod
    def get_metadata(self) -> PluginMetadata:
        """Return plugin metadata"""
        pass
    
    @abstractmethod
    async def initialize(self) -> bool:
        """Initialize the plugin"""
        pass
    
    @abstractmethod
    async def cleanup(self) -> bool:
        """Cleanup plugin resources"""
        pass
```

### 2. Plugin Metadata

Each plugin provides metadata describing its capabilities:

```python
@dataclass
class PluginMetadata:
    name: str                           # Plugin name
    version: str                        # Version number
    plugin_type: PluginType            # Type (Adapter, Workflow, etc.)
    description: str                    # Human-readable description
    author: str = ""                    # Plugin author
    dependencies: List[str] = []        # Required dependencies
    config_schema: Dict[str, Any] = {}  # Configuration schema
    enabled: bool = True                # Enable/disable flag
    priority: int = 100                 # Execution priority
```

### 3. Plugin Types

```python
class PluginType(Enum):
    ADAPTER = "adapter"              # System integration adapters
    WORKFLOW = "workflow"            # Automated workflow templates
    TRANSFORMER = "transformer"      # Data transformation plugins
    VALIDATOR = "validator"          # Data validation plugins
    AUTHENTICATOR = "authenticator"  # Authentication providers
    NOTIFIER = "notifier"           # Notification plugins
```

### 4. Plugin Registry

The registry manages the plugin lifecycle:

```python
class PluginRegistry:
    """Central registry for managing plugins"""
    
    def __init__(self):
        self.plugins: Dict[str, Plugin] = {}
        self.metadata: Dict[str, PluginMetadata] = {}
        self.plugin_hooks: Dict[str, List[Callable]] = {}
    
    def register_plugin(self, plugin_id: str, plugin: Plugin) -> bool
    def unregister_plugin(self, plugin_id: str) -> bool
    def get_plugin(self, plugin_id: str) -> Optional[Plugin]
    def get_plugins_by_type(self, plugin_type: PluginType) -> List[Plugin]
    def list_plugins(self) -> Dict[str, PluginMetadata]
    async def initialize_all(self) -> Dict[str, bool]
    async def cleanup_all(self) -> None
    def discover_plugins(self, package_name: str) -> int
```

### 5. Plugin Manager

High-level interface for working with plugins:

```python
class PluginManager:
    """High-level plugin management interface"""
    
    def __init__(self):
        self.registry = PluginRegistry()
    
    def load_plugin(self, plugin_class: Type[Plugin], 
                   plugin_id: str, config: Dict[str, Any]) -> bool
    def load_plugins_from_config(self, config: Dict[str, Any]) -> int
    async def start(self) -> None
    async def stop(self) -> None
    def get_plugin(self, plugin_id: str) -> Optional[Plugin]
    def list_plugins(self, plugin_type: Optional[PluginType]) -> List[PluginMetadata]
```

## Plugin Lifecycle

```
┌─────────────┐
│ Registration│ ← Plugin is registered with unique ID
└──────┬──────┘
       │
       ▼
┌─────────────┐
│ Validation  │ ← Configuration is validated
└──────┬──────┘
       │
       ▼
┌──────────────┐
│Initialization│ ← initialize() method is called
└──────┬───────┘
       │
       ▼
┌─────────────┐
│   Active    │ ← Plugin is ready to use
└──────┬──────┘
       │
       ▼
┌─────────────┐
│   Cleanup   │ ← cleanup() method is called
└─────────────┘
```

## Design Patterns

### 1. Abstract Factory Pattern

The plugin system uses the Abstract Factory pattern to create plugin instances:

```python
# Plugin classes are factories for creating instances
insurance_plugin = InsuranceAdapter(config={...})
government_plugin = GovernmentAdapter(config={...})
```

### 2. Registry Pattern

The PluginRegistry implements the Registry pattern for managing plugin instances:

```python
registry = PluginRegistry()
registry.register_plugin("my_plugin", plugin_instance)
plugin = registry.get_plugin("my_plugin")
```

### 3. Strategy Pattern

Plugins implement the Strategy pattern - different plugins provide different strategies for the same operations:

```python
# Different adapters, same interface
insurance.send_data("Claim", data)
government.send_data("PublicHealthCase", data)
provider.send_data("Patient", data)
```

### 4. Observer Pattern

The hook system implements the Observer pattern for event-driven behavior:

```python
# Register observer
registry.register_hook("data_received", callback_function)

# Notify observers
await registry.trigger_hook("data_received", data=data)
```

## Configuration Schema

Plugins define their configuration requirements using JSON Schema:

```python
config_schema = {
    "system_id": {
        "type": "string",
        "required": True,
        "description": "Unique system identifier"
    },
    "base_url": {
        "type": "string",
        "required": True,
        "pattern": "^https://.*"
    },
    "timeout": {
        "type": "integer",
        "default": 30,
        "minimum": 1,
        "maximum": 300
    }
}
```

## Security Considerations

### 1. Configuration Validation

All plugin configurations are validated before registration:

```python
def validate_config(self, config: Dict[str, Any]) -> bool:
    # Custom validation logic
    return True
```

### 2. Sandboxing

Plugins run in isolated contexts with limited permissions.

### 3. Credential Management

Sensitive credentials are never stored in code:

```yaml
config:
  api_key: "${INSURANCE_API_KEY}"  # Environment variable
```

### 4. Audit Logging

All plugin operations are logged using structured logging:

```python
logger.info("Plugin operation", 
           plugin_id=plugin_id,
           operation="send_data",
           resource_type=resource_type)
```

## Extension Points

### 1. Custom Plugins

Create custom plugins by inheriting from `Plugin`:

```python
class MyCustomPlugin(Plugin):
    def get_metadata(self) -> PluginMetadata:
        return PluginMetadata(...)
    
    async def initialize(self) -> bool:
        # Setup code
        return True
    
    async def cleanup(self) -> bool:
        # Cleanup code
        return True
```

### 2. Hook System

Register callbacks for custom events:

```python
def on_claim_submitted(claim_data):
    # Custom logic
    pass

registry.register_hook("claim_submitted", on_claim_submitted)
```

### 3. Plugin Discovery

Automatically discover plugins in packages:

```python
# Discovers all Plugin subclasses in the package
count = registry.discover_plugins("my_custom_plugins")
```

## Performance Considerations

### 1. Lazy Loading

Plugins are loaded on-demand, not at import time.

### 2. Async Operations

All I/O operations are asynchronous to prevent blocking:

```python
async def send_data(self, resource_type: str, data: Dict[str, Any]) -> bool:
    # Async implementation
    await asyncio.sleep(0)
    return True
```

### 3. Connection Pooling

Adapters maintain connection pools for better performance.

### 4. Caching

Frequently accessed data is cached to reduce API calls.

## Error Handling

### 1. Plugin-Level Errors

Plugins handle their own errors and return appropriate status:

```python
try:
    result = await plugin.send_data(resource_type, data)
except Exception as e:
    logger.error("Plugin operation failed", error=str(e))
    return False
```

### 2. System-Level Errors

The plugin manager catches and logs system-level errors:

```python
try:
    await plugin_manager.start()
except Exception as e:
    logger.error("Failed to start plugin manager", error=str(e))
```

## Testing Strategy

### 1. Unit Tests

Each plugin has comprehensive unit tests:

```python
@pytest.mark.asyncio
async def test_insurance_plugin():
    plugin = InsuranceAdapter(config={...})
    await plugin.initialize()
    result = await plugin.send_data("Claim", claim_data)
    assert result == True
```

### 2. Integration Tests

Test plugins working together:

```python
@pytest.mark.asyncio
async def test_complete_workflow():
    manager = PluginManager()
    # Load multiple plugins
    # Test workflow
```

### 3. Mock Adapters

Mock adapters for testing without external systems:

```python
class MockInsuranceAdapter(InsuranceAdapter):
    async def send_data(self, resource_type, data):
        return True  # Mock success
```

## Best Practices

### 1. Plugin Development

- **Single Responsibility**: Each plugin should do one thing well
- **Configuration Schema**: Always define configuration requirements
- **Error Handling**: Handle errors gracefully and return meaningful messages
- **Logging**: Use structured logging for all operations
- **Documentation**: Document all public methods and configuration options

### 2. Plugin Usage

- **Configuration Files**: Use YAML/JSON for configuration
- **Environment Variables**: Store credentials in environment variables
- **Error Checking**: Always check return values
- **Resource Cleanup**: Always call cleanup methods
- **Version Pinning**: Pin plugin versions in production

### 3. Security

- **Never hardcode credentials**
- **Validate all inputs**
- **Use HTTPS for all external connections**
- **Enable audit logging**
- **Follow principle of least privilege**

## Future Enhancements

### Planned Features

1. **Plugin Marketplace**: Central repository for community plugins
2. **Hot Reloading**: Update plugins without restarting
3. **Version Management**: Support multiple versions of the same plugin
4. **Dependency Resolution**: Automatic dependency installation
5. **Plugin Signing**: Cryptographic verification of plugin integrity
6. **Performance Monitoring**: Built-in performance metrics
7. **A/B Testing**: Support for testing different plugin versions

## Resources

- **Source Code**: `pyheart-pkg/src/pyheart/core/plugins.py`
- **Plugin Implementations**: `pyheart-pkg/src/pyheart/plugins/`
- **Examples**: `examples/plugins/`
- **Tests**: `pyheart-pkg/tests/test_plugins.py`
- **Documentation**: `PLUGINS.md`, `QUICKSTART_PLUGINS.md`

## Contributing

We welcome contributions! To contribute a plugin:

1. Fork the repository
2. Create your plugin following the architecture guidelines
3. Add tests and documentation
4. Submit a pull request

## License

Apache License 2.0 - See LICENSE file for details
