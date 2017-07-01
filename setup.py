from setuptools import find_packages
from setuptools import setup
import condor


def get_install_requires():
    """
    Yields a list of install requirements.
    """
    return [
        'SQLAlchemy==1.1.10',
        'bibtexparser==0.6.2',
        'click==6.7',
        'nltk==3.2.3',
        'numpy==1.12.1',
        'pyenchant==1.6.8',
        'PyPDF2==1.26.0',
        'tabulate==0.7.7',
        'tqdm==4.11.2',
        'requests==2.14.2',
    ]

setup(
    name='condor-ir',
    version=condor.__version__,
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
        .format(condor.__version__)
    ),
    keywords=['lsa', 'search', 'search engine', 'semantics', ],
    description='A latent semantic search engine implementation',
)
