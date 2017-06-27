#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

with open('README') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    'click',
    'six',
    'spacy',
]

setup_requirements = [
]

test_requirements = [
    'mock',
]

setup(
    name='pynlai',
    version='0.1.0',
    description="PYthon Natural Language Application Interface library.",
    long_description=readme + '\n\n' + history,
    author="Chris Pappalardo",
    author_email='cpappala@yahoo.com',
    url='https://github.com/ChrisPappalardo/pynlai',
    packages=find_packages(include=['pynlai']),
    entry_points={
        'console_scripts': [
            'pynlai=pynlai.cli:entry_point'
        ]
    },
    include_package_data=True,
    install_requires=requirements,
    license="MIT license",
    zip_safe=False,
    keywords='pynlai',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
    ],
    test_suite='tests',
    tests_require=test_requirements,
    setup_requires=setup_requirements,
)
