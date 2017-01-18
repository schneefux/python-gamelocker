#!/usr/bin/python

from setuptools import setup

setup(
    name="python-gamelocker",
    version="0.1.1",
    description="Python Gamelocker API Wrapper",
    author="schneefux",
    author_email="schneefux+pypi_schneefux@schneefux.xyz",
    url="https://git.schneefux.xyz/schneefux/python-gamelocker",
    packages=["gamelocker"],
    install_requires=["requests"],
    setup_requires=["pytest-runner"],
    tests_require=["pytest"]
)
