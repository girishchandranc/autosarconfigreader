# -*- coding: utf-8 -*-

from setuptools import setup, find_packages


with open('README') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='AutosarConfigReader',
    version='0.1.0',
    description='Python module for generating classes corresponding to the autosar module definition arxml files',
    long_description=readme,
    author='Girish Chandran',
    author_email='girishchandran.tpm@gmail.com',
    url='https://github.com/girishchandranc/autosarconfigreader',
    license=license,
    packages=find_packages(exclude=('tests', 'test_resources', 'docs'))
)