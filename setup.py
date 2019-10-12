from setuptools import find_packages
from setuptools import setup
import condor


def install_requires():
    """
    Yields a list of install requirements.
    """
    return [
        'SQLAlchemy~=1.3',
        'bibtexparser~=0.6.2',
        'click~=6.7',
        'nltk~=3.4',
        'numpy~=1.12',
        'langdetect',
        'langcodes',
        'PyPDF2~=1.26',
        'tabulate~=0.7',
        'tqdm~=4.11.2',
        'requests>2,<3'
    ]

setup(
    name='condor-ir',
    version=condor.__version__,
    author='Oscar D. Arbeláez-Echeverri <@odarbelaeze>, German A. Osorio-Zuluaga',
    author_email='odarbelaeze@gmail.com',
    packages=find_packages(),
    install_requires=install_requires(),
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
        .format(condor.__version__)
    ),
    keywords=['lsa', 'search', 'search engine', 'semantics', ],
    description='A latent semantic search engine implementation',
)
