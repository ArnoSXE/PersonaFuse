from setuptools import setup, find_packages

setup(
    name="personafuse",
    version="1.0",
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "personafuse=personafuse.cli:analyze"
        ]
    }
)
