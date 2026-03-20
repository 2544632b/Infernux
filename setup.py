"""
Minimal setup.py to force platform-specific wheel tags.

InfEngine ships pre-built native extensions (.pyd / .dll) as package data,
so the wheel must NOT be tagged 'py3-none-any'.  Overriding has_ext_modules()
makes setuptools produce a platform wheel (e.g. cp312-win_amd64).
"""

from setuptools import setup
from setuptools.dist import Distribution


class BinaryDistribution(Distribution):
    def has_ext_modules(self):
        return True


setup(distclass=BinaryDistribution)
