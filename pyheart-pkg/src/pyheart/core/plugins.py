"""
Plugin system for PyHeart - Enable plug-and-play integrations

This module provides a flexible plugin architecture that allows healthcare
providers, insurance companies, and government offices to easily extend
PyHeart with custom adapters, workflows, and automations.
"""

from typing import Any, Dict, List, Optional, Type, Callable
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum
import importlib
import pkgutil
import inspect
import structlog

logger = structlog.get_logger()


class PluginType(Enum):
    """Types of plugins supported"""
    ADAPTER = "adapter"  # Healthcare system adapters
    WORKFLOW = "workflow"  # Automated workflow templates
    TRANSFORMER = "transformer"  # Data transformation plugins
    VALIDATOR = "validator"  # Data validation plugins
    AUTHENTICATOR = "authenticator"  # Authentication providers
    NOTIFIER = "notifier"  # Notification plugins


@dataclass
class PluginMetadata:
    """Metadata for a plugin"""
    name: str
    version: str
    plugin_type: PluginType
    description: str
    author: str = ""
    dependencies: List[str] = field(default_factory=list)
    config_schema: Dict[str, Any] = field(default_factory=dict)
    enabled: bool = True
    priority: int = 100  # Lower number = higher priority


class Plugin(ABC):
    """
    Base class for all PyHeart plugins
    
    All plugins must inherit from this class and implement the required methods.
    """
    
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
    
    def validate_config(self, config: Dict[str, Any]) -> bool:
        """Validate plugin configuration"""
        # Override in subclass for custom validation
        return True


class PluginRegistry:
    """
    Central registry for managing plugins
    
    Handles plugin discovery, loading, validation, and lifecycle management.
    """
    
    def __init__(self):
        self.plugins: Dict[str, Plugin] = {}
        self.metadata: Dict[str, PluginMetadata] = {}
        self.plugin_hooks: Dict[str, List[Callable]] = {}
    
    def register_plugin(self, plugin_id: str, plugin: Plugin) -> bool:
        """
        Register a plugin instance
        
        Args:
            plugin_id: Unique identifier for the plugin
            plugin: Plugin instance
            
        Returns:
            True if registration successful
        """
        if plugin_id in self.plugins:
            logger.warning("Plugin already registered", plugin_id=plugin_id)
            return False
        
        try:
            metadata = plugin.get_metadata()
            
            if not metadata.enabled:
                logger.info("Plugin is disabled", plugin_id=plugin_id)
                return False
            
            self.plugins[plugin_id] = plugin
            self.metadata[plugin_id] = metadata
            
            logger.info("Plugin registered successfully",
                       plugin_id=plugin_id,
                       plugin_type=metadata.plugin_type.value,
                       version=metadata.version)
            return True
            
        except Exception as e:
            logger.error("Failed to register plugin",
                        plugin_id=plugin_id,
                        error=str(e))
            return False
    
    def unregister_plugin(self, plugin_id: str) -> bool:
        """Unregister a plugin"""
        if plugin_id not in self.plugins:
            return False
        
        plugin = self.plugins[plugin_id]
        
        try:
            # Cleanup plugin
            import asyncio
            asyncio.create_task(plugin.cleanup())
        except Exception as e:
            logger.error("Error during plugin cleanup",
                        plugin_id=plugin_id,
                        error=str(e))
        
        del self.plugins[plugin_id]
        del self.metadata[plugin_id]
        
        logger.info("Plugin unregistered", plugin_id=plugin_id)
        return True
    
    def get_plugin(self, plugin_id: str) -> Optional[Plugin]:
        """Get a registered plugin by ID"""
        return self.plugins.get(plugin_id)
    
    def get_plugins_by_type(self, plugin_type: PluginType) -> List[Plugin]:
        """Get all plugins of a specific type"""
        result = []
        for plugin_id, metadata in self.metadata.items():
            if metadata.plugin_type == plugin_type:
                plugin = self.plugins.get(plugin_id)
                if plugin:
                    result.append(plugin)
        
        # Sort by priority (lower number = higher priority)
        result.sort(key=lambda p: p.get_metadata().priority)
        return result
    
    def list_plugins(self) -> Dict[str, PluginMetadata]:
        """List all registered plugins"""
        return self.metadata.copy()
    
    async def initialize_all(self) -> Dict[str, bool]:
        """Initialize all registered plugins"""
        results = {}
        
        for plugin_id, plugin in self.plugins.items():
            try:
                success = await plugin.initialize()
                results[plugin_id] = success
                
                if success:
                    plugin.initialized = True
                    logger.info("Plugin initialized", plugin_id=plugin_id)
                else:
                    logger.warning("Plugin initialization failed", plugin_id=plugin_id)
                    
            except Exception as e:
                logger.error("Error initializing plugin",
                           plugin_id=plugin_id,
                           error=str(e))
                results[plugin_id] = False
        
        return results
    
    async def cleanup_all(self) -> None:
        """Cleanup all registered plugins"""
        for plugin_id, plugin in self.plugins.items():
            try:
                await plugin.cleanup()
                logger.info("Plugin cleaned up", plugin_id=plugin_id)
            except Exception as e:
                logger.error("Error cleaning up plugin",
                           plugin_id=plugin_id,
                           error=str(e))
    
    def discover_plugins(self, package_name: str) -> int:
        """
        Discover and auto-register plugins from a package
        
        Args:
            package_name: Python package to search for plugins
            
        Returns:
            Number of plugins discovered
        """
        count = 0
        
        try:
            package = importlib.import_module(package_name)
            
            for _, module_name, _ in pkgutil.walk_packages(package.__path__,
                                                          prefix=f"{package_name}."):
                try:
                    module = importlib.import_module(module_name)
                    
                    # Find all Plugin subclasses in the module
                    for name, obj in inspect.getmembers(module):
                        if (inspect.isclass(obj) and 
                            issubclass(obj, Plugin) and 
                            obj is not Plugin):
                            
                            # Auto-instantiate and register
                            plugin_id = f"{package_name}.{name}"
                            plugin_instance = obj()
                            
                            if self.register_plugin(plugin_id, plugin_instance):
                                count += 1
                                
                except Exception as e:
                    logger.debug("Error loading module",
                               module=module_name,
                               error=str(e))
            
            logger.info("Plugin discovery complete",
                       package=package_name,
                       count=count)
            
        except ImportError as e:
            logger.error("Package not found for plugin discovery",
                        package=package_name,
                        error=str(e))
        
        return count
    
    def register_hook(self, hook_name: str, callback: Callable) -> None:
        """
        Register a hook callback
        
        Hooks allow plugins to react to events in the system
        """
        if hook_name not in self.plugin_hooks:
            self.plugin_hooks[hook_name] = []
        
        self.plugin_hooks[hook_name].append(callback)
        logger.debug("Hook registered", hook=hook_name)
    
    async def trigger_hook(self, hook_name: str, *args, **kwargs) -> List[Any]:
        """
        Trigger all callbacks registered for a hook
        
        Returns:
            List of results from all callbacks
        """
        if hook_name not in self.plugin_hooks:
            return []
        
        results = []
        for callback in self.plugin_hooks[hook_name]:
            try:
                if inspect.iscoroutinefunction(callback):
                    result = await callback(*args, **kwargs)
                else:
                    result = callback(*args, **kwargs)
                results.append(result)
            except Exception as e:
                logger.error("Error executing hook callback",
                           hook=hook_name,
                           error=str(e))
        
        return results


class PluginManager:
    """
    High-level plugin management interface
    
    Provides convenience methods for working with the plugin system
    """
    
    def __init__(self):
        self.registry = PluginRegistry()
    
    def load_plugin(self, plugin_class: Type[Plugin], 
                   plugin_id: str,
                   config: Optional[Dict[str, Any]] = None) -> bool:
        """
        Load and register a plugin class
        
        Args:
            plugin_class: Plugin class to instantiate
            plugin_id: Unique identifier for the plugin
            config: Optional configuration dictionary
            
        Returns:
            True if loaded successfully
        """
        try:
            plugin = plugin_class(config=config)
            return self.registry.register_plugin(plugin_id, plugin)
        except Exception as e:
            logger.error("Failed to load plugin",
                        plugin_id=plugin_id,
                        error=str(e))
            return False
    
    def load_plugins_from_config(self, config: Dict[str, Any]) -> int:
        """
        Load plugins from configuration
        
        Expected config format:
        {
            "plugins": {
                "plugin_id": {
                    "class": "module.path.PluginClass",
                    "config": {...}
                }
            }
        }
        
        Returns:
            Number of plugins loaded
        """
        count = 0
        plugins_config = config.get("plugins", {})
        
        for plugin_id, plugin_config in plugins_config.items():
            try:
                class_path = plugin_config.get("class")
                if not class_path:
                    logger.warning("No class specified for plugin", plugin_id=plugin_id)
                    continue
                
                # Import the plugin class
                module_path, class_name = class_path.rsplit(".", 1)
                module = importlib.import_module(module_path)
                plugin_class = getattr(module, class_name)
                
                # Load the plugin
                if self.load_plugin(plugin_class, plugin_id, 
                                   plugin_config.get("config")):
                    count += 1
                    
            except Exception as e:
                logger.error("Failed to load plugin from config",
                           plugin_id=plugin_id,
                           error=str(e))
        
        logger.info("Plugins loaded from config", count=count)
        return count
    
    async def start(self) -> None:
        """Start the plugin manager and initialize all plugins"""
        logger.info("Starting plugin manager")
        await self.registry.initialize_all()
    
    async def stop(self) -> None:
        """Stop the plugin manager and cleanup all plugins"""
        logger.info("Stopping plugin manager")
        await self.registry.cleanup_all()
    
    def get_plugin(self, plugin_id: str) -> Optional[Plugin]:
        """Get a plugin by ID"""
        return self.registry.get_plugin(plugin_id)
    
    def list_plugins(self, plugin_type: Optional[PluginType] = None) -> List[PluginMetadata]:
        """
        List all plugins, optionally filtered by type
        
        Args:
            plugin_type: Optional filter by plugin type
            
        Returns:
            List of plugin metadata
        """
        all_metadata = self.registry.list_plugins()
        
        if plugin_type is None:
            return list(all_metadata.values())
        
        return [m for m in all_metadata.values() if m.plugin_type == plugin_type]


# Global plugin manager instance
_plugin_manager: Optional[PluginManager] = None


def get_plugin_manager() -> PluginManager:
    """Get the global plugin manager instance"""
    global _plugin_manager
    if _plugin_manager is None:
        _plugin_manager = PluginManager()
    return _plugin_manager
