import codecs
from os import path

from setuptools import find_packages, setup

__version__ = '0.1.0'

BASE_DIR = path.abspath(path.dirname(__file__))


def load_reqirements(f):
    with open(f, 'r') as file:
        return [line for line in file.readlines() if not line.startswith('#')]


with codecs.open(path.join(BASE_DIR, 'README.md'), encoding='utf-8') as f:
    LONG_DESCRIPTION = f.read()


install_requirements = load_reqirements('requirements.txt')
tests_requirements = load_reqirements('requirements.dev.txt')


setup(
    name='gcalcli',
    version=__version__,
    description='Simple CLI that interacts with Google Calendar',
    long_description=LONG_DESCRIPTION,
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3.6',
    ],
    packages=find_packages(exclude=['docs', 'tests*']),
    include_package_data=True,
    author='Krzysztof Drabek',
    dependency_links=[],
    author_email='kdrabek@gmail.com',
    install_requires=install_requirements,
    setup_requires=[
        'pytest-runner==2.9'
    ],
    tests_require=tests_requirements
)
