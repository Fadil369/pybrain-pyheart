# 🚀 PyBrain & PyHeart Deployment Guide

This guide walks you through building, testing, and publishing the PyBrain and PyHeart packages to PyPI.

## 📋 Prerequisites

1. **Python 3.8+** installed
2. **pip** updated to latest version
3. **PyPI account** (for publishing)
4. **TestPyPI account** (for testing)

## 🛠️ Setup

### 1. Install Build Tools

```bash
pip install --upgrade pip build twine
```

### 2. Set up PyPI Credentials

Create `~/.pypirc` file:

```ini
[distutils]
index-servers =
    pypi
    testpypi

[pypi]
username = __token__
password = pypi-your-api-token-here

[testpypi]
repository = https://test.pypi.org/legacy/
username = __token__
password = pypi-your-testpypi-api-token-here
```

## 🔨 Building Packages

### Automated Build (Recommended)

Run the automated build script:

```bash
python build_and_publish.py
```

This script will:
- Clean previous builds
- Build both packages
- Run tests
- Check package integrity
- Install packages locally for testing

### Manual Build

#### Build PyBrain

```bash
cd pybrain-pkg
python -m build
python -m twine check dist/*
```

#### Build PyHeart

```bash
cd pyheart-pkg
python -m build
python -m twine check dist/*
```

## 🧪 Testing

### Run Package Tests

```bash
# Test PyBrain
cd pybrain-pkg
python -m pytest tests/ -v

# Test PyHeart
cd pyheart-pkg
python -m pytest tests/ -v
```

### Test Local Installation

```bash
# Install PyBrain locally
cd pybrain-pkg
pip install -e .

# Install PyHeart locally
cd pyheart-pkg
pip install -e .

# Test imports
python -c "from pybrain import AIEngine; print('PyBrain imported successfully')"
python -c "from pyheart import FHIRClient; print('PyHeart imported successfully')"
```

## 📦 Publishing

### 1. Publish to Test PyPI (Recommended First)

```bash
# Publish PyBrain to TestPyPI
cd pybrain-pkg
python -m twine upload --repository testpypi dist/*

# Publish PyHeart to TestPyPI
cd pyheart-pkg
python -m twine upload --repository testpypi dist/*
```

### 2. Test Installation from TestPyPI

```bash
# Test install PyBrain from TestPyPI
pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ pybrain

# Test install PyHeart from TestPyPI
pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ pyheart
```

### 3. Publish to Production PyPI

Once testing is successful:

```bash
# Publish PyBrain to PyPI
cd pybrain-pkg
python -m twine upload dist/*

# Publish PyHeart to PyPI
cd pyheart-pkg
python -m twine upload dist/*
```

## 🔍 Verification

### Verify Publication

```bash
# Check PyBrain on PyPI
pip search pybrain
pip show pybrain

# Check PyHeart on PyPI
pip search pyheart
pip show pyheart
```

### Test Installation from PyPI

```bash
# Create fresh virtual environment
python -m venv test_env
source test_env/bin/activate  # On Windows: test_env\Scripts\activate

# Install from PyPI
pip install pybrain pyheart

# Test functionality
python -c "
from pybrain import AIEngine, DataHarmonizer
from pyheart import FHIRClient, WorkflowEngine

# Test PyBrain
ai = AIEngine()
entities = ai.extract_clinical_entities('Patient has diabetes')
print('PyBrain entities:', entities)

# Test PyHeart
client = FHIRClient('https://example.com')
print('PyHeart client created successfully')
"
```

## 📊 Package Information

### PyBrain Package
- **Name**: `pybrain`
- **Description**: Unified Healthcare Intelligence Platform
- **Key Features**: AI-powered data harmonization, clinical NLP, decision support
- **Dependencies**: PyTorch, Transformers, FHIR Resources, Pandas, NumPy

### PyHeart Package
- **Name**: `pyheart`
- **Description**: Healthcare Interoperability & Workflow Engine
- **Key Features**: Universal API gateway, workflow orchestration, security & compliance
- **Dependencies**: FastAPI, HTTPX, Pydantic, SQLAlchemy, Redis

## 🚨 Troubleshooting

### Common Issues

1. **Build fails with missing dependencies**
   ```bash
   pip install --upgrade setuptools wheel build
   ```

2. **Tests fail due to missing modules**
   ```bash
   pip install -e .[dev]
   ```

3. **Upload fails with authentication error**
   - Check your `~/.pypirc` file
   - Verify API tokens are correct
   - Use `--verbose` flag for detailed error info

4. **Package already exists error**
   - Increment version number in `pyproject.toml`
   - Use semantic versioning (e.g., 0.1.1, 0.2.0)

### Version Management

Update versions in both packages before publishing:

```bash
# In pybrain-pkg/pyproject.toml
version = "0.1.1"

# In pyheart-pkg/pyproject.toml
version = "0.1.1"

# Also update __init__.py files
__version__ = "0.1.1"
```

## 📈 Post-Publication

### Monitor Downloads

- Check PyPI statistics: https://pypistats.org/packages/pybrain
- Monitor GitHub issues and feedback
- Update documentation based on user feedback

### Maintenance

1. **Regular updates** for security and bug fixes
2. **Documentation updates** as features evolve
3. **Community engagement** through GitHub issues
4. **Dependency updates** to latest stable versions

## 🌟 Success Checklist

- [ ] Both packages build without errors
- [ ] All tests pass
- [ ] Packages install locally
- [ ] Published to TestPyPI successfully
- [ ] Tested installation from TestPyPI
- [ ] Published to production PyPI
- [ ] Verified public availability
- [ ] Documentation updated
- [ ] GitHub releases created

## 🤝 Contributing

For ongoing development:

1. Fork the repository
2. Create feature branches
3. Write tests for new features
4. Update documentation
5. Submit pull requests
6. Follow semantic versioning for releases

---

**🎉 Congratulations! Your PyBrain and PyHeart packages are now available on PyPI!**