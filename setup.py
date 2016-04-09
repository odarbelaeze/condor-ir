import os

from setuptools import find_packages
from setuptools import setup


def get_install_requires():
    if os.environ.get('READTHEDOCS', None) == 'True':
        return [
            'mock>=1.3.0',
        ]
    return [
        'bibtexparser>=0.6.2',
        'click>=6.2',
        'marshmallow>=2.4.2',
        'nltk>=3.1',
        'numpy>=1.9.2',
        'pymongo>=3.2',
        'scipy>=0.16.0',
        'pyenchang>=1.6',
    ]


setup(
    name='lsa-program',
    version='0.2.2',
    author='Oscar David Arbeláez <@odarbelaeze>, German Augusto Osorio',
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
    lsapopulate=lsa.scripts.populate:lsapopulate
    lsamodel=lsa.scripts.model:lsamodel
    lsaquery=lsa.scripts.query:lsaquery
    ''',
    url='https://github.com/odarbelaeze/lsa-program',
    download_url='https://github.com/odarbelaeze/lsa-program/targall/0.2.2',
    keywords=['lsa', 'search', 'search engine', 'semantics', ],
    description='A latent semantic search engine implementation',
)
