#!/usr/bin/env python
# -*- coding: utf_8 -*-
from setuptools import setup, find_packages
from kintone_sdk4python import __author__, __version__, __license__

setup(
    name = 'kintone SDK for Python',
    version = __version__,
    description = 'kintone SDK for Python.',
    license = __license__,
    author = __author__,
    author_email = 'cy.nishio0820@gmail.com',
    url = 'https://github.com/sada-nishio/kintone_sdk4python.git',
    keywords = 'kintone SDK for Python.',
    packages = find_packages(),
    install_requires = ['requests']
)
