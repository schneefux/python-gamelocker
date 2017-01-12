#!/usr/bin/python

from setuptools import setup

setup(
    name="Gamelocker-API",
    version="0.1",
    description="Gamelocker API Wrapper",
    author="schneefux",
    py_modules=["gamelocker"],
    setup_requires=["pytest-runner"],
    tests_require=["pytest"]
)
