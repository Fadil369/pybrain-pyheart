#!/usr/bin/env python3
"""
Version update script for PyBrain & PyHeart packages
"""

import sys
import re
import os
from pathlib import Path


def update_version_in_file(file_path: str, new_version: str, pattern: str, replacement: str):
    """Update version in a specific file"""
    try:
        with open(file_path, 'r') as f:
            content = f.read()
        
        new_content = re.sub(pattern, replacement.format(version=new_version), content)
        
        with open(file_path, 'w') as f:
            f.write(new_content)
        
        print(f"✅ Updated {file_path}")
        return True
    except Exception as e:
        print(f"❌ Failed to update {file_path}: {e}")
        return False


def validate_version(version: str) -> bool:
    """Validate semantic version format"""
    pattern = r'^\d+\.\d+\.\d+(-[a-zA-Z0-9]+(\.[a-zA-Z0-9]+)*)?$'
    return bool(re.match(pattern, version))


def update_all_versions(new_version: str):
    """Update version in all relevant files"""
    if not validate_version(new_version):
        print(f"❌ Invalid version format: {new_version}")
        print("Version should follow semantic versioning: X.Y.Z or X.Y.Z-alpha.1")
        return False
    
    print(f"🔄 Updating version to {new_version}")
    
    # Files to update
    files_to_update = [
        {
            'path': 'pybrain-pkg/pyproject.toml',
            'pattern': r'version = "[^"]*"',
            'replacement': 'version = "{version}"'
        },
        {
            'path': 'pybrain-pkg/src/pybrain/__init__.py',
            'pattern': r'__version__ = "[^"]*"',
            'replacement': '__version__ = "{version}"'
        },
        {
            'path': 'pyheart-pkg/pyproject.toml',
            'pattern': r'version = "[^"]*"',
            'replacement': 'version = "{version}"'
        },
        {
            'path': 'pyheart-pkg/src/pyheart/__init__.py',
            'pattern': r'__version__ = "[^"]*"',
            'replacement': '__version__ = "{version}"'
        }
    ]
    
    success_count = 0
    for file_info in files_to_update:
        if update_version_in_file(
            file_info['path'],
            new_version,
            file_info['pattern'],
            file_info['replacement']
        ):
            success_count += 1
    
    print(f"\n📊 Updated {success_count}/{len(files_to_update)} files")
    
    if success_count == len(files_to_update):
        print(f"🎉 All files updated successfully to version {new_version}")
        print("\n📋 Next steps:")
        print("1. Review changes: git diff")
        print("2. Update CHANGELOG.md")
        print("3. Commit: git add . && git commit -m 'chore: bump version to {}'".format(new_version))
        print("4. Tag: git tag v{} && git push origin main --tags".format(new_version))
        print("5. Build: python build_and_publish.py")
        return True
    else:
        print("❌ Some files failed to update")
        return False


def main():
    """Main function"""
    if len(sys.argv) != 2:
        print("Usage: python update_version.py <new_version>")
        print("Example: python update_version.py 0.1.1")
        sys.exit(1)
    
    new_version = sys.argv[1]
    
    # Change to repository root
    script_dir = Path(__file__).parent
    repo_root = script_dir.parent
    os.chdir(repo_root)
    
    success = update_all_versions(new_version)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()