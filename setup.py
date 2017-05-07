import os

from setuptools import find_packages
from setuptools import setup


def get_install_requires():
    if os.environ.get('READTHEDOCS', None) == 'True':
        return [
            'mock>=1.3.0',
        ]
    return [
        'SQLAlchemy==1.0.12',
        'bibtexparser>=0.6.2',
        'click>=6.2',
        'marshmallow>=2.4.2',
        'nltk>=3.1',
        'numpy>=1.9.2',
        'pyenchant>=1.6',
        'PyPDF2==1.26.0',
        'tabulate>=0.7.5',
        'tqdm==4.11.2',
    ]

VERSION = '1.1.0'

setup(
    name='condor-ir',
    version=VERSION,
    author='Oscar D. Arbeláez-Echeverri <@odarbelaeze>, German A. Osorio-Zuluaga',
    author_email='odarbelaeze@gmail.com',
    packages=find_packages(),
    install_requires=get_install_requires(),
    tests_require=[
        'cov-core>=1.15.0',
        'coverage>=3.7.1',
        'py>=1.4.29',
        'pytest>=2.8.0',
        'pytest-cov>=1.8.1',
    ],
    setup_requires=[
        'pytest-runner>=2.7,<3dev',
    ],
    entry_points='''
    [console_scripts]
    condor=condor.scripts.cli:condor
    ''',
    url='https://condor-ir.co',
    download_url=(
        'https://github.com/odarbelaeze/condor-ir/tarball/{}'
        .format(VERSION)
    ),
    keywords=['lsa', 'search', 'search engine', 'semantics', ],
    description='A latent semantic search engine implementation',
)
