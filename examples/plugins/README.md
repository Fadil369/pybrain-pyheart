# PyHeart Plugin Examples

This directory contains comprehensive examples demonstrating how to use PyHeart's plugin system for different healthcare stakeholders.

## 🎯 Overview

PyHeart's plugin architecture enables healthcare organizations to easily integrate and automate their systems with minimal code. The plugin system supports:

- **Plug-and-Play Integration**: Load adapters dynamically without code changes
- **Automated Workflows**: Pre-built automation for common healthcare processes
- **Configuration-Driven**: Manage plugins through YAML configuration files
- **Extensible**: Create custom plugins for specialized needs

## 📚 Examples

### 1. Insurance Company Integration (`insurance_example.py`)

Demonstrates how insurance companies can:
- Submit and track claims automatically
- Check patient eligibility and benefits
- Request prior authorizations
- Process Explanation of Benefits (EOB)

**Key Features:**
- Claims validation and submission
- Automated eligibility verification
- Prior authorization workflow
- Integration with IntegrationHub

**Run the example:**
```bash
python examples/plugins/insurance_example.py
```

### 2. Government Office Integration (`government_example.py`)

Shows how government healthcare offices can:
- Submit public health case reports
- Manage immunization registries
- Report quality measures to CMS
- Handle Medicare/Medicaid claims

**Key Features:**
- Reportable condition detection
- Automated public health reporting
- Immunization forecasting
- Quality measure submission

**Run the example:**
```bash
python examples/plugins/government_example.py
```

### 3. Healthcare Provider Integration (`provider_example.py`)

Illustrates how healthcare providers can:
- Connect to EHR systems (Epic, Cerner, etc.)
- Access patient records and clinical data
- Create referrals and coordinate care
- Automate patient engagement

**Key Features:**
- EHR data access (patients, conditions, medications)
- Care coordination workflows
- Patient appointment reminders
- Medication adherence tracking
- Lab order submission

**Run the example:**
```bash
python examples/plugins/provider_example.py
```

## ⚙️ Configuration

### Using YAML Configuration

Instead of programmatic configuration, you can load plugins from a YAML file:

```python
import asyncio
import yaml
from pyheart import PluginManager

async def main():
    # Load configuration
    with open('plugin_config.yaml', 'r') as f:
        config = yaml.safe_load(f)
    
    # Initialize plugin manager
    plugin_manager = PluginManager()
    
    # Load plugins from config
    plugin_manager.load_plugins_from_config(config)
    
    # Start plugins
    await plugin_manager.start()
    
    # Use plugins...
    
    # Cleanup
    await plugin_manager.stop()

if __name__ == "__main__":
    asyncio.run(main())
```

See `plugin_config.yaml` for a complete configuration example.

### Environment Variables

Sensitive configuration values should use environment variables:

```bash
export INSURANCE_API_KEY="your-api-key"
export EPIC_CLIENT_ID="your-client-id"
export EPIC_CLIENT_SECRET="your-client-secret"
```

## 🔌 Creating Custom Plugins

You can create custom plugins for specialized needs:

```python
from pyheart.core.plugins import Plugin, PluginMetadata, PluginType

class MyCustomAdapter(Plugin):
    """Custom healthcare system adapter"""
    
    def get_metadata(self) -> PluginMetadata:
        return PluginMetadata(
            name="My Custom Adapter",
            version="1.0.0",
            plugin_type=PluginType.ADAPTER,
            description="Custom integration adapter",
            author="Your Organization"
        )
    
    async def initialize(self) -> bool:
        """Initialize your plugin"""
        # Setup code here
        return True
    
    async def cleanup(self) -> bool:
        """Cleanup resources"""
        # Cleanup code here
        return True
    
    # Add your custom methods...
```

## 🚀 Quick Start

### 1. Install PyHeart

```bash
pip install pyheart
```

### 2. Run an Example

```bash
cd examples/plugins
python insurance_example.py
```

### 3. Customize for Your Needs

1. Copy one of the example files
2. Update the configuration with your system details
3. Add your API keys and credentials
4. Run your customized integration

## 📖 Plugin Types

PyHeart supports several plugin types:

1. **ADAPTER**: System integration adapters
   - Insurance systems
   - Government agencies
   - EHR systems
   - Legacy systems

2. **WORKFLOW**: Automated workflow plugins
   - Claims processing
   - Public health reporting
   - Care coordination
   - Patient engagement

3. **TRANSFORMER**: Data transformation plugins
   - Format conversion
   - Data mapping
   - Validation

4. **VALIDATOR**: Data validation plugins
   - Schema validation
   - Business rule validation
   - Compliance checks

5. **AUTHENTICATOR**: Authentication plugins
   - OAuth2 providers
   - SMART on FHIR
   - Custom auth methods

6. **NOTIFIER**: Notification plugins
   - Email notifications
   - SMS alerts
   - Push notifications

## 🏥 Use Cases by Organization Type

### For Insurance Companies
- **Automated Claims Processing**: Validate and submit claims automatically
- **Eligibility Verification**: Real-time benefit checks
- **Prior Authorization**: Streamlined authorization workflows
- **Provider Network Management**: Maintain provider directories

### For Government Offices
- **Public Health Surveillance**: Automated reportable condition detection
- **Registry Management**: Immunization and disease registries
- **Quality Reporting**: CMS quality measures and Meaningful Use
- **Program Administration**: Medicare/Medicaid claim processing

### For Healthcare Providers
- **EHR Integration**: Connect to any EHR system seamlessly
- **Care Coordination**: Referral management and care team collaboration
- **Patient Engagement**: Automated reminders and follow-ups
- **Clinical Decision Support**: AI-powered recommendations

## 🔒 Security Best Practices

1. **Store Credentials Securely**: Use environment variables or secure vaults
2. **Enable Plugin Authentication**: Require authentication for plugin operations
3. **Validate Plugin Sources**: Only load plugins from trusted sources
4. **Monitor Plugin Activity**: Log and audit all plugin operations
5. **Use Sandbox Mode**: Test new plugins in isolation first

## 📞 Support

For questions or issues:
- GitHub Issues: https://github.com/Fadil369/pybrain-pyheart/issues
- Documentation: https://pyheart.readthedocs.io
- Email: healthcare@brainsait.com

## 📄 License

Apache License 2.0 - See LICENSE file for details
