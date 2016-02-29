#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name="CDAT Widgets",
    version="0.1",
    description="Dev Package for CDATGUI widgets",
    author="Bryce Sampson",
    author_email="sampson9@llnl.gov",
    packages=find_packages(exclude="tests"),
)