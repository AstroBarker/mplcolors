#!/usr/bin/env python3
from setuptools import setup, find_packages

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name="mplcolors",
    description="CLI and package to manipulate and display matplotlib colors",
    long_description=long_description,
    url="https://github.com/AstroBarker/mplcolors",
    author="Brandon L. Barker",
    author_email="bbarker.py@proton.me",
    license="GPL-3.0",
    classifiers=[
        "Development Status :: 6 - Mature",
        "Intended Audience :: Science/Research/DevOps",
        "Environment :: Console",
        "Natural Language :: English",
        "Operating System :: Unix",
        "Programming Language :: Python :: 3.10"
    ],
    keywords="simulations science computing githubapp visualization cli",
    packages=find_packages(),
    install_requires=["matplotlib", "argparse"],
)
