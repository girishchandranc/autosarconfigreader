# -*- coding: utf-8 -*-

from setuptools import setup, find_packages


with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='AutosarConfigReader',
    version='0.1.4',
    description='Python module for reading autosar module configuration arxml files',
    long_description=readme,
    author='Girish Chandran',
    author_email='girishchandran.tpm@gmail.com',
    url='https://github.com/girishchandranc/autosarconfigreader',
    license=license,
    packages=find_packages(exclude=('tests')),
    include_package_data=True,
    python_requires='>=3.6',
)
