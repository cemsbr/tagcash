"""A setuptools based setup module."""
from pathlib import Path

from setuptools import setup

HERE = Path().parent.resolve()  # pylint: disable=no-member

# Get the long description from the README file
README = HERE / 'README.rst'
with open(str(README), encoding='utf-8') as f:
    LONG_DESC = f.read()

setup(
    name='tagcash',
    version='1.0.0b2',
    description='Finances with tags in CLI',
    long_description=LONG_DESC,
    url='https://github.com/cemsbr/tagcash',
    author='Carlos Eduardo Moreira dos Santos',
    author_email='cems@cemshost.com.br',
    license='MIT',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: Financial and Insurance Industry',
        'Topic :: Office/Business :: Financial :: Accounting',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    keywords='accounting finance finances cli terminal',
    packages=['tagcash'],
    install_requires=[
        'docopt',
        'terminaltables',
    ],
    extras_require={
        'dev': [
            # coverage version:
            # - incomplete-file-path-in-xml-report
            #   https://bitbucket.org/ned/coveragepy/issues/578/
            # - Code climate requires < 4.4
            'coverage<4.4',
            'eradicate',
            'pip-tools',
            'rstcheck',
            'tox',
            # Python 3.5 support since 1.4.0
            'yala>=1.4.0',
        ]
    },
    entry_points={
        'console_scripts': [
            'tagcash=tagcash.interface:main',
        ],
    },
    test_suite='tests',
)
