"""
Setup script for HIPAA-Compliant AI Investigation System
"""
from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="hipaa-ai-investigation",
    version="1.0.0",
    author="STATE",
    description="HIPAA-compliant AI Investigation System",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/state/hipaa-ai-investigation",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Government",
        "Topic :: Security",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.9",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "investigation-api=src.api.main:app",
        ],
    },
)

