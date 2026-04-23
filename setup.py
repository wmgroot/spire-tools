import os
from setuptools import setup, find_packages

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    author = 'Matt Groot',
    author_email = '',
    classifiers = [
        'Development Status :: 3 - Alpha',
        'Topic :: Utilities',
        'License :: GNU GENERAL PUBLIC LICENSE :: Version 3',
    ],
    description = ('Spire Helper Tools'),
    entry_points = {
        'console_scripts': [
            'spire = spire.spire:main',
        ],
    },
    include_package_data = True,
    install_requires = [
        'ruamel.yaml==0.18.16'
    ],
    keywords = 'spire city must fall rpg trpg tools rowan rook decard',
    license = 'GPL3',
    long_description = read('README.md'),
    long_description_content_type='text/markdown',
    name = 'spire-tools',
    packages = find_packages(),
    python_requires = '>=3.5',
    url = 'https://github.com/wmgroot/spire-tools',
    version = '0.1.0',
)
