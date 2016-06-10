#!/usr/bin/env python3

from setuptools import find_packages, setup

setup(
    name='tp',
    description='A client and server REST framework',
    author='Hugo Osvaldo Barrera, Santiago Pappier',
    author_email='hugo@barrera.io, spappier@gmail.com',
    url='https://gitlab.com/hobarrera/tp-tecnicas-avanzada-prog',
    license='undefined',
    packages=find_packages(),
    include_package_data=True,
    long_description=open('README.rst').read(),
    install_requires=open('requirements.txt').read().splitlines(),
    use_scm_version={'version_scheme': 'post-release'},
    setup_requires=['setuptools_scm'],
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ]
)
