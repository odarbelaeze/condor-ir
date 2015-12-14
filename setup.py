from setuptools import setup
from setuptools import find_packages


if __name__ == '__main__':
    setup(
        name='lsa-program',
        author='Oscar David Arbeláez <@odarbelaeze>',
        packages=find_packages(),
        install_requires=[
            'nltk==3.0.2',
            'pymongo==3.0.2',
            'numpy==1.9.2',
            'scipy==0.16.0',
            'marshmallow==2.4.2',
        ],
        tests_require=[
            'cov-core==1.15.0',
            'coverage==3.7.1',
            'py==1.4.27',
            'pytest==2.7.0',
            'pytest-cov==1.8.1',
        ],
        entry_points='''
            [console_scripts]
            lsapopulate=lsa.scripts.populate:lsapopulate
            lsamodel=lsa.scripts.model:lsamodel
            lsaquery=lsa.scripts.query:lsaquery
        '''
    )
