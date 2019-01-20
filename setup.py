"""A setuptools based setup module."""
from setuptools import setup, find_packages
from os import path

from io import open

here = path.abspath(path.dirname(__file__))

with open(path.join(here, "README.md"), encoding="utf-8") as f:
    long_description = f.read()


setup(
    name="toastr",
    version="0.0.0",
    description="An Optical Character recognition based code execution tool.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/markygriff/toastr",
    author="Mark, Enzo, Jordan, and Brad",
    packages=find_packages(exclude=["contrib", "docs", "tests"]),
    install_requires=[
        "numpy",
        "opencv-python",
        "google-cloud-pubsub",
        "google-cloud-storage",
        "google-cloud-translate",
        "google-cloud-vision",
    ],
    # entry_points={"console_scripts": ["sample=sample:main"]},  # Optional
)
