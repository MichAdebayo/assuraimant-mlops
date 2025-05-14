from setuptools import setup, find_packages

setup(
    name="assuraimant_ci_cd",
    version="0.1",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
)
