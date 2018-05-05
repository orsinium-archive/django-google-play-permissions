#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# external
# external
# external
from setuptools import find_packages, setup


setup(
    name='djgpp',
    version='0.1.0',

    author='orsinium',
    author_email='master_fess@mail.ru',

    description='Get app permissions from Google Play',
    long_description=open('README.rst').read(),
    keywords='django google play android permissions',

    packages=find_packages(),
    install_requires=[line for line in open('requirements.txt').read().split('\n') if line],

    url='https://github.com/orsinium/django-google-play-permissions',
    download_url='https://github.com/orsinium/django-google-play-permissions/tarball/master',

    license='GNU Lesser General Public License v3.0',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Plugins',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU Lesser General Public License v3 or later (LGPLv3+)',
        'Programming Language :: Python',
    ],
)
