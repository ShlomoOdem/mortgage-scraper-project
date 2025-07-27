"""
Setup script for Investment Module
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="investment-module",
    version="1.0.0",
    author="Investment Module Team",
    author_email="team@investmentmodule.com",
    description="A comprehensive investment calculation module with tax and inflation considerations",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/investment-module",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Financial and Insurance Industry",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Office/Business :: Financial :: Investment",
        "Topic :: Scientific/Engineering :: Mathematics",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=6.0.0",
            "pytest-cov>=2.10.0",
            "black>=21.0.0",
            "flake8>=3.8.0",
        ],
        "viz": [
            "matplotlib>=3.5.0",
            "seaborn>=0.11.0",
            "plotly>=5.0.0",
        ],
    },
    keywords="investment, finance, calculation, tax, inflation, portfolio",
    project_urls={
        "Bug Reports": "https://github.com/yourusername/investment-module/issues",
        "Source": "https://github.com/yourusername/investment-module",
        "Documentation": "https://investment-module.readthedocs.io/",
    },
) 