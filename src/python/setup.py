#!/usr/bin/env python3
"""
Setup script for brw-scan-print Python package
"""

from setuptools import setup, find_packages

setup(
    name="brw-scan-print",
    version="0.1.0",
    description="Brother MFC-L2750DW Scanner & Printer Python Module",
    author="Brother MFC-L2750DW Project",
    author_email="dev@example.com",
    url="https://github.com/example/brw-scan-print",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    python_requires=">=3.8",
    install_requires=[
        "pygobject",
        "pycairo",
        "Pillow",
    ],
    extras_require={
        "cups": ["pycups"],
        "sane": ["python-sane"],
        "test": ["pytest", "pytest-cov"],
    },
    entry_points={
        "console_scripts": [
            "brw-scan-print=brw_app.main:main",
            "brw-print=brw_app.cli:print_command",
            "brw-scan=brw_app.cli:scan_command",
        ],
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
)
