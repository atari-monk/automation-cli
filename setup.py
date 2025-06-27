from setuptools import setup, find_packages


setup(
    name="automation-cli",
    version="0.1",
    packages=find_packages(),
    install_requires=[],
    entry_points={
        "console_scripts": [
            "automation_cli=automation_cli.main:main",
        ],
    },
    python_requires=">=3.7",
)
