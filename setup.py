#!/usr/bin/env python3.11

from os.path import abspath, dirname, join
from setuptools import setup, find_packages

with open("requirements.txt") as f:
    requirements = f.read().strip().splitlines()


source_directory = dirname(abspath(__file__))


setup(
    name="pyutils",
    version="0.0.1",
    python_requires=">=3.8",
    description="Python utilities",
    author="Mayank Mahajan",
    author_email="mayankm2089@gmail.com",
    url="https://github.com/mayank-m2/pyutils",
    packages=find_packages(),
    install_requires=requirements,
    include_package_data=True,
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
)
