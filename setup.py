# -*- coding: utf-8 -*-

from setuptools import setup, find_packages


with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='wordlist_processor',
    version='0.1.0',
    description='',
    long_description=readme,
    author='0x4E0x650x6F',
    author_email='tiago.alexand@gmail.com',
    url='www.tiagoalexandre.com',
    license=license,
    install_requires=[
        'bleach',
    ],
    packages=find_packages(exclude=('tests'))
)
