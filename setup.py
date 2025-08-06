#!/usr/bin/env python3
"""
AI Engineering Toolkit Setup Script
"""

from setuptools import setup, find_packages
import os

# Read README file
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# Read requirements
def read_requirements(filename):
    """Read requirements from file"""
    with open(filename, 'r') as f:
        return [line.strip() for line in f if line.strip() and not line.startswith('#')]

# Read version
def read_version():
    """Read version from __init__.py"""
    version_file = os.path.join("ai_toolkit", "__init__.py")
    if os.path.exists(version_file):
        with open(version_file, 'r') as f:
            for line in f:
                if line.startswith('__version__'):
                    return line.split('=')[1].strip().strip('"').strip("'")
    return "0.1.0"

setup(
    name="ai-engineering-toolkit",
    version=read_version(),
    author="AI Engineering Toolkit Contributors",
    author_email="contributors@ai-toolkit.com",
    description="A comprehensive toolkit for AI engineering professionals and newsletter creators",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/ai-engineering-toolkit",
    project_urls={
        "Bug Tracker": "https://github.com/yourusername/ai-engineering-toolkit/issues",
        "Documentation": "https://github.com/yourusername/ai-engineering-toolkit/wiki",
        "Source Code": "https://github.com/yourusername/ai-engineering-toolkit",
    },
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Communications :: Email",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content :: News/Diary",
    ],
    python_requires=">=3.8",
    install_requires=read_requirements("requirements.txt") if os.path.exists("requirements.txt") else [],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "black>=22.0.0",
            "isort>=5.10.0",
            "flake8>=5.0.0",
            "mypy>=0.991",
            "pre-commit>=2.20.0",
        ],
        "jupyter": [
            "jupyter>=1.0.0",
            "notebook>=6.4.0",
            "ipywidgets>=8.0.0",
            "matplotlib>=3.5.0",
            "seaborn>=0.11.0",
        ],
        "docs": [
            "sphinx>=5.0.0",
            "sphinx-rtd-theme>=1.0.0",
            "myst-parser>=0.18.0",
        ],
        "all": [
            # Include all optional dependencies
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0", 
            "black>=22.0.0",
            "isort>=5.10.0",
            "flake8>=5.0.0",
            "mypy>=0.991",
            "pre-commit>=2.20.0",
            "jupyter>=1.0.0",
            "notebook>=6.4.0",
            "ipywidgets>=8.0.0",
            "matplotlib>=3.5.0",
            "seaborn>=0.11.0",
            "sphinx>=5.0.0",
            "sphinx-rtd-theme>=1.0.0",
            "myst-parser>=0.18.0",
        ]
    },
    entry_points={
        "console_scripts": [
            "ai-toolkit-content=scripts.newsletter_automation.content_generator:main",
            "ai-toolkit-rag=examples.rag_systems.ai_toolkit_rag:main",
        ],
    },
    include_package_data=True,
    package_data={
        "": ["*.md", "*.txt", "*.yaml", "*.yml", "*.json", "*.toml"],
        "templates": ["newsletter/*", "social-media/*"],
        "scripts": ["*/*.py"],
        "examples": ["*/*.py"],
    },
    zip_safe=False,
    keywords=[
        "ai",
        "artificial-intelligence", 
        "machine-learning",
        "deep-learning",
        "newsletter",
        "automation",
        "llm",
        "rag",
        "mlops",
        "ai-engineering",
        "content-generation",
        "social-media",
        "analytics",
    ],
)