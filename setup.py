# -*- coding: utf-8 -*-

from setuptools import setup, find_packages


with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='AutosarConfigReader',
    version='0.1.5',
    description='Python module for reading autosar module configuration arxml files',
    long_description=readme,
    long_description_content_type="text/markdown",
    author='Girish Chandran',
    author_email='girishchandran.tpm@gmail.com',
    url='https://github.com/girishchandranc/autosarconfigreader',
    license="MIT",
    packages=find_packages(exclude=('tests')),
    include_package_data=True,
    install_requires=["lxml>=4.6.1",
                        "Jinja2>=2.11.2"],
    python_requires='>=3.6',
)
