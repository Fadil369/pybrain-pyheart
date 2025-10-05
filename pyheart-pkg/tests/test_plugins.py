"""
Tests for the plugin system
"""

import pytest
from pyheart.core.plugins import (
    Plugin, PluginManager, PluginRegistry, PluginType, PluginMetadata
)
from pyheart.plugins.insurance import InsuranceAdapter, ClaimsAutomationPlugin
from pyheart.plugins.government import GovernmentAdapter, PublicHealthReportingPlugin
from pyheart.plugins.provider import ProviderAdapter, CareCoordinationPlugin


class TestPluginRegistry:
    """Test plugin registry functionality"""
    
    def test_register_plugin(self):
        """Test plugin registration"""
        registry = PluginRegistry()
        
        # Create a test plugin
        plugin = InsuranceAdapter(config={
            "system_id": "test",
            "base_url": "https://test.com",
            "api_key": "test-key",
            "payer_id": "TEST-001"
        })
        
        # Register plugin
        success = registry.register_plugin("test_insurance", plugin)
        assert success
        
        # Verify plugin is registered
        assert "test_insurance" in registry.plugins
        assert "test_insurance" in registry.metadata
    
    def test_get_plugin(self):
        """Test retrieving a plugin"""
        registry = PluginRegistry()
        
        plugin = InsuranceAdapter(config={
            "system_id": "test",
            "base_url": "https://test.com",
            "api_key": "test-key",
            "payer_id": "TEST-001"
        })
        
        registry.register_plugin("test_insurance", plugin)
        
        # Get plugin
        retrieved = registry.get_plugin("test_insurance")
        assert retrieved is not None
        assert retrieved == plugin
    
    def test_get_plugins_by_type(self):
        """Test filtering plugins by type"""
        registry = PluginRegistry()
        
        # Register adapter plugin
        adapter = InsuranceAdapter(config={
            "system_id": "test",
            "base_url": "https://test.com",
            "api_key": "test-key",
            "payer_id": "TEST-001"
        })
        registry.register_plugin("adapter", adapter)
        
        # Register workflow plugin
        workflow = ClaimsAutomationPlugin()
        registry.register_plugin("workflow", workflow)
        
        # Get adapters
        adapters = registry.get_plugins_by_type(PluginType.ADAPTER)
        assert len(adapters) == 1
        assert adapters[0] == adapter
        
        # Get workflows
        workflows = registry.get_plugins_by_type(PluginType.WORKFLOW)
        assert len(workflows) == 1
        assert workflows[0] == workflow
    
    def test_list_plugins(self):
        """Test listing all plugins"""
        registry = PluginRegistry()
        
        plugin1 = InsuranceAdapter(config={
            "system_id": "test1",
            "base_url": "https://test.com",
            "api_key": "test-key",
            "payer_id": "TEST-001"
        })
        plugin2 = GovernmentAdapter(config={
            "system_id": "test2",
            "agency_type": "public_health",
            "base_url": "https://test.com",
            "jurisdiction": "CA"
        })
        
        registry.register_plugin("plugin1", plugin1)
        registry.register_plugin("plugin2", plugin2)
        
        plugins = registry.list_plugins()
        assert len(plugins) == 2
        assert "plugin1" in plugins
        assert "plugin2" in plugins
    
    def test_unregister_plugin(self):
        """Test unregistering a plugin"""
        registry = PluginRegistry()
        
        plugin = InsuranceAdapter(config={
            "system_id": "test",
            "base_url": "https://test.com",
            "api_key": "test-key",
            "payer_id": "TEST-001"
        })
        
        registry.register_plugin("test", plugin)
        assert "test" in registry.plugins
        
        # Unregister
        success = registry.unregister_plugin("test")
        assert success
        assert "test" not in registry.plugins
        assert "test" not in registry.metadata


class TestPluginManager:
    """Test plugin manager functionality"""
    
    def test_load_plugin(self):
        """Test loading a plugin through manager"""
        manager = PluginManager()
        
        config = {
            "system_id": "test",
            "base_url": "https://test.com",
            "api_key": "test-key",
            "payer_id": "TEST-001"
        }
        
        success = manager.load_plugin(InsuranceAdapter, "test_insurance", config)
        assert success
        
        # Verify plugin is loaded
        plugin = manager.get_plugin("test_insurance")
        assert plugin is not None
    
    def test_list_plugins(self):
        """Test listing plugins through manager"""
        manager = PluginManager()
        
        manager.load_plugin(InsuranceAdapter, "insurance", {
            "system_id": "test",
            "base_url": "https://test.com",
            "api_key": "key",
            "payer_id": "TEST"
        })
        
        plugins = manager.list_plugins()
        assert len(plugins) == 1
    
    def test_list_plugins_by_type(self):
        """Test filtering plugins by type through manager"""
        manager = PluginManager()
        
        # Load adapter
        manager.load_plugin(InsuranceAdapter, "adapter", {
            "system_id": "test",
            "base_url": "https://test.com",
            "api_key": "key",
            "payer_id": "TEST"
        })
        
        # Load workflow
        manager.load_plugin(ClaimsAutomationPlugin, "workflow", {})
        
        # Filter by type
        adapters = manager.list_plugins(plugin_type=PluginType.ADAPTER)
        assert len(adapters) == 1
        
        workflows = manager.list_plugins(plugin_type=PluginType.WORKFLOW)
        assert len(workflows) == 1


class TestInsurancePlugin:
    """Test insurance adapter plugin"""
    
    def test_metadata(self):
        """Test insurance plugin metadata"""
        plugin = InsuranceAdapter(config={
            "system_id": "test",
            "base_url": "https://test.com",
            "api_key": "key",
            "payer_id": "TEST"
        })
        
        metadata = plugin.get_metadata()
        assert metadata.name == "Insurance Adapter"
        assert metadata.plugin_type == PluginType.ADAPTER
        assert metadata.version == "1.0.0"
    
    @pytest.mark.asyncio
    async def test_initialize(self):
        """Test insurance plugin initialization"""
        plugin = InsuranceAdapter(config={
            "system_id": "test",
            "base_url": "https://test.com",
            "api_key": "key",
            "payer_id": "TEST"
        })
        
        success = await plugin.initialize()
        assert success
    
    @pytest.mark.asyncio
    async def test_fetch_claims(self):
        """Test fetching claims"""
        plugin = InsuranceAdapter(config={
            "system_id": "test",
            "base_url": "https://test.com",
            "api_key": "key",
            "payer_id": "TEST"
        })
        
        await plugin.initialize()
        
        claims = await plugin.fetch_data("Claim", {"claim_id": "CLM-001"})
        assert len(claims) > 0
        assert claims[0]["resourceType"] == "Claim"


class TestGovernmentPlugin:
    """Test government adapter plugin"""
    
    def test_metadata(self):
        """Test government plugin metadata"""
        plugin = GovernmentAdapter(config={
            "system_id": "test",
            "agency_type": "public_health",
            "base_url": "https://test.com",
            "jurisdiction": "CA"
        })
        
        metadata = plugin.get_metadata()
        assert metadata.name == "Government Adapter"
        assert metadata.plugin_type == PluginType.ADAPTER
    
    @pytest.mark.asyncio
    async def test_initialize(self):
        """Test government plugin initialization"""
        plugin = GovernmentAdapter(config={
            "system_id": "test",
            "agency_type": "public_health",
            "base_url": "https://test.com",
            "jurisdiction": "CA"
        })
        
        success = await plugin.initialize()
        assert success


class TestProviderPlugin:
    """Test provider adapter plugin"""
    
    def test_metadata(self):
        """Test provider plugin metadata"""
        plugin = ProviderAdapter(config={
            "system_id": "test",
            "ehr_type": "epic",
            "base_url": "https://test.com",
            "client_id": "client",
            "client_secret": "secret"
        })
        
        metadata = plugin.get_metadata()
        assert metadata.name == "Provider Adapter"
        assert metadata.plugin_type == PluginType.ADAPTER
    
    @pytest.mark.asyncio
    async def test_initialize(self):
        """Test provider plugin initialization"""
        plugin = ProviderAdapter(config={
            "system_id": "test",
            "ehr_type": "epic",
            "base_url": "https://test.com",
            "client_id": "client",
            "client_secret": "secret"
        })
        
        success = await plugin.initialize()
        assert success
    
    @pytest.mark.asyncio
    async def test_fetch_patients(self):
        """Test fetching patients"""
        plugin = ProviderAdapter(config={
            "system_id": "test",
            "ehr_type": "epic",
            "base_url": "https://test.com",
            "client_id": "client",
            "client_secret": "secret"
        })
        
        await plugin.initialize()
        
        patients = await plugin.fetch_data("Patient", {"patient_id": "12345"})
        assert len(patients) > 0
        assert patients[0]["resourceType"] == "Patient"


class TestWorkflowPlugins:
    """Test workflow plugins"""
    
    @pytest.mark.asyncio
    async def test_claims_automation(self):
        """Test claims automation plugin"""
        plugin = ClaimsAutomationPlugin()
        
        await plugin.initialize()
        
        claim_data = {
            "patient": "Patient/123",
            "provider": "Org/456",
            "diagnosis": [{"code": "E11.9"}],
            "serviceDate": "2024-01-15"
        }
        
        result = await plugin.process_claim(claim_data)
        assert result["valid"] is True
        assert len(result["errors"]) == 0
    
    @pytest.mark.asyncio
    async def test_public_health_reporting(self):
        """Test public health reporting plugin"""
        plugin = PublicHealthReportingPlugin(config={"jurisdiction": "CA"})
        
        await plugin.initialize()
        
        # Test reportable condition detection
        assert plugin.is_reportable("COVID-19") is True
        assert plugin.is_reportable("Common Cold") is False
        
        # Test report generation
        patient_data = {"id": "Patient/123", "provider": "Dr. Smith"}
        condition_data = {"code": "COVID-19", "onsetDateTime": "2024-01-10"}
        
        report = await plugin.generate_report(patient_data, condition_data)
        assert report["condition"] == "COVID-19"
        assert report["jurisdiction"] == "CA"
    
    @pytest.mark.asyncio
    async def test_care_coordination(self):
        """Test care coordination plugin"""
        plugin = CareCoordinationPlugin()
        
        await plugin.initialize()
        
        patient_data = {"id": "Patient/123", "name": "John Doe"}
        referral = await plugin.create_referral(
            patient_data,
            "Cardiology",
            "Abnormal ECG"
        )
        
        assert referral["resourceType"] == "ServiceRequest"
        assert referral["specialty"] == "Cardiology"
