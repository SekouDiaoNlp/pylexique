#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = ['joblib', 'colorama', 'tqdm', 'pyxlsb', "dataclasses>=0.6; python_version < '3.7'", 'Click>=7.1', 'pandas'] # integrate 'faster_than_csv'

setup_requirements = ['pytest-runner', ]

test_requirements = [
    'pytest-runner',
    'pytest',
    'pytest-cov',
    "dataclasses>=0.6; python_version < '3.7'",
    'Click>=7.1',
]

setup(
    author="SekouDiaoNlp",
    author_email='diao.sekou.nlp@gmail.com',
    classifiers=[
        'Development Status :: 5 - Production/Stable','Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Education',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
        'Topic :: Utilities',
        'Intended Audience :: Developers',
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: Education',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    description="Pylexique is a Python wrapper around Lexique83",
    entry_points={
        'console_scripts': [
            'pylexique=pylexique.cli:main',
        ],
    },
    install_requires=requirements,
    license="MIT license",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    package_data={'documentation': ['docs/*'],
                  'tests': ['tests/*'],
                  'translations': ['pylexique/locale/*'],
                  'type_stubs': ['pylexique/py.typed', 'pylexique/*'],
                  'pylexique383': ['pylexique/Lexique383/*']},
    keywords='pylexique',
    name='pylexique',
    packages=find_packages(include=['pylexique']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/SekouDiaoNlp/pylexique',
    version='1.3.5',
    zip_safe=False,
)
