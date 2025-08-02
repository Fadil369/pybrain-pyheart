# Version Strategy & Release Best Practices

## 📋 Semantic Versioning

This project follows [Semantic Versioning (SemVer)](https://semver.org/) with the format `MAJOR.MINOR.PATCH`:

### Version Format: `X.Y.Z`

- **MAJOR (X)**: Breaking changes that require user code modifications
- **MINOR (Y)**: New features that are backward-compatible
- **PATCH (Z)**: Bug fixes and backward-compatible improvements

### Examples:
- `0.1.0` → `0.1.1`: Bug fix (patch)
- `0.1.1` → `0.2.0`: New features (minor) 
- `0.2.0` → `1.0.0`: Breaking changes (major)

## 🔄 Release Process

### 1. Pre-Release Checklist
- [ ] All tests passing
- [ ] Documentation updated
- [ ] CHANGELOG.md updated
- [ ] Version numbers updated in all files
- [ ] Security scan completed
- [ ] Performance benchmarks run

### 2. Version Update Locations
Update version in these files:
```bash
# PyBrain
pybrain-pkg/pyproject.toml      # version = "X.Y.Z"
pybrain-pkg/src/pybrain/__init__.py  # __version__ = "X.Y.Z"

# PyHeart  
pyheart-pkg/pyproject.toml      # version = "X.Y.Z"
pyheart-pkg/src/pyheart/__init__.py  # __version__ = "X.Y.Z"
```

### 3. Release Steps

#### Step 1: Prepare Release
```bash
# 1. Create release branch
git checkout -b release/v0.2.0

# 2. Update versions (use helper script)
python scripts/update_version.py 0.2.0

# 3. Update CHANGELOG.md
# Add new section for version 0.2.0

# 4. Commit changes
git add .
git commit -m "chore: bump version to 0.2.0"
```

#### Step 2: Test Release
```bash
# 1. Build packages
python build_and_publish.py

# 2. Test locally
pip install -e ./pybrain-pkg[dev]
pip install -e ./pyheart-pkg[dev]

# 3. Run full test suite
pytest pybrain-pkg/tests/ -v
pytest pyheart-pkg/tests/ -v

# 4. Test CLI commands
pybrain --version
pyheart --version
```

#### Step 3: Create Release
```bash
# 1. Merge to main
git checkout main
git merge release/v0.2.0

# 2. Create and push tag
git tag -a v0.2.0 -m "Release version 0.2.0"
git push origin main --tags

# 3. Create GitHub release (automated or manual)
gh release create v0.2.0 --generate-notes --title "v0.2.0"
```

#### Step 4: Publish Packages
```bash
# 1. Build final packages
cd pybrain-pkg && python -m build
cd ../pyheart-pkg && python -m build

# 2. Publish to PyPI
cd pybrain-pkg && python -m twine upload dist/*
cd ../pyheart-pkg && python -m twine upload dist/*
```

## 🏷️ Release Types

### Stable Releases (1.0.0+)
- Full production ready
- Comprehensive testing
- Performance optimized
- Complete documentation

### Beta Releases (0.X.0)
- Feature complete
- Public testing
- API stabilization
- Documentation review

### Alpha Releases (0.0.X)
- Early development
- Core features working
- Breaking changes expected
- Limited testing

## 📊 Release Categories

### Major Releases (X.0.0)
**Examples of breaking changes:**
- API redesign or removal
- Database schema changes
- Configuration format changes
- Minimum version requirement updates

### Minor Releases (X.Y.0)
**Examples of new features:**
- New AI models or algorithms
- Additional FHIR resources support
- New integration adapters
- Enhanced CLI commands

### Patch Releases (X.Y.Z)
**Examples of fixes:**
- Bug fixes
- Security patches
- Performance improvements
- Documentation updates

## 🔒 Security Releases

For security issues:
1. **Immediate patch** for critical vulnerabilities
2. **Security advisory** published on GitHub
3. **Coordinated disclosure** with affected parties
4. **Fast-track release** process

## 📅 Release Schedule

### Regular Schedule
- **Major releases**: Every 6-12 months
- **Minor releases**: Every 1-2 months
- **Patch releases**: As needed (weekly if required)

### Emergency Schedule
- **Security patches**: Within 24-48 hours
- **Critical bugs**: Within 1 week
- **High-priority features**: Within 1 month

## 🛠️ Automation Tools

### GitHub Actions Workflows
```yaml
# .github/workflows/release.yml
name: Release
on:
  push:
    tags: ['v*']
jobs:
  release:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Build and publish
        run: |
          python -m build
          python -m twine upload dist/*
```

### Version Update Script
```python
# scripts/update_version.py
import sys
import re

def update_version(new_version):
    files = [
        "pybrain-pkg/pyproject.toml",
        "pybrain-pkg/src/pybrain/__init__.py",
        "pyheart-pkg/pyproject.toml", 
        "pyheart-pkg/src/pyheart/__init__.py"
    ]
    
    for file_path in files:
        # Update version in each file
        pass
```

## 📈 Metrics & Monitoring

### Release Metrics
- Download statistics from PyPI
- GitHub release analytics
- Issue/bug reports post-release
- Performance benchmarks

### Quality Gates
- ✅ 90%+ test coverage
- ✅ All CI/CD checks pass
- ✅ Security scan clean
- ✅ Documentation complete
- ✅ Performance within SLA

## 🎯 Best Practices Summary

1. **Always update CHANGELOG.md** with user-facing changes
2. **Test thoroughly** before releasing
3. **Use semantic versioning** consistently
4. **Tag releases** with descriptive messages
5. **Automate where possible** to reduce errors
6. **Communicate changes** clearly to users
7. **Monitor post-release** for issues
8. **Rollback plan** ready for critical issues

## 🚀 Quick Release Commands

### For Patch Release (0.1.0 → 0.1.1)
```bash
python scripts/update_version.py 0.1.1
git add . && git commit -m "chore: bump version to 0.1.1"
git tag v0.1.1 && git push origin main --tags
python build_and_publish.py
```

### For Minor Release (0.1.1 → 0.2.0)
```bash
python scripts/update_version.py 0.2.0
# Update CHANGELOG.md with new features
git add . && git commit -m "feat: release version 0.2.0"
git tag v0.2.0 && git push origin main --tags
gh release create v0.2.0 --generate-notes
python build_and_publish.py
```